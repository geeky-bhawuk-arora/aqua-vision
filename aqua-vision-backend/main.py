import time
import base64
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- ML/Image Processing Dependencies (Installation Required: pip install opencv-python Pillow)
# from PIL import Image
# import cv2
# import numpy as np

# 1. Initialize FastAPI Application
app = FastAPI(
    title="AquaVision Backend API",
    description="AI-powered underwater image enhancement and object classification."
)

# 2. Configure CORS Middleware
# IMPORTANT: This must match the port where your Vite frontend is running (default is 5173).
origins = [
    "http://localhost:5173",  # Your frontend development server
    "http://127.0.0.1:5173",
    # Add your production domain here when deploying
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define Response Data Structure for Frontend
class EnhancedImageResponse(BaseModel):
    success: bool
    enhanced_image: str  # Base64 encoded image string
    processing_time: str
    confidence: float

# 4. Mock/Placeholder AI Function (Replace with your actual ML code)
# You will integrate your Preprocessing Pipeline and Model Inference here.
# Note: The actual Image and OpenCV imports are commented out to run this mock,
# but they are necessary for the real implementation.
def process_and_enhance_image(image_bytes: bytes) -> tuple[str, str, float]:
    """
    Placeholder for the full AI enhancement pipeline.
    Replaces steps 1, 2, and 3 of the 'Core Data & AI Flow Summary'.
    """
    start_time = time.time()

    # --- Step 1: Image Ingestion and Preprocessing (OpenCV, CLAHE, etc.) ---
    # Convert bytes to a format suitable for OpenCV/Pillow
    # original_image = Image.open(BytesIO(image_bytes))
    
    # --------------------------------------------------------------------------
    # 💡 REPLACE THIS SECTION with your actual ML pipeline integration:
    # 1. Apply image enhancement (CLAHE, White Balance)
    # 2. Resize and normalize image for model input
    # 3. Perform model inference (ResNet50/ViT)
    # 4. Get the classified/detected output image.
    
    # MOCK LOGIC: For the mock, we'll just return the original image
    # and encode it as the 'enhanced' image to test the frontend flow.
    # We will use the original bytes and base64 encode them.
    enhanced_image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # MOCK METADATA: Use values similar to the frontend's demo fallback
    processing_time = f"{(time.time() - start_time):.2f}s"
    confidence_score = 0.94
    # --------------------------------------------------------------------------

    return enhanced_image_base64, processing_time, confidence_score

# 5. Define the Enhancement Endpoint
@app.post("/api/enhance-image", response_model=EnhancedImageResponse)
async def enhance_image_endpoint(file: UploadFile = File(...)):
    """
    Handles file upload, processes the image using the AI model, and returns
    the enhanced image and metadata to the frontend.
    """
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")

    try:
        # Read the file content
        image_bytes = await file.read()

        # Check file size (optional, but good practice)
        if len(image_bytes) > 10 * 1024 * 1024: # 10MB limit as suggested in frontend
            raise HTTPException(status_code=400, detail="File size exceeds the 10MB limit.")

        # Process the image with the mock/real pipeline
        enhanced_base64, proc_time, confidence = process_and_enhance_image(image_bytes)

        # Construct the response for the frontend
        return EnhancedImageResponse(
            success=True,
            enhanced_image=f"data:{file.content_type};base64,{enhanced_base64}",
            processing_time=proc_time,
            confidence=confidence
        )

    except HTTPException as e:
        # Re-raise explicit HTTP exceptions
        raise e
    except Exception as e:
        # Log the error and return a generic server error
        print(f"Enhancement error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during image processing.")

# 6. Basic Health Check Endpoint
@app.get("/")
def health_check():
    return {"status": "ok", "service": "AquaVision API"}

# 7. How to run the application (Add this to the end of main.py)
if __name__ == "__main__":
    import uvicorn
    # To run: python main.py
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
    # Frontend should now call http://localhost:8000/api/enhance-image