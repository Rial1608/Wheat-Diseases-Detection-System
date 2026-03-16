import os
os.environ['MPLBACKEND'] = 'Agg'  # Use non-interactive backend

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
from PIL import Image


def save_heatmap_visualization(original_image, heatmap, disease_class, confidence, output_path):
    """
    Save heatmap visualization with original image and overlayed heatmap.
    Falls back to simple overlay if matplotlib fails.
    """
    try:
        # Normalize heatmap to 0-255
        if len(heatmap.shape) == 2:
            heatmap_2d = heatmap
        else:
            heatmap_2d = heatmap[:, :, 0]
        
        # Resize heatmap to match original image
        heatmap_resized = cv2.resize(heatmap_2d, (original_image.shape[1], original_image.shape[0]))
        heatmap_normalized = np.uint8(255 * (heatmap_resized - heatmap_resized.min()) / (heatmap_resized.max() - heatmap_resized.min() + 1e-8))
        
        # Apply color map to heatmap
        heatmap_colored = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)
        
        # Create overlay
        alpha = 0.5
        overlayed = cv2.addWeighted(original_image, 1 - alpha, heatmap_colored, alpha, 0)
        
        # Try matplotlib visualization first
        try:
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            axes[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            axes[0].set_title('Original Image')
            axes[0].axis('off')
            
            axes[1].imshow(heatmap_resized, cmap='jet')
            axes[1].set_title('Grad-CAM Heatmap')
            axes[1].axis('off')
            
            axes[2].imshow(cv2.cvtColor(overlayed, cv2.COLOR_BGR2RGB))
            axes[2].set_title(f'Prediction: {disease_class} ({confidence:.1%})')
            axes[2].axis('off')
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            print(f"✓ Heatmap saved successfully to {output_path}")
            return overlayed
        
        except Exception as plt_error:
            print(f"⚠ Matplotlib visualization failed: {plt_error}")
            print(f"  Falling back to simple overlay image...")
            
            # Fallback: Save as simple overlay image using OpenCV
            cv2.imwrite(output_path, overlayed)
            print(f"✓ Fallback heatmap saved successfully to {output_path}")
            return overlayed
    
    except Exception as e:
        print(f"✗ Heatmap visualization failed: {e}")
        print(f"  Output path attempted: {output_path}")
        raise


def overlay_heatmap(image_path, heatmap, output_path, alpha=0.4):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    heatmap_resized = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
    heatmap_normalized = np.uint8(255 * heatmap_resized)
    
    heatmap_colored = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    overlayed = cv2.addWeighted(original_image, 1 - alpha, heatmap_colored, alpha, 0)
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.imshow(original_image)
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(heatmap_resized, cmap='jet')
    plt.title('Grad-CAM Heatmap')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(overlayed)
    plt.title('Overlayed Heatmap')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()
    
    return overlayed
