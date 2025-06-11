# Image Enhancer Server

This is the backend server for the Image Enhancer application. It provides API endpoints for image upload and enhancement using OpenCV.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Run the server using:
```bash
python app.py
```

The server will start on http://localhost:5000

## API Endpoints

### Upload and Enhance Image
- **URL**: `/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Form Parameter**: `image`
- **Response**: JSON with enhanced image URL

### Get Enhanced Image
- **URL**: `/get-image/<filename>`
- **Method**: `GET`
- **Response**: JPEG image file

## Directory Structure
- `uploads/`: Stores uploaded images
- `output/`: Stores enhanced images 