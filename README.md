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

## Deployment

### Backend Deployment (Flask) - Render

1. Create a Render account at https://render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: cd server && gunicorn app:app
   ```
5. Add environment variables if needed
6. Choose your plan and deploy

### Frontend Deployment (React) - Netlify

1. Create a Netlify account at https://www.netlify.com
2. Create a new site from Git
3. Connect your GitHub repository
4. Configure the build settings:
   ```
   Base directory: client
   Build command: npm run build
   Publish directory: client/build
   ```
5. Add environment variables:
   ```
   REACT_APP_API_URL=your_backend_url
   ```
6. Deploy

### Alternative Backend Deployment (Python Anywhere)

1. Create a PythonAnywhere account at https://www.pythonanywhere.com
2. Go to the Web tab and create a new web app
3. Choose Manual Configuration and Python 3.8
4. Set up your virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.8 myenv
   pip install -r requirements.txt
   ```
5. Configure WSGI file:
   ```python
   import sys
   path = '/home/yourusername/your-repo-name'
   if path not in sys.path:
       sys.path.append(path)
   
   from server.app import app as application
   ```
6. Configure static files and reload the web app

### Docker Deployment

1. Create a Dockerfile in the root directory:
   ```dockerfile
   # Build frontend
   FROM node:14 AS frontend-build
   WORKDIR /app/client
   COPY client/package*.json ./
   RUN npm install
   COPY client/ ./
   RUN npm run build

   # Build backend
   FROM python:3.8-slim
   WORKDIR /app
   
   # Copy backend requirements and install dependencies
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   # Copy backend code
   COPY server/ ./server/
   
   # Copy built frontend from previous stage
   COPY --from=frontend-build /app/client/build ./client/build
   
   # Run the application
   EXPOSE 5000
   CMD ["python", "server/app.py"]
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t image-enhancer .
   docker run -p 5000:5000 image-enhancer
   ```

### Environment Variables

Create a `.env` file in both client and server directories:

Frontend (.env):
```
REACT_APP_API_URL=your_backend_url
```

Backend (.env):
```
FLASK_ENV=production
FLASK_APP=app.py
```

### Production Considerations

1. **SSL/HTTPS**: Enable SSL certificates for secure communication
2. **CORS**: Update CORS settings in Flask for production domains
3. **Error Logging**: Set up proper error logging (e.g., Sentry)
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Monitoring**: Set up monitoring tools (e.g., New Relic)
6. **Backup**: Configure regular backups for uploaded files
7. **Scaling**: Consider using a CDN for static files

### CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    
    - name: Install Node.js dependencies
      run: |
        cd client
        npm install
        npm run build
    
    - name: Deploy to production
      env:
        PRODUCTION_URL: ${{ secrets.PRODUCTION_URL }}
      run: |
        # Add your deployment commands here
```

### Vercel Deployment

#### Backend Deployment (Flask)

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Navigate to the server directory:
   ```bash
   cd server
   ```

4. Deploy to Vercel:
   ```bash
   vercel
   ```

5. For production deployment:
   ```bash
   vercel --prod
   ```

#### Frontend Deployment (React)

1. Install Vercel CLI (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. Navigate to the client directory:
   ```bash
   cd client
   ```

3. Deploy to Vercel:
   ```bash
   vercel
   ```

4. For production deployment:
   ```bash
   vercel --prod
   ```

#### Environment Variables in Vercel

1. Backend Environment Variables:
   - Go to your Vercel project settings
   - Navigate to the "Environment Variables" section
   - Add the following:
     ```
     FLASK_ENV=production
     FLASK_APP=app.py
     ```

2. Frontend Environment Variables:
   - In your frontend project settings on Vercel
   - Add:
     ```
     REACT_APP_API_URL=your_backend_vercel_url
     ```

#### Important Notes for Vercel Deployment

1. Make sure your backend URL is correctly set in the frontend environment variables
2. Both frontend and backend will have different URLs in Vercel
3. Update CORS settings in Flask to allow your frontend domain
4. Vercel automatically handles SSL/HTTPS
5. Each push to main branch will trigger automatic deployment if you've connected your GitHub repository 