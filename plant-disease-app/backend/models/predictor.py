"""
Plant disease prediction model using EfficientNet-B0.
"""
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os
from typing import List, Tuple, Optional


class PlantDiseasePredictor:
    """
    Plant disease prediction class using EfficientNet-B0 model.
    Supports 38 PlantVillage disease classes.
    """
    
    # 38 PlantVillage disease classes
    DISEASE_CLASSES = [
        "Apple___Apple_scab",
        "Apple___Black_rot",
        "Apple___Cedar_apple_rust",
        "Apple___healthy",
        "Blueberry___healthy",
        "Cherry_(including_sour)___Powdery_mildew",
        "Cherry_(including_sour)___healthy",
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Corn_(maize)___Common_rust_",
        "Corn_(maize)___Northern_Leaf_Blight",
        "Corn_(maize)___healthy",
        "Grape___Black_rot",
        "Grape___Esca_(Black_Measles)",
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "Grape___healthy",
        "Orange___Haunglongbing_(Citrus_greening)",
        "Peach___Bacterial_spot",
        "Peach___healthy",
        "Pepper,_bell___Bacterial_spot",
        "Pepper,_bell___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
        "Raspberry___healthy",
        "Soybean___healthy",
        "Squash___Powdery_mildew",
        "Strawberry___Leaf_scorch",
        "Strawberry___healthy",
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Spider_mites Two-spotted_spider_mite",
        "Tomato___Target_Spot",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___healthy"
    ]
    
    def __init__(self, model_path: Optional[str] = None, device: str = "cpu"):
        """
        Initialize the plant disease predictor.
        
        Args:
            model_path: Path to trained model weights (.pth file)
            device: Device to run inference on ('cpu' or 'cuda')
        """
        self.device = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
        self.num_classes = len(self.DISEASE_CLASSES)
        
        # Initialize model
        self.model = self._build_model()
        
        # Load weights if provided
        if model_path and os.path.exists(model_path):
            self._load_weights(model_path)
        
        self.model.to(self.device)
        self.model.eval()
        
        # Define preprocessing transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def _build_model(self) -> nn.Module:
        """
        Build EfficientNet-B0 model for plant disease classification.
        
        Returns:
            EfficientNet-B0 model with modified classifier
        """
        # Load pretrained EfficientNet-B0
        model = models.efficientnet_b0(pretrained=True)
        
        # Modify the classifier for our number of classes
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, self.num_classes)
        
        return model
    
    def _load_weights(self, model_path: str):
        """
        Load model weights from file.
        
        Args:
            model_path: Path to model weights file
        """
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
            else:
                self.model.load_state_dict(checkpoint)
            print(f"Successfully loaded model weights from {model_path}")
        except Exception as e:
            print(f"Warning: Could not load model weights from {model_path}: {e}")
            print("Using randomly initialized weights")
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess image for model input.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image tensor
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transforms
        image_tensor = self.transform(image)
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
    
    def predict(self, image: Image.Image, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Predict plant disease from image.
        
        Args:
            image: PIL Image object
            top_k: Number of top predictions to return
            
        Returns:
            List of tuples (disease_name, confidence_score) for top-k predictions
        """
        # Preprocess image
        image_tensor = self.preprocess_image(image)
        image_tensor = image_tensor.to(self.device)
        
        # Run inference
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
        
        # Get top-k predictions
        top_probs, top_indices = torch.topk(probabilities, k=min(top_k, self.num_classes), dim=1)
        
        # Convert to list of (disease_name, confidence)
        predictions = []
        for prob, idx in zip(top_probs[0], top_indices[0]):
            disease_name = self.DISEASE_CLASSES[idx.item()]
            # Format disease name (replace underscores with spaces, clean up)
            disease_name = disease_name.replace('___', ' - ').replace('_', ' ')
            predictions.append((disease_name, prob.item()))
        
        return predictions
    
    def get_disease_classes(self) -> List[str]:
        """
        Get list of all supported disease classes.
        
        Returns:
            List of disease class names
        """
        return [name.replace('___', ' - ').replace('_', ' ') for name in self.DISEASE_CLASSES]
    
    def get_crops(self) -> List[str]:
        """
        Get list of supported crops.
        
        Returns:
            List of unique crop names
        """
        crops = set()
        for disease_class in self.DISEASE_CLASSES:
            crop = disease_class.split('___')[0].replace('_', ' ')
            crops.add(crop)
        return sorted(list(crops))
