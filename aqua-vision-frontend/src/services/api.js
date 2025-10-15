// Example: src/services/api.js

const API_BASE_URL = 'http://localhost:8000/api'; // <--- Ensure this matches your FastAPI server (e.g., port 8000)

export const enhanceImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file); // 'file' must match the parameter name in main.py's endpoint

    const response = await fetch(`${API_BASE_URL}/enhance-image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      // Handle HTTP errors (e.g., 400 Bad Request, 500 Internal Server Error)
      const errorData = await response.json();
      console.error('API Error:', errorData.detail);
      // The frontend fallback handles the 'false' success case, so we return it.
      return { success: false, error: errorData.detail || 'Server error' };
    }

    const data = await response.json();
    return { success: true, data: data };

  } catch (error) {
    console.error('Network or Fetch Error:', error);
    // Return success: false to trigger the demo fallback in UploadPage.jsx
    return { success: false, error: 'Network connection failed' };
  }
};