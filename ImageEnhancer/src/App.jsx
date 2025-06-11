import React, { useState, useCallback } from "react";
import axios from "axios";

const MAX_FILE_SIZE = 16 * 1024 * 1024; // 16MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif"];

function App() {
  const [image, setImage] = useState(null);
  const [enhancedImage, setEnhancedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [mode, setMode] = useState('enhance');

  const validateFile = (file) => {
    if (!file) return "Please select an image file";
    if (!ALLOWED_TYPES.includes(file.type)) {
      return "Invalid file type. Please upload a JPEG, PNG, or GIF image.";
    }
    if (file.size > MAX_FILE_SIZE) {
      return "File is too large. Maximum size is 16MB.";
    }
    return null;
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    const error = validateFile(file);
    
    setError(error);
    setImage(error ? null : file);
    setEnhancedImage(null);
    setProgress(0);
  };

  const handleUpload = async () => {
    if (!image) {
      setError("Please select an image first");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setProgress(0);
      
      const formData = new FormData();
      formData.append("image", image);
      formData.append("mode", mode);

      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted);
        },
      });

      const enhancedImageUrl = `http://localhost:5000${response.data.enhanced_image}`;
      setEnhancedImage(enhancedImageUrl);
    } catch (err) {
      const errorMessage = err.response?.data?.error || 
                         err.message || 
                         "Failed to process image";
      setError(errorMessage);
      setEnhancedImage(null);
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = useCallback(() => {
    setError(null);
    setEnhancedImage(null);
    setProgress(0);
    setImage(null);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-8">AI Image Enhancer</h1>
      
      <div className="w-full max-w-md">
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            Select Image (Max 16MB)
          </label>
          <input
            type="file"
            accept="image/jpeg,image/png,image/gif"
            onChange={handleFileChange}
            className="w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
          />
          <p className="mt-2 text-xs text-gray-400">
            Supported formats: JPEG, PNG, GIF
          </p>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            Processing Mode
          </label>
          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => setMode('enhance')}
              className={`py-2 px-4 rounded transition-colors ${
                mode === 'enhance'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              Enhance Image
            </button>
            <button
              onClick={() => setMode('colorize')}
              className={`py-2 px-4 rounded transition-colors ${
                mode === 'colorize'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              Colorize B&W
            </button>
          </div>
          <p className="mt-2 text-xs text-gray-400">
            {mode === 'enhance' 
              ? 'Enhance image quality, reduce noise, and improve clarity'
              : 'Convert black & white images to color using AI'}
          </p>
        </div>

        {progress > 0 && progress < 100 && (
          <div className="mb-4">
            <div className="w-full bg-gray-700 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-400 mt-1">
              Uploading: {progress}%
            </p>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={loading || !image}
          className={`w-full py-2 px-4 rounded ${
            loading || !image
              ? "bg-gray-600 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          } transition-colors`}
        >
          {loading ? `${mode === 'enhance' ? 'Enhancing' : 'Colorizing'}...` : `${mode === 'enhance' ? 'Enhance' : 'Colorize'} Image`}
        </button>

        {error && (
          <div className="mt-4 p-4 bg-red-500/20 border border-red-500 rounded">
            <p className="text-red-100 mb-2">{error}</p>
            <button
              onClick={handleRetry}
              className="text-sm text-red-100 hover:text-white underline"
            >
              Try Again
            </button>
          </div>
        )}

        {enhancedImage && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Results</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-400 mb-2">Original</p>
                <div className="relative aspect-square">
                  <img
                    src={URL.createObjectURL(image)}
                    alt="Original"
                    className="w-full h-full object-contain rounded shadow-lg"
                  />
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-400 mb-2">
                  {mode === 'enhance' ? 'Enhanced' : 'Colorized'}
                </p>
                <div className="relative aspect-square">
                  <img
                    src={enhancedImage}
                    alt={mode === 'enhance' ? 'Enhanced' : 'Colorized'}
                    className="w-full h-full object-contain rounded shadow-lg"
                  />
                  <a
                    href={`${enhancedImage}?download=true`}
                    download
                    className="absolute bottom-4 right-4 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-full shadow-lg flex items-center space-x-2 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                    <span>Download</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
