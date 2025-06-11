from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import cv2
from PIL import Image
import time
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def clean_old_files(directory, max_age_hours=24):
    current_time = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file_age = current_time - os.path.getctime(filepath)
        if file_age > (max_age_hours * 3600):
            try:
                os.remove(filepath)
            except Exception:
                pass

def colorize_image(image):
    try:
        # Convert to grayscale if not already
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Create a simple colorization effect using adaptive histogram equalization
        # and color mapping
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)

        # Create a pseudo-color effect
        # Apply a color map (COLORMAP_MAGMA gives nice, natural-looking colors)
        colored = cv2.applyColorMap(enhanced_gray, cv2.COLORMAP_MAGMA)

        # Enhance the colors
        colored = cv2.convertScaleAbs(colored, alpha=1.1, beta=0)
        
        # Apply slight blending for more natural look
        colored = cv2.addWeighted(colored, 0.8, cv2.GaussianBlur(colored, (5, 5), 0), 0.2, 0)

        return colored
    except Exception as e:
        raise Exception(f"Error in colorization: {str(e)}")

def enhance_image(input_path, output_path, mode='enhance'):
    try:
        # Read the image using OpenCV
        img = cv2.imread(input_path)
        if img is None:
            return False, "Failed to read image"

        if mode == 'colorize':
            # Convert to grayscale first to ensure consistent colorization
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            enhanced = colorize_image(gray)
        else:  # Default enhance mode
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Step 1: Denoise the image
            denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

            # Step 2: Apply detail enhancement
            enhanced = cv2.detailEnhance(denoised, sigma_s=12, sigma_r=0.15)

            # Step 3: Improve clarity and contrast
            lab = cv2.cvtColor(enhanced, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            
            enhanced_lab = cv2.merge((cl, a, b))
            enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)

            # Step 4: Apply smart sharpening
            kernel = np.array([[-1,-1,-1],
                             [-1, 9,-1],
                             [-1,-1,-1]])
            
            sharpened = cv2.filter2D(enhanced, -1, kernel)
            enhanced = cv2.addWeighted(enhanced, 0.7, sharpened, 0.3, 0)

            # Step 5: Final adjustments
            alpha = 1.1  # Contrast control
            beta = 5    # Brightness control
            enhanced = cv2.convertScaleAbs(enhanced, alpha=alpha, beta=beta)

            # Convert back to BGR
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_RGB2BGR)
        
        # Save the enhanced image
        cv2.imwrite(output_path, enhanced, [cv2.IMWRITE_JPEG_QUALITY, 100])
        return True, "Image processed successfully"
    except Exception as e:
        return False, str(e)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Clean old files
        clean_old_files(UPLOAD_FOLDER)
        clean_old_files(OUTPUT_FOLDER)

        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400

        # Get the enhancement mode
        mode = request.form.get('mode', 'enhance')
        if mode not in ['enhance', 'colorize']:
            return jsonify({'error': 'Invalid mode. Use "enhance" or "colorize"'}), 400

        # Generate unique filename
        timestamp = int(time.time())
        original_ext = os.path.splitext(secure_filename(file.filename))[1]
        input_filename = f'image_{timestamp}{original_ext}'
        output_filename = f'enhanced_{timestamp}.jpg'
        
        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Save the uploaded file
        file.save(input_path)

        # Validate image content
        if not validate_image(input_path):
            os.remove(input_path)
            return jsonify({'error': 'Invalid image content'}), 400

        # Process the image
        success, message = enhance_image(input_path, output_path, mode)
        
        if not success:
            try:
                os.remove(input_path)
            except:
                pass
            return jsonify({'error': message}), 500

        return jsonify({
            'message': 'Image processed successfully',
            'enhanced_image': f'/get-image/{output_filename}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-image/<filename>')
def get_image(filename):
    try:
        # Validate filename to prevent directory traversal
        filename = secure_filename(filename)
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Image not found'}), 404

        # Get the download parameter
        download = request.args.get('download', 'false').lower() == 'true'

        return send_file(
            file_path,
            mimetype='image/jpeg',
            as_attachment=download,  # Set to True for download, False for display
            download_name=f'enhanced_{filename}' if download else filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure the upload size limit is set
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.run(debug=True, port=5000, host='0.0.0.0') 