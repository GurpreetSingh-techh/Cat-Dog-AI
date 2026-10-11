/* =========================================
   ELEMENTS
========================================= */

const imageInput = document.getElementById("imageInput");

const uploadArea = document.getElementById("uploadArea");

const uploadContent = document.getElementById("uploadContent");

const browseButton = document.getElementById("browseButton");

const previewContainer =
    document.getElementById("previewContainer");

const previewImage =
    document.getElementById("previewImage");

const removeImage =
    document.getElementById("removeImage");

const guessButtons =
    document.querySelectorAll(".guess-button");

const predictButton =
    document.getElementById("predictButton");

const predictText =
    document.getElementById("predictText");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const resultAnimal =
    document.getElementById("resultAnimal");

const resultTitle =
    document.getElementById("resultTitle");

const confidenceText =
    document.getElementById("confidenceText");

const progressBar =
    document.getElementById("progressBar");

const gameResult =
    document.getElementById("gameResult");

const tryAgain =
    document.getElementById("tryAgain");


/* =========================================
   VARIABLES
========================================= */

let selectedFile = null;

let userGuess = null;


/* =========================================
   OPEN FILE SELECTOR
========================================= */

browseButton.addEventListener("click", function (event) {

    event.stopPropagation();

    imageInput.click();

});


uploadArea.addEventListener("click", function () {

    if (!selectedFile) {

        imageInput.click();

    }

});


/* =========================================
   FILE SELECTED
========================================= */

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (file) {

        handleImage(file);

    }

});


/* =========================================
   HANDLE IMAGE
========================================= */

function handleImage(file) {

    if (!file.type.startsWith("image/")) {

        alert("Please select an image file.");

        return;
    }


    selectedFile = file;


    const reader = new FileReader();


    reader.onload = function (event) {

        previewImage.src = event.target.result;

        uploadContent.style.display = "none";

        previewContainer.classList.add("show");

        result.classList.remove("show");

        loading.classList.remove("show");

        updatePredictButton();

    };


    reader.readAsDataURL(file);

}


/* =========================================
   DRAG & DROP
========================================= */

uploadArea.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadArea.classList.add("dragover");

});


uploadArea.addEventListener("dragleave", function () {

    uploadArea.classList.remove("dragover");

});


uploadArea.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadArea.classList.remove("dragover");


    const files = event.dataTransfer.files;


    if (files.length > 0) {

        handleImage(files[0]);

    }

});


/* =========================================
   REMOVE IMAGE
========================================= */

removeImage.addEventListener("click", function (event) {

    event.stopPropagation();

    resetImage();

});


function resetImage() {

    selectedFile = null;

    imageInput.value = "";

    previewImage.src = "";

    uploadContent.style.display = "block";

    previewContainer.classList.remove("show");

    result.classList.remove("show");

    loading.classList.remove("show");

    progressBar.style.width = "0%";

    confidenceText.textContent = "0%";

    userGuess = null;


    guessButtons.forEach(function (button) {

        button.classList.remove("selected");

    });


    updatePredictButton();

}


/* =========================================
   USER GUESS
========================================= */

guessButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        userGuess =
            button.dataset.guess;


        guessButtons.forEach(function (item) {

            item.classList.remove("selected");

        });


        button.classList.add("selected");


        updatePredictButton();

    });

});


/* =========================================
   ENABLE / DISABLE PREDICT BUTTON
========================================= */

function updatePredictButton() {

    if (selectedFile && userGuess) {

        predictButton.disabled = false;

    } else {

        predictButton.disabled = true;

    }

}


/* =========================================
   PREDICT
========================================= */

predictButton.addEventListener("click", async function () {

    if (!selectedFile || !userGuess) {

        return;

    }


    /* Hide previous result */

    result.classList.remove("show");


    /* Show loading */

    loading.classList.add("show");


    predictButton.disabled = true;

    predictText.textContent = "Analyzing...";


    try {

        /*
         * Send image to your Python backend.
         *
         * Your backend should have:
         *
         * POST /predict
         *
         * and return JSON like:
         *
         * {
         *     "prediction": "dog",
         *     "confidence": 94.7
         * }
         */


        const formData = new FormData();

        formData.append(
            "image",
            selectedFile
        );


        /*
         * IMPORTANT:
         *
         * This URL assumes your Python server
         * is running on the same website.
         *
         * Later, if your Flask/FastAPI server
         * runs on another port, change this.
         */


        const response = await fetch(
            "/predict",
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {

            throw new Error(
                "Server error"
            );

        }


        const data = await response.json();


        showResult(
            data.prediction,
            data.confidence
        );


    } catch (error) {

    console.error(error);

    loading.classList.remove("show");

    predictButton.disabled = false;

    predictText.textContent = "Let AI Guess";

    alert(
        "Could not connect to the AI model. Make sure the Python server is running."
    );
}

    }

);


/* =========================================
   SHOW RESULT
========================================= */

function showResult(prediction, confidence) {

    loading.classList.remove("show");


    prediction =
        String(prediction).toLowerCase();


    confidence =
        Number(confidence);


    if (confidence <= 1) {

        confidence *= 100;

    }


    confidence =
        Math.min(
            100,
            Math.max(0, confidence)
        );


    /* Animal */

    if (prediction === "cat") {

        resultAnimal.textContent = "🐱";

        resultTitle.textContent = "Cat";

    } else {

        resultAnimal.textContent = "🐶";

        resultTitle.textContent = "Dog";

    }


    /* Confidence */

    confidenceText.textContent =
        confidence.toFixed(1) + "%";


    progressBar.style.width =
        confidence + "%";


    /* User result */

    if (userGuess === prediction) {

        gameResult.textContent =
            "🎉 You beat the AI's prediction!";

        gameResult.classList.remove("wrong");

    } else {

        gameResult.textContent =
            "AI got it this time!";

        gameResult.classList.add("wrong");

    }


    result.classList.add("show");


    predictText.textContent =
        "Let AI Guess";


    predictButton.disabled = false;


    result.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


/* =========================================
   TRY AGAIN
========================================= */

tryAgain.addEventListener("click", function () {

    resetImage();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});
