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

# Define the endpoint for making predictions
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded image file
    contents = await file.read()
    
    img = tf.keras.utils.load_img(io.BytesIO(contents), target_size=(70, 300))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    # Make predictions using the loaded model
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    predicted_class = np.argmax(score)  # Get the predicted class index
    confidence = 100 * np.max(score)  # Calculate confidence
    
    class_names = ['esotropia', 'exotropia', 'hypertropia', 'hypotropia', 'normal']  # Update with your class names
    
    print("This image most likely belongs to {} with a {:.2f}% confidence.".format(class_names[predicted_class], confidence))
    
    # Return the prediction result
    return {"class": class_names[predicted_class], "confidence": confidence}
