"""
Pydantic schemas for API request/response models.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="API health status")
    message: str = Field(..., description="Status message")


class PredictionResult(BaseModel):
    """Single prediction result with disease name and confidence."""
    disease: str = Field(..., description="Predicted disease name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class PredictionResponse(BaseModel):
    """Disease prediction response with top predictions."""
    success: bool = Field(..., description="Whether prediction was successful")
    predictions: List[PredictionResult] = Field(..., description="Top disease predictions")
    message: Optional[str] = Field(None, description="Optional message or error")


class TreatmentControl(BaseModel):
    """Treatment control measures."""
    cultural_controls: List[str] = Field(default_factory=list, description="Cultural control methods")
    biological_controls: List[str] = Field(default_factory=list, description="Biological control methods")
    chemical_controls: List[str] = Field(default_factory=list, description="Chemical control methods")


class TreatmentResponse(BaseModel):
    """Treatment recommendation response."""
    disease_name: str = Field(..., description="Disease name")
    crop: str = Field(..., description="Affected crop")
    summary: str = Field(..., description="Disease summary")
    symptoms: List[str] = Field(default_factory=list, description="Disease symptoms")
    cultural_controls: List[str] = Field(default_factory=list, description="Cultural control methods")
    biological_controls: List[str] = Field(default_factory=list, description="Biological control methods")
    chemical_controls: List[str] = Field(default_factory=list, description="Chemical control methods")
    prevention: List[str] = Field(default_factory=list, description="Prevention measures")
    severity: str = Field(..., description="Disease severity level")


class CropInfo(BaseModel):
    """Crop information with supported diseases."""
    crop_name: str = Field(..., description="Crop name")
    diseases: List[str] = Field(..., description="List of detectable diseases")


class CropListResponse(BaseModel):
    """Response with list of supported crops."""
    crops: List[CropInfo] = Field(..., description="List of supported crops")


class DiseaseInfo(BaseModel):
    """Disease information."""
    disease_name: str = Field(..., description="Disease name")
    crop: str = Field(..., description="Affected crop")


class DiseaseListResponse(BaseModel):
    """Response with list of all detectable diseases."""
    diseases: List[DiseaseInfo] = Field(..., description="List of all diseases")
    total: int = Field(..., description="Total number of diseases")
