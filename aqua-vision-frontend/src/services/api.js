const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Sends the uploaded image to the backend for AI enhancement.
 * @param {File} file The image file object.
 * @returns {Promise<{success: boolean, data?: object, error?: string}>}
 */
export const enhanceImage = async (file) => {
  try {
    const formData = new FormData();
    // 'file' here must match the parameter name (UploadFile) in your FastAPI endpoint
    formData.append('file', file); 

    const response = await fetch(`${API_BASE_URL}/enhance-image`, {
      method: 'POST',
      body: formData,
      // FastAPI/Fetch automatically handles Content-Type for FormData
    });

    // Check for HTTP errors (e.g., 400, 500)
    if (!response.ok) {
      const errorData = await response.json();
      console.error('API Error:', errorData.detail);
      return { success: false, error: errorData.detail || 'Server processing failed' };
    }

    const data = await response.json();
    return { success: true, data: data };

  } catch (error) {
    // Handle network errors (server not running, CORS issues)
    console.error('Network or Fetch Error:', error);
    return { success: false, error: 'Could not connect to the backend API' };
  }
};