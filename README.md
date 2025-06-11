# Image Enhancer

A modern web application for image enhancement and colorization using React (frontend) and Flask (backend). The application provides two main features: image enhancement and black & white image colorization.

**Author & Owner**: Omkar

## Features

### Image Enhancement
- Noise reduction using Non-Local Means Denoising
- Detail enhancement with custom parameters
- Contrast improvement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Smart sharpening with custom kernels
- Brightness and contrast optimization
- Support for multiple image formats (PNG, JPG, JPEG, GIF)

### Image Colorization
- Grayscale to color conversion
- Adaptive histogram equalization
- Custom color mapping using COLORMAP_MAGMA
- Smart color blending for natural results
- Real-time processing

### User Interface
- Drag and drop file upload
- Progress tracking
- Side-by-side image comparison
- Mode selection (enhance/colorize)
- One-click download of processed images
- Responsive design
- Error handling and validation

## Technologies Used

### Frontend
- React.js
- Material-UI for components
- Axios for API calls
- React Dropzone for file uploads
- CSS Grid and Flexbox for layout

### Backend
- Flask (Python web framework)
- OpenCV for image processing
- NumPy for numerical operations
- Pillow for image validation
- Flask-CORS for cross-origin support

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install Python dependencies:
```bash
pip install flask flask-cors opencv-python pillow numpy
```

3. Start the Flask server:
```bash
cd server
python app.py
```
The backend server will run on http://localhost:5000

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd client
npm install
```

2. Start the React development server:
```bash
npm start
```
The frontend application will run on http://localhost:3000

## Project Structure

```
Image enhancer/
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   └── styles/        # CSS styles
│   ├── package.json
│   └── public/
├── server/                 # Backend Flask application
│   ├── app.py             # Main Flask application
│   ├── uploads/           # Temporary storage for uploaded images
│   └── output/            # Processed images storage
└── README.md
```

## API Endpoints

### POST /upload
- Uploads and processes an image
- Parameters:
  - `image`: Image file (multipart/form-data)
  - `mode`: 'enhance' or 'colorize'
- Returns: JSON with processed image URL

### GET /get-image/<filename>
- Retrieves processed image
- Parameters:
  - `download`: boolean (optional) - for direct download
- Returns: Image file or download response

## Image Processing Details

### Enhancement Pipeline
1. Denoising using `cv2.fastNlMeansDenoisingColored`
2. Detail enhancement with `cv2.detailEnhance`
3. LAB color space conversion for better color processing
4. CLAHE application for contrast enhancement
5. Smart sharpening using custom kernel
6. Final adjustments for brightness and contrast

### Colorization Pipeline
1. Grayscale conversion (if needed)
2. Adaptive histogram equalization using CLAHE
3. Color mapping with COLORMAP_MAGMA
4. Color enhancement and blending
5. Final adjustments for natural appearance

## Usage

1. Open the web application in your browser (http://localhost:3000)
2. Drag and drop an image or click to select one
3. Choose the processing mode (enhance or colorize)
4. Wait for processing to complete
5. Compare the original and processed images
6. Download the processed image if desired

## File Handling

- Maximum file size: 16MB
- Supported formats: PNG, JPG, JPEG, GIF
- Automatic cleanup of temporary files (24-hour retention)
- Secure filename handling
- Image content validation

## Error Handling

- File type validation
- Image content verification
- Size limit enforcement
- Processing error handling
- Graceful error messages

## Security Features

- Secure file handling
- Directory traversal prevention
- File size limitations
- Content type validation
- Cross-origin resource sharing (CORS) configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 