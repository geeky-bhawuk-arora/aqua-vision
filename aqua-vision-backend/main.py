import time
import base64
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Initialize FastAPI Application
app = FastAPI(title="AquaVision Backend API")

# 2. Configure CORS Middleware (Essential for connecting React Frontend on port 5173)
origins = [
    "http://localhost:5173",  # Your frontend development server
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define Response Data Structure
class EnhancedImageResponse(BaseModel):
    success: bool
    enhanced_image: str  # Base64 encoded image string
    processing_time: str
    confidence: float

# 4. Core AI Pipeline Function (The Integration Point)
def process_and_enhance_image(image_bytes: bytes, original_mime_type: str) -> tuple[str, str, float]:
    """
    Simulates the full Data Pipeline Layer (Preprocessing) and Model Serving Layer (Inference).
    """
    start_time = time.time()
    
    # --- 💠 1. Data Pipeline Layer (Preprocessing) ---
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    # Placeholder for Preprocessing:
    # 💡 REPLACE HERE: Apply image enhancement (CLAHE, White Balance Correction)
    # image_enhanced = apply_clahe(image_cv) 
    image_processed = image_cv # For demo, no change
    
    # Resize and normalize for model input
    # target_size = (224, 224) 
    # model_input = cv2.resize(image_processed, target_size)

    # --- 🔹 2. Model Serving Layer (Inference) ---
    # Placeholder for Model Loading (Only load once, outside this function in production)
    # model = load_model_from_onnx_or_pt('your_model_path.onnx')
    
    # Placeholder for Inference:
    # 💡 REPLACE HERE: Run model prediction
    # model_output = model.predict(model_input)
    # confidence_score = float(model_output['confidence']) 
    
    # MOCK LOGIC for demo:
    enhanced_image_cv = image_processed
    confidence_score = 0.94 # Mock confidence

    # --- 🔹 3. Prepare Final Output ---
    
    # Convert enhanced OpenCV image back to bytes for Base64 encoding
    success, buffer = cv2.imencode('.png', enhanced_image_cv)
    if not success:
        raise Exception("Could not encode enhanced image.")
    
    enhanced_image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    processing_time = f"{(time.time() - start_time):.2f}s"

    return enhanced_image_base64, processing_time, confidence_score

# 5. Define the Enhancement Endpoint
@app.post("/api/enhance-image", response_model=EnhancedImageResponse)
async def enhance_image_endpoint(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")
    
    # We pass the MIME type to properly format the data URI on the backend
    mime_type = file.content_type

    try:
        image_bytes = await file.read()
        
        # Call the main processing pipeline
        enhanced_base64, proc_time, confidence = process_and_enhance_image(image_bytes, mime_type)

        # The 'enhanced_image' needs the data URI prefix for the frontend's <img> tag
        data_uri_prefix = f"data:{mime_type};base64,"
        
        # Returns structured data expected by the frontend (UploadPage.jsx)
        return EnhancedImageResponse(
            success=True,
            enhanced_image=data_uri_prefix + enhanced_base64,
            processing_time=proc_time,
            confidence=confidence
        )

    except Exception as e:
        print(f"Enhancement error: {e}")
        # The frontend uses this failure to trigger its demo fallback
        raise HTTPException(status_code=500, detail="AI Processing pipeline failed.")

# 6. Run command for the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)