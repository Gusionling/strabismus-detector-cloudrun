FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY app.py .
COPY model.h5 .
COPY detect.py .
COPY keras ./keras
COPY tensorflow ./tensorflow

# Set environment variable for port
ENV PORT=8080

# Expose port for Cloud Run
EXPOSE 8080

# Configure startup command
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT}
