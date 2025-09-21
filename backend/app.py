import cv2
import numpy as np
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
import tensorflow as tf

# 애플리케이션 기본 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 모델 파일 경로
MODEL_PATH = os.path.join(BASE_DIR, 'model.h5')

# Load the pre-trained Haar cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load your trained TensorFlow model
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"모델 로드 오류: {e}")
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        print(f"두 번째 시도에서도 모델 로드 실패: {e}")
        model = None

app = FastAPI(
    title="Strabismus Detector API",
    description="사시 감지 및 분류를 위한 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Strabismus Detector API is running"}

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
    try:
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
            confidence = float(100 * np.max(score))  # Calculate confidence and convert to native float

            class_names = ['esotropia', 'exotropia', 'hypertropia', 'hypotropia', 'normal']

            print(f"This image most likely belongs to {class_names[predicted_class]} with a {confidence:.2f}% confidence.")

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
                    "sex": sex
                },
                "prediction": {
                    "class": class_names[predicted_class],
                    "confidence": confidence,
                    "condition": condition,
                }
            }
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Less than two eyes detected in the image"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred during processing: {str(e)}"}
        )
