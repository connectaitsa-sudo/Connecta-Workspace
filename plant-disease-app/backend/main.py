"""
FastAPI application for Plant Disease Diagnosis and Treatment Recommendation.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from typing import List

from models import PlantDiseasePredictor
from database import TreatmentKnowledgeBase
from schemas import (
    HealthResponse,
    PredictionResponse,
    PredictionResult,
    TreatmentResponse,
    CropListResponse,
    CropInfo,
    DiseaseListResponse,
    DiseaseInfo,
)

# Initialize FastAPI app
app = FastAPI(
    title="Plant Disease Diagnosis & Treatment API",
    description="AI-powered plant disease detection and treatment recommendation system",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model and knowledge base
predictor = PlantDiseasePredictor(device="cpu")
knowledge_base = TreatmentKnowledgeBase()


@app.get("/", response_model=dict)
async def root():
    """
    Root endpoint - API information.
    
    Returns:
        API information and available endpoints
    """
    return {
        "name": "Plant Disease Diagnosis & Treatment API",
        "version": "1.0.0",
        "description": "AI-powered plant disease detection and treatment recommendations",
        "endpoints": {
            "health": "GET /health - Health check",
            "predict": "POST /predict - Upload image for disease prediction",
            "treatments": "GET /treatments/{disease_name} - Get treatment recommendations",
            "crops": "GET /crops - List supported crops",
            "diseases": "GET /diseases - List all detectable diseases",
        },
        "documentation": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        API health status
    """
    return HealthResponse(
        status="healthy",
        message="Plant Disease Diagnosis API is running"
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)):
    """
    Predict plant disease from uploaded image.
    
    Args:
        file: Uploaded image file
        
    Returns:
        Top-3 disease predictions with confidence scores
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get predictions
        predictions = predictor.predict(image, top_k=3)
        
        # Format response
        prediction_results = [
            PredictionResult(disease=disease, confidence=confidence)
            for disease, confidence in predictions
        ]
        
        return PredictionResponse(
            success=True,
            predictions=prediction_results,
            message="Prediction successful"
        )
        
    except Exception as e:
        return PredictionResponse(
            success=False,
            predictions=[],
            message=f"Error processing image: {str(e)}"
        )


@app.get("/treatments/{disease_name}", response_model=TreatmentResponse)
async def get_treatment(disease_name: str):
    """
    Get treatment recommendations for a specific disease.
    
    Args:
        disease_name: Name of the disease
        
    Returns:
        Treatment recommendations including cultural, biological, and chemical controls
    """
    treatment = knowledge_base.get_treatment(disease_name)
    
    if not treatment:
        raise HTTPException(
            status_code=404,
            detail=f"Treatment information for '{disease_name}' not found"
        )
    
    return TreatmentResponse(**treatment)


@app.get("/crops", response_model=CropListResponse)
async def list_crops():
    """
    List all supported crops with their detectable diseases.
    
    Returns:
        List of crops and their diseases
    """
    # Get all disease classes from predictor
    disease_classes = predictor.DISEASE_CLASSES
    
    # Group diseases by crop
    crop_diseases = {}
    for disease_class in disease_classes:
        parts = disease_class.split('___')
        crop = parts[0].replace('_', ' ')
        disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
        
        if crop not in crop_diseases:
            crop_diseases[crop] = []
        crop_diseases[crop].append(disease)
    
    # Create response
    crops = [
        CropInfo(crop_name=crop, diseases=diseases)
        for crop, diseases in sorted(crop_diseases.items())
    ]
    
    return CropListResponse(crops=crops)


@app.get("/diseases", response_model=DiseaseListResponse)
async def list_diseases():
    """
    List all detectable diseases.
    
    Returns:
        List of all diseases with crop information
    """
    disease_classes = predictor.DISEASE_CLASSES
    
    diseases = []
    for disease_class in disease_classes:
        parts = disease_class.split('___')
        crop = parts[0].replace('_', ' ')
        disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
        
        diseases.append(
            DiseaseInfo(
                disease_name=disease,
                crop=crop
            )
        )
    
    return DiseaseListResponse(
        diseases=diseases,
        total=len(diseases)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
