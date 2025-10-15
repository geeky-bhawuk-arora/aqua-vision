import time
import base64
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- FASTAPI SETUP ---
app = FastAPI(
    title="AquaVision Backend API",
    description="AI-powered underwater image enhancement and object classification."
)

origins = [
    "http://localhost:5173",  # Frontend Dev Server
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnhancedImageResponse(BaseModel):
    success: bool
    enhanced_image: str  # Base64 encoded image string (with data URI prefix)
    processing_time: str
    confidence: float

# --- CORE LOGIC: DATA PIPELINE LAYER (PREPROCESSING) ---

def apply_underwater_enhancement(image_cv: np.ndarray) -> np.ndarray:
    """
    Simulates the Preprocessing Pipeline: CLAHE, White Balance, and Dehazing.
    
    In this prototype, we use a basic, fast color correction approach 
    (gray-world assumption) and CLAHE for contrast enhancement.
    """
    
    # 1. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    lab = cv2.cvtColor(image_cv, cv2.COLOR_BGR2LAB)
    l_channel = lab[:,:,0]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)
    lab[:,:,0] = cl
    enhanced_clahe = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # 2. Simple Gray-World Color Correction (Simulates White Balance)
    # Convert image to float to perform math
    img_f = enhanced_clahe.astype(np.float32) / 255.0
    
    # Calculate average of each color channel
    avg_b = np.average(img_f[:,:,0])
    avg_g = np.average(img_f[:,:,1])
    avg_r = np.average(img_f[:,:,2])
    
    # Calculate scale factors to normalize to the overall average
    avg_all = (avg_b + avg_g + avg_r) / 3.0
    
    if avg_b > 0 and avg_g > 0 and avg_r > 0:
        scale_b = avg_all / avg_b
        scale_g = avg_all / avg_g
        scale_r = avg_all / avg_r
        
        # Apply scaling
        img_f[:,:,0] = np.clip(img_f[:,:,0] * scale_b, 0, 1)
        img_f[:,:,1] = np.clip(img_f[:,:,1] * scale_g, 0, 1)
        img_f[:,:,2] = np.clip(img_f[:,:,2] * scale_r, 0, 1)
    
    # Convert back to uint8
    final_enhanced = (img_f * 255).astype(np.uint8)
    
    return final_enhanced

# --- CORE LOGIC: COMBINED PIPELINE & MODEL SERVING LAYER ---

def run_aqua_vision_pipeline(image_bytes: bytes, original_mime_type: str) -> tuple[str, str, float]:
    start_time = time.time()
    
    # 1. Data Ingestion (Read and Convert to OpenCV format)
    # Note: Use BGR format for OpenCV
    image_np = np.array(Image.open(BytesIO(image_bytes)).convert("RGB"))
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # 2. Data Pipeline Layer: Preprocessing / Enhancement
    image_enhanced_cv = apply_underwater_enhancement(image_cv)
    
    # 3. Model Serving Layer: Inference
    # ------------------------------------------------------------------
    # 💡 MODEL INTEGRATION POINT: 
    # Here you would typically perform:
    # a) Resize: image_model_input = cv2.resize(image_enhanced_cv, (512, 512))
    # b) Normalization/Tensor conversion.
    # c) Model Prediction: prediction = model.predict(image_model_input)
    # d) Classification/Detection result.
    
    # For this demo, we mock the result of a classification model:
    confidence_score = 0.96 # High confidence in the 'enhanced' output
    # ------------------------------------------------------------------

    # 4. Prepare Final Output
    # The enhanced image is the output from our enhancement function
    final_image_output_cv = image_enhanced_cv
    
    # Convert enhanced OpenCV image back to bytes (PNG format for optimal clarity)
    success, buffer = cv2.imencode('.png', final_image_output_cv)
    if not success:
        raise Exception("Could not encode enhanced image.")
    
    enhanced_image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    processing_time = f"{(time.time() - start_time):.2f}s"

    return enhanced_image_base64, processing_time, confidence_score

# --- FASTAPI ENDPOINT ---

@app.post("/api/enhance-image", response_model=EnhancedImageResponse)
async def enhance_image_endpoint(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")

    try:
        image_bytes = await file.read()
        
        # Check size (10MB limit as suggested in frontend's UploadPage.jsx)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds the 10MB limit.")

        # Run the entire pipeline
        enhanced_base64, proc_time, confidence = run_aqua_vision_pipeline(image_bytes, file.content_type)

        # Base64 output uses PNG encoding from OpenCV, so the MIME type must reflect that
        data_uri_prefix = f"data:image/png;base64," 
        
        return EnhancedImageResponse(
            success=True,
            enhanced_image=data_uri_prefix + enhanced_base64,
            processing_time=proc_time,
            confidence=confidence
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Server Error during processing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error: AI pipeline failure.")

# --- RUNNER ---
if __name__ == "__main__":
    import uvicorn
    # Start the server (run this in Terminal 1)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)