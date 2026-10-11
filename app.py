from flask import Flask, request, jsonify, send_from_directory
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# DEVICE
# ==========================================

device = torch.device("cpu")

print("Using device:", device)


# ==========================================
# CNN MODEL
# This MUST match your training model
# ==========================================

class CatDogCNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.relu = nn.ReLU()

        self.conv1 = nn.Conv2d(
            3,
            16,
            3,
            padding=1
        )

        self.pool = nn.MaxPool2d(2, 2)

        self.conv2 = nn.Conv2d(
            16,
            32,
            3,
            padding=1
        )

        self.conv3 = nn.Conv2d(
            32,
            64,
            3,
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

        x = self.pool(
            self.relu(
                self.conv1(x)
            )
        )

        x = self.pool(
            self.relu(
                self.conv2(x)
            )
        )

        x = self.pool(
            self.relu(
                self.conv3(x)
            )
        )

        x = self.flatten(x)

        x = self.relu(
            self.fc1(x)
        )

        x = self.fc2(x)

        return x


# ==========================================
# LOAD MODEL
# ==========================================

model = CatDogCNN()


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "catdog_model.pth"
)


print("Loading model from:")
print(MODEL_PATH)


model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)


model.to(device)

model.eval()


print("Model loaded successfully!")


# ==========================================
# IMAGE TRANSFORM
# SAME AS TRAINING
# ==========================================

transform = transforms.Compose([

    transforms.Resize(
        (150, 150)
    ),

    transforms.ToTensor()

])


# ==========================================
# CLASSES
# ==========================================

classes = [
    "cat",
    "dog"
]


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return send_from_directory(
        os.path.dirname(__file__),
        "index.html"
    )


# ==========================================
# CSS FILE
# ==========================================

@app.route("/style.css")
def css():

    return send_from_directory(
        os.path.dirname(__file__),
        "style.css"
    )


# ==========================================
# JAVASCRIPT FILE
# ==========================================

@app.route("/script.js")
def javascript():

    return send_from_directory(
        os.path.dirname(__file__),
        "script.js"
    )


# ==========================================
# PREDICTION API
# ==========================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # ----------------------------------
        # CHECK IMAGE
        # ----------------------------------

        if "image" not in request.files:

            return jsonify({
                "error": "No image was uploaded."
            }), 400


        file = request.files["image"]


        if file.filename == "":

            return jsonify({
                "error": "No image was selected."
            }), 400


        # ----------------------------------
        # OPEN IMAGE
        # ----------------------------------

        image = Image.open(
            file.stream
        ).convert("RGB")


        # ----------------------------------
        # PREPROCESS IMAGE
        # ----------------------------------

        image = transform(image)


        # Add batch dimension

        image = image.unsqueeze(0)


        image = image.to(device)


        # ----------------------------------
        # MODEL PREDICTION
        # ----------------------------------

        with torch.no_grad():

            output = model(image)


            # Convert raw model output
            # into probabilities

            probabilities = torch.softmax(
                output,
                dim=1
            )


            confidence, prediction = torch.max(
                probabilities,
                1
            )


        # ----------------------------------
        # GET RESULT
        # ----------------------------------

        predicted_class = classes[
            prediction.item()
        ]


        confidence_value = (
            confidence.item() * 100
        )


        print(
            f"Prediction: {predicted_class}"
        )

        print(
            f"Confidence: {confidence_value:.2f}%"
        )


        # ----------------------------------
        # SEND RESULT TO JAVASCRIPT
        # ----------------------------------

        return jsonify({

            "prediction": predicted_class,

            "confidence": round(
                confidence_value,
                2
            )

        })


    except Exception as e:

        print("Prediction error:")

        print(e)


        return jsonify({

            "error": str(e)

        }), 500


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print()
    print("==============================")
    print(" Cat vs Dog AI")
    print("==============================")
    print()
    print(
        "Open this in your browser:"
    )
    print(
        "http://127.0.0.1:5000"
    )
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
    