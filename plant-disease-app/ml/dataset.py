"""
Dataset utilities for PlantVillage dataset.
Includes data loading, augmentation, and preprocessing.
"""
import os
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image
from typing import Tuple, Optional, List
import glob


class PlantVillageDataset(Dataset):
    """
    Custom dataset class for PlantVillage dataset.
    Expects directory structure: data_dir/class_name/image.jpg
    """
    
    def __init__(self, data_dir: str, transform: Optional[transforms.Compose] = None):
        """
        Initialize the dataset.
        
        Args:
            data_dir: Root directory containing class folders
            transform: Optional transforms to apply to images
        """
        self.data_dir = data_dir
        self.transform = transform
        
        # Collect all image paths and labels
        self.images = []
        self.labels = []
        self.class_names = []
        
        if os.path.exists(data_dir):
            self._load_dataset()
        else:
            print(f"Warning: Data directory {data_dir} does not exist")
    
    def _load_dataset(self):
        """Load all images and create class mappings."""
        # Get all class directories
        class_dirs = sorted([d for d in os.listdir(self.data_dir) 
                           if os.path.isdir(os.path.join(self.data_dir, d))])
        
        self.class_names = class_dirs
        self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(class_dirs)}
        
        # Collect all images
        for class_name in class_dirs:
            class_dir = os.path.join(self.data_dir, class_name)
            image_files = glob.glob(os.path.join(class_dir, "*.jpg")) + \
                         glob.glob(os.path.join(class_dir, "*.jpeg")) + \
                         glob.glob(os.path.join(class_dir, "*.png"))
            
            for img_path in image_files:
                self.images.append(img_path)
                self.labels.append(self.class_to_idx[class_name])
        
        print(f"Loaded {len(self.images)} images from {len(self.class_names)} classes")
    
    def __len__(self) -> int:
        """Return the number of images in the dataset."""
        return len(self.images)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """
        Get a single item from the dataset.
        
        Args:
            idx: Index of the item
            
        Returns:
            Tuple of (image_tensor, label)
        """
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # Load image
        image = Image.open(img_path).convert('RGB')
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        return image, label
    
    def get_class_names(self) -> List[str]:
        """Get list of class names."""
        return self.class_names


def get_train_transforms() -> transforms.Compose:
    """
    Get training data augmentation transforms.
    
    Returns:
        Composed transforms for training
    """
    return transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomCrop((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def get_val_transforms() -> transforms.Compose:
    """
    Get validation/test data transforms (no augmentation).
    
    Returns:
        Composed transforms for validation
    """
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def create_data_loaders(
    data_dir: str,
    batch_size: int = 32,
    val_split: float = 0.2,
    num_workers: int = 4,
    seed: int = 42
) -> Tuple[DataLoader, DataLoader]:
    """
    Create train and validation data loaders.
    
    Args:
        data_dir: Root directory containing class folders
        batch_size: Batch size for data loaders
        val_split: Fraction of data to use for validation
        num_workers: Number of worker processes for data loading
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (train_loader, val_loader)
    """
    # Create datasets with appropriate transforms
    train_dataset_full = PlantVillageDataset(data_dir, transform=get_train_transforms())
    
    # Calculate split sizes
    dataset_size = len(train_dataset_full)
    val_size = int(dataset_size * val_split)
    train_size = dataset_size - val_size
    
    # Split dataset
    generator = torch.Generator().manual_seed(seed)
    train_dataset, val_dataset_temp = random_split(
        train_dataset_full, 
        [train_size, val_size],
        generator=generator
    )
    
    # Create validation dataset with validation transforms
    val_dataset = PlantVillageDataset(data_dir, transform=get_val_transforms())
    # Use the same indices as val_dataset_temp
    val_dataset.images = [train_dataset_full.images[i] for i in val_dataset_temp.indices]
    val_dataset.labels = [train_dataset_full.labels[i] for i in val_dataset_temp.indices]
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    print(f"Train dataset: {len(train_dataset)} images")
    print(f"Validation dataset: {len(val_dataset)} images")
    
    return train_loader, val_loader


if __name__ == "__main__":
    # Test dataset loading
    data_dir = "../data/plantvillage"  # Adjust path as needed
    
    if os.path.exists(data_dir):
        train_loader, val_loader = create_data_loaders(
            data_dir=data_dir,
            batch_size=16,
            val_split=0.2
        )
        
        # Test loading a batch
        images, labels = next(iter(train_loader))
        print(f"\nBatch shape: {images.shape}")
        print(f"Labels shape: {labels.shape}")
        print(f"Labels: {labels[:5]}")
    else:
        print(f"Data directory {data_dir} not found")
