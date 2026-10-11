import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# -----------------------------
# CNN MODEL
# -----------------------------

class CatDogCNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.relu = nn.ReLU()

        self.conv1 = nn.Conv2d(3,16,3,padding=1)

        self.pool = nn.MaxPool2d(2,2)

        self.conv2 = nn.Conv2d(16,32,3,padding=1)

        self.conv3 = nn.Conv2d(32,64,3,padding=1)

        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(64*18*18,128)

        self.fc2 = nn.Linear(128,2)

    def forward(self,x):

        x=self.pool(self.relu(self.conv1(x)))
        x=self.pool(self.relu(self.conv2(x)))
        x=self.pool(self.relu(self.conv3(x)))

        x=self.flatten(x)

        x=self.relu(self.fc1(x))

        x=self.fc2(x)

        return x


# -----------------------------
# LOAD MODEL
# -----------------------------

model=CatDogCNN()

model.load_state_dict(torch.load("catdogAI/catdog_model.pth"))

model.eval()

# -----------------------------
# IMAGE TRANSFORM
# -----------------------------

transform=transforms.Compose([
    transforms.Resize((150,150)),
    transforms.ToTensor()
])

# -----------------------------
# LOAD IMAGE
# -----------------------------

image=Image.open("catdogAI/ccc.jpg").convert("RGB")

image=transform(image)

image=image.unsqueeze(0)

# -----------------------------
# PREDICT
# -----------------------------

with torch.no_grad():

    output=model(image)

    prediction=torch.argmax(output,1).item()

classes=["cat","dog"]

print("Prediction:",classes[prediction])
