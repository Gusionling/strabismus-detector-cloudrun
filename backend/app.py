import cv2
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from tensorflow.keras.models import load_model
import tensorflow as tf
from fastapi.staticfiles import StaticFiles

# Load the pre-trained Haar cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load your trained TensorFlow model
model = load_model('./model.h5')

app = FastAPI()
app.mount("/db", StaticFiles(directory="db"), name="db")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def preprocess_image(img):
    # Resize to 300x70 pixels
    img_resized = cv2.resize(img, (300, 70))
    return img_resized

@app.post("/predict/")
async def predict(
    file: UploadFile = File(...),
    name: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...)    
    ):

    print("hi")
    # Read the uploaded image file
    contents = await file.read()
    
    # Decode the image using OpenCV
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), -1)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform eye detection
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

    # Check if 2 or more eyes are detected
    if len(eyes) >= 2:
        # Sort eyes by x coordinate
        sorted_eyes = sorted(eyes, key=lambda x: x[0])

        # Get the leftmost and rightmost eyes
        left_eye = sorted_eyes[0]
        right_eye = sorted_eyes[-1]

        # Create a bounding box that encompasses both eyes
        box_start = (left_eye[0], min(left_eye[1], right_eye[1]))
        box_end = (right_eye[0] + right_eye[2], max(left_eye[1] + left_eye[3], right_eye[1] + right_eye[3]))

        filepath = "./db/"+name+".jpg"

        cv2.rectangle(img, box_start, box_end, (0, 255, 0), 5)
        cv2.imwrite(filepath, img)

        filepath = "http://localhost:8000/db/"+name+".jpg"

        # Crop the image to include only the region with both eyes
        cropped_img = img[box_start[1]:box_end[1], box_start[0]:box_end[0]]

        # Preprocess the cropped image
        img_preprocessed = preprocess_image(cropped_img)

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
        conditions = ['Mild', 'Moderate', 'Severe']

        if confidence < 30:
            condition = conditions[0]
        elif confidence < 60:
            condition = conditions[1]
        else:
            condition = conditions[2]

        # Return the prediction result
        return {
            "patient": {
                "name": name,
                "age": age,
                "sex": sex,
                "image": filepath
            },
            "prediction": {
                "class": class_names[predicted_class],
                "confidence": confidence,
                "condition": condition,
            }
        }
    else:
        return {"error": "Less than two eyes detected"}
