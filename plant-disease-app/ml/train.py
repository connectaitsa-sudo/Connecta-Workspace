"""
Training script for plant disease classification model.
"""
import argparse
import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from model import create_model
from dataset import create_data_loaders


def train_epoch(model, train_loader, criterion, optimizer, device, epoch):
    """
    Train for one epoch.
    
    Args:
        model: Model to train
        train_loader: Training data loader
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on
        epoch: Current epoch number
        
    Returns:
        Average training loss and accuracy
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc=f"Epoch {epoch} - Training")
    
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        # Zero gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item() * images.size(0)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
        # Update progress bar
        pbar.set_postfix({
            'loss': f'{loss.item():.4f}',
            'acc': f'{100 * correct / total:.2f}%'
        })
    
    epoch_loss = running_loss / total
    epoch_acc = 100 * correct / total
    
    return epoch_loss, epoch_acc


def validate(model, val_loader, criterion, device, epoch):
    """
    Validate the model.
    
    Args:
        model: Model to validate
        val_loader: Validation data loader
        criterion: Loss function
        device: Device to validate on
        epoch: Current epoch number
        
    Returns:
        Average validation loss and accuracy
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(val_loader, desc=f"Epoch {epoch} - Validation")
    
    with torch.no_grad():
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Statistics
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            # Update progress bar
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100 * correct / total:.2f}%'
            })
    
    epoch_loss = running_loss / total
    epoch_acc = 100 * correct / total
    
    return epoch_loss, epoch_acc


def save_checkpoint(model, optimizer, epoch, best_acc, save_path):
    """
    Save model checkpoint.
    
    Args:
        model: Model to save
        optimizer: Optimizer state
        epoch: Current epoch
        best_acc: Best validation accuracy
        save_path: Path to save checkpoint
    """
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'best_acc': best_acc,
    }
    torch.save(checkpoint, save_path)
    print(f"Checkpoint saved to {save_path}")


def train(args):
    """
    Main training function.
    
    Args:
        args: Command line arguments
    """
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() and args.use_gpu else "cpu")
    print(f"Using device: {device}")
    
    # Create data loaders
    print("\nLoading data...")
    train_loader, val_loader = create_data_loaders(
        data_dir=args.data_dir,
        batch_size=args.batch_size,
        val_split=args.val_split,
        num_workers=args.num_workers
    )
    
    # Create model
    print("\nInitializing model...")
    model = create_model(
        num_classes=args.num_classes,
        pretrained=args.pretrained,
        freeze_backbone=args.freeze_backbone
    )
    model = model.to(device)
    
    # Print model info
    param_counts = model.count_parameters()
    print(f"Total parameters: {param_counts['total']:,}")
    print(f"Trainable parameters: {param_counts['trainable']:,}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.get_trainable_params(), lr=args.learning_rate)
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=3, verbose=True
    )
    
    # TensorBoard writer
    writer = SummaryWriter(log_dir=args.log_dir)
    
    # Training loop
    print("\nStarting training...")
    best_acc = 0.0
    
    for epoch in range(1, args.epochs + 1):
        print(f"\n{'='*60}")
        print(f"Epoch {epoch}/{args.epochs}")
        print(f"{'='*60}")
        
        # Train
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device, epoch
        )
        
        # Validate
        val_loss, val_acc = validate(
            model, val_loader, criterion, device, epoch
        )
        
        # Log to TensorBoard
        writer.add_scalar('Loss/train', train_loss, epoch)
        writer.add_scalar('Loss/val', val_loss, epoch)
        writer.add_scalar('Accuracy/train', train_acc, epoch)
        writer.add_scalar('Accuracy/val', val_acc, epoch)
        writer.add_scalar('Learning_rate', optimizer.param_groups[0]['lr'], epoch)
        
        # Print epoch summary
        print(f"\nEpoch {epoch} Summary:")
        print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        
        # Update learning rate
        scheduler.step(val_acc)
        
        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            save_path = os.path.join(args.save_dir, 'best_model.pth')
            save_checkpoint(model, optimizer, epoch, best_acc, save_path)
            print(f"New best accuracy: {best_acc:.2f}%")
        
        # Save checkpoint every N epochs
        if epoch % args.save_freq == 0:
            save_path = os.path.join(args.save_dir, f'checkpoint_epoch_{epoch}.pth')
            save_checkpoint(model, optimizer, epoch, best_acc, save_path)
    
    print(f"\nTraining completed! Best validation accuracy: {best_acc:.2f}%")
    writer.close()


def main():
    """Parse arguments and start training."""
    parser = argparse.ArgumentParser(description='Train plant disease classification model')
    
    # Data parameters
    parser.add_argument('--data_dir', type=str, default='../data/plantvillage',
                        help='Path to dataset directory')
    parser.add_argument('--num_classes', type=int, default=38,
                        help='Number of disease classes')
    parser.add_argument('--val_split', type=float, default=0.2,
                        help='Validation split ratio')
    
    # Model parameters
    parser.add_argument('--pretrained', action='store_true', default=True,
                        help='Use pretrained weights')
    parser.add_argument('--freeze_backbone', action='store_true',
                        help='Freeze backbone during training')
    
    # Training parameters
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Batch size for training')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                        help='Initial learning rate')
    parser.add_argument('--num_workers', type=int, default=4,
                        help='Number of data loading workers')
    
    # GPU settings
    parser.add_argument('--use_gpu', action='store_true', default=True,
                        help='Use GPU if available')
    
    # Checkpointing
    parser.add_argument('--save_dir', type=str, default='./checkpoints',
                        help='Directory to save model checkpoints')
    parser.add_argument('--save_freq', type=int, default=10,
                        help='Save checkpoint every N epochs')
    parser.add_argument('--log_dir', type=str, default='./logs',
                        help='Directory for TensorBoard logs')
    
    args = parser.parse_args()
    
    # Create directories
    os.makedirs(args.save_dir, exist_ok=True)
    os.makedirs(args.log_dir, exist_ok=True)
    
    # Start training
    train(args)


if __name__ == "__main__":
    main()
