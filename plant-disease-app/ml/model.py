"""
EfficientNet-B0 model architecture for plant disease classification.
"""
import torch
import torch.nn as nn
from torchvision import models


class PlantDiseaseModel(nn.Module):
    """
    EfficientNet-B0 based model for plant disease classification.
    Supports transfer learning with freeze/unfreeze capabilities.
    """
    
    def __init__(self, num_classes: int = 38, pretrained: bool = True):
        """
        Initialize the plant disease model.
        
        Args:
            num_classes: Number of disease classes to predict
            pretrained: Whether to use pretrained ImageNet weights
        """
        super(PlantDiseaseModel, self).__init__()
        
        self.num_classes = num_classes
        
        # Load pretrained EfficientNet-B0
        self.backbone = models.efficientnet_b0(pretrained=pretrained)
        
        # Get the number of input features for the classifier
        in_features = self.backbone.classifier[1].in_features
        
        # Replace the classifier with custom head
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.2, inplace=True),
            nn.Linear(in_features, num_classes)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the model.
        
        Args:
            x: Input tensor of shape (batch_size, 3, 224, 224)
            
        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        return self.backbone(x)
    
    def freeze_backbone(self):
        """
        Freeze the backbone (feature extractor) weights.
        Only the classifier head will be trainable.
        """
        for param in self.backbone.features.parameters():
            param.requires_grad = False
        
        # Ensure classifier is trainable
        for param in self.backbone.classifier.parameters():
            param.requires_grad = True
        
        print("Backbone frozen. Only classifier is trainable.")
    
    def unfreeze_backbone(self):
        """
        Unfreeze the backbone weights for fine-tuning.
        All model parameters will be trainable.
        """
        for param in self.backbone.parameters():
            param.requires_grad = True
        
        print("Backbone unfrozen. All parameters are trainable.")
    
    def get_trainable_params(self):
        """
        Get list of trainable parameters.
        
        Returns:
            List of trainable parameters
        """
        return [p for p in self.parameters() if p.requires_grad]
    
    def count_parameters(self) -> dict:
        """
        Count model parameters.
        
        Returns:
            Dictionary with total, trainable, and frozen parameter counts
        """
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        frozen_params = total_params - trainable_params
        
        return {
            "total": total_params,
            "trainable": trainable_params,
            "frozen": frozen_params,
        }


def create_model(num_classes: int = 38, pretrained: bool = True, freeze_backbone: bool = False) -> PlantDiseaseModel:
    """
    Factory function to create a PlantDiseaseModel.
    
    Args:
        num_classes: Number of disease classes
        pretrained: Whether to use pretrained weights
        freeze_backbone: Whether to freeze the backbone initially
        
    Returns:
        Initialized PlantDiseaseModel
    """
    model = PlantDiseaseModel(num_classes=num_classes, pretrained=pretrained)
    
    if freeze_backbone:
        model.freeze_backbone()
    
    return model


if __name__ == "__main__":
    # Test model creation
    model = create_model(num_classes=38, pretrained=True)
    
    # Print model info
    param_counts = model.count_parameters()
    print(f"\nModel Information:")
    print(f"Total parameters: {param_counts['total']:,}")
    print(f"Trainable parameters: {param_counts['trainable']:,}")
    print(f"Frozen parameters: {param_counts['frozen']:,}")
    
    # Test forward pass
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    print(f"\nInput shape: {dummy_input.shape}")
    print(f"Output shape: {output.shape}")
