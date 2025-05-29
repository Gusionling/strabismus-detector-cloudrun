# Strabismus Detector - Cloud Run Version

This project is a modified version of [Strabismus-Detector](https://github.com/aswinpradeepc/Strabismus-Detector), adapted to run on **Google Cloud Run**.

## 🧠 About

An end-to-end machine learning project to let people test for **strabismus** (squint-eye) and recognize the type of condition.  
The image classification model is built using **TensorFlow**, with a backend developed in **FastAPI** and a frontend using **React**.

## 🚀 Modifications in This Version

- Added Docker support for containerized deployment
- Configured application to run on **Google Cloud Run**
- Updated structure for deployment compatibility

## 🏗️ Deployment (Google Cloud Run)

### 1. Build the image
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/strabismus-detector

