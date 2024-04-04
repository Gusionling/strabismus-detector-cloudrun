import tensorflow as tf
from fastapi import FastAPI, File, UploadFile
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import io
import cv2

# Load your trained TensorFlow model
model = tf.keras.models.load_model('./model.h5')

# Define your FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def preprocess_image(img):
    # Resize to 300x70 pixels
    img_resized = cv2.resize(img, (300, 70))
    return img_resized


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded image file
    contents = await file.read()

    # Decode the image using OpenCV
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), -1)

    # Preprocess the image
    img_preprocessed = preprocess_image(img)

    # Convert to a format compatible with TensorFlow
    img_array = tf.keras.preprocessing.image.img_to_array(img_preprocessed)
    img_array = np.expand_dims(img_array, axis=0)  # Create a batch

    # Make predictions using the loaded model
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    predicted_class = np.argmax(score)  # Get the predicted class index
    confidence = 100 * np.max(score)  # Calculate confidence

    class_names = ['esotropia', 'exotropia', 'hypertropia', 'hypotropia', 'normal']  # Update with your class names

    print("This image most likely belongs to {} with a {:.2f}% confidence.".format(class_names[predicted_class],
                                                                                   confidence))

    # Return the prediction result
    return {"class": class_names[predicted_class], "confidence": confidence}
