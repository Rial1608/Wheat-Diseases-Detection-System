import numpy as np
import cv2
from scipy import ndimage


def estimate_infection_severity(heatmap, disease_class, threshold=0.3):
    """
    Estimate the infection percentage based on Grad-CAM heatmap.
    
    Args:
        heatmap: 2D numpy array representing the Grad-CAM heatmap
        disease_class: String representing the predicted disease class
        threshold: Float between 0 and 1 for heatmap thresholding
    
    Returns:
        Tuple of (severity_percentage, severity_level)
    """
    
    # If the disease is healthy, return 0% infection
    if disease_class.lower() == 'healthy':
        return 0, 'Healthy'
    
    # Normalize heatmap to 0-1 range if needed
    if heatmap.max() == heatmap.min():
        heatmap_normalized = np.zeros_like(heatmap)
    else:
        heatmap_normalized = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
    
    # Apply threshold to identify infected regions
    infected_mask = heatmap_normalized > threshold
    
    # Calculate infection percentage
    total_pixels = heatmap_normalized.size
    infected_pixels = np.sum(infected_mask)
    
    infection_percentage = (infected_pixels / total_pixels) * 100
    
    # Classify severity level
    if infection_percentage < 10:
        severity_level = 'Trace'
    elif infection_percentage < 20:
        severity_level = 'Low Infection'
    elif infection_percentage < 50:
        severity_level = 'Moderate Infection'
    else:
        severity_level = 'Severe Infection'
    
    return round(infection_percentage, 1), severity_level


def calculate_connected_components(heatmap, threshold=0.3):
    """
    Calculate connected components in the heatmap to identify disease regions.
    
    Args:
        heatmap: 2D numpy array
        threshold: Threshold value for binary segmentation
    
    Returns:
        Tuple of (num_components, component_areas)
    """
    
    # Normalize heatmap
    if heatmap.max() == heatmap.min():
        heatmap_normalized = np.zeros_like(heatmap)
    else:
        heatmap_normalized = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
    
    # Create binary mask
    binary_mask = (heatmap_normalized > threshold).astype(np.uint8)
    
    # Label connected components
    labeled_array, num_features = ndimage.label(binary_mask)
    
    # Calculate area of each component
    component_areas = ndimage.sum(binary_mask, labeled_array, range(num_features + 1))
    
    return num_features, component_areas


def color_severity_level(severity_percentage, severity_level):
    """
    Assign a color code based on severity level for visualization.
    
    Args:
        severity_percentage: Float representing infection percentage
        severity_level: String representing severity level
    
    Returns:
        String representing color code
    """
    
    color_map = {
        'Healthy': '#28a745',  # Green
        'Trace': '#ffc107',  # Amber
        'Low Infection': '#fd7e14',  # Orange
        'Moderate Infection': '#fd7e14',  # Orange
        'Severe Infection': '#dc3545'  # Red
    }
    
    return color_map.get(severity_level, '#6c757d')  # Default gray


def estimate_confidence_by_severity(confidence, severity_percentage):
    """
    Adjust confidence score based on severity estimation.
    
    This provides a more nuanced view of the model's certainty.
    
    Args:
        confidence: Float between 0 and 1 (model prediction confidence)
        severity_percentage: Float representing infection percentage
    
    Returns:
        Dictionary with adjusted metrics
    """
    
    # If very low infection but high confidence, reduce certainty slightly
    if severity_percentage < 20 and confidence > 0.85:
        adjusted_confidence = confidence * 0.95
    # If high infection and high confidence, boost it slightly
    elif severity_percentage > 50 and confidence > 0.70:
        adjusted_confidence = confidence * 1.05
    else:
        adjusted_confidence = confidence
    
    # Clamp to [0, 1]
    adjusted_confidence = min(1.0, max(0.0, adjusted_confidence))
    
    return {
        'original_confidence': confidence,
        'adjusted_confidence': adjusted_confidence,
        'severity_adjusted': adjusted_confidence != confidence
    }
