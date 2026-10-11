import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import random_split
transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor()
])
dataset = datasets.ImageFolder(
    root="catdogAI/dataset",
    transform=transform
)
train_size = int(0.8 * len(dataset))

validation_size = len(dataset) - train_size


train_dataset, validation_dataset = random_split(
    dataset,
    [train_size, validation_size]
)


train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)


validation_loader = DataLoader(
    validation_dataset,
    batch_size=32,
    shuffle=False
)
print("Number of images:", len(dataset))

print("Classes:", dataset.classes)

class CatDogCNN(nn.Module):

    def __init__(self):
        super().__init__()
        self.relu = nn.ReLU()

        self.conv1 = nn.Conv2d(
    in_channels=3,
    out_channels=16,
    kernel_size=3,
    padding=1
) 
        self.pool = nn.MaxPool2d(2,2)

        self.conv2 = nn.Conv2d(
    16,
    32,
    kernel_size=3,
    padding=1
)
        self.conv3 = nn.Conv2d(
    32,
    64,
    kernel_size=3,
    padding=1
)
        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(
    64 * 18 * 18,
    128
)
        self.fc2 = nn.Linear(
    128,
    2
)
        
    def forward(self, x):

     x = self.pool(self.relu(self.conv1(x)))

     x = self.pool(self.relu(self.conv2(x)))

     x = self.pool(self.relu(self.conv3(x)))

     x = self.flatten(x)

     x = self.relu(self.fc1(x))

     x = self.fc2(x)

     return x


model = CatDogCNN()
criterion = nn.CrossEntropyLoss()

print(model)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)
epochs = 10
for epoch in range(epochs):

    running_loss = 0.0

    total_train = 0
    correct_train = 0


    for images, labels in train_loader:

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        _,predicted = torch.max(
            outputs,
            1
        )

        total_train += labels.size(0)

        correct_train += torch.sum(
        predicted == labels
)       .item()



    train_accuracy = (
        100 * correct_train / total_train
    )

    model.eval()


    total_validation = 0
    correct_validation = 0



    with torch.no_grad():


        for images, labels in validation_loader:


            outputs = model(images)



            _, predicted = torch.max(
                outputs,
                1
            )


            total_validation += labels.size(0)


            correct_validation += (
                predicted == labels
            ).sum().item()



    validation_accuracy = (
        100 * correct_validation / total_validation
    )




    

    print(
        f"Epoch {epoch+1}/{epochs}, Loss: {running_loss:.4f}"
    )

    print(
        f"""
Epoch {epoch+1}/{epochs}

Loss: {running_loss:.4f}

Training Accuracy: {train_accuracy:.2f}%

Validation Accuracy: {validation_accuracy:.2f}%

----------------------------
"""
    )

    torch.save(model.state_dict(), "catdog_model.pth")

print("Model Saved Successfully!")