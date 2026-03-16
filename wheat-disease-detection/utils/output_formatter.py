"""
Utility module for formatting prediction output and determining disease severity
"""

# Disease recommendation dictionary
DISEASE_RECOMMENDATIONS = {
    'Healthy': [
        'Status: Crop looks healthy',
        '* Continue regular monitoring',
        '* Maintain optimal irrigation',
        '* Monitor for early disease signs'
    ],
    'Brown_rust': [
        '* Apply fungicide (e.g., Tilt, Prosaro)',
        '* Remove infected leaves immediately',
        '* Improve air circulation in crop',
        '* Monitor field regularly for spread',
        '* Consider crop rotation next season'
    ],
    'Yellow_rust': [
        '* Apply rust-resistant fungicide',
        '* Monitor field conditions closely',
        '* Remove heavily infected plants',
        '* Improve drainage to reduce humidity',
        '* Consider resistant variety next season'
    ],
    'Leaf_rust': [
        '* Apply fungicide treatment immediately',
        '* Remove infected leaves',
        '* Reduce leaf wetness duration',
        '* Maintain proper crop spacing',
        '* Monitor closely for disease progression'
    ],
    'Stem_rust': [
        '* Immediate fungicide treatment recommended',
        '* Remove severely infected plants',
        '* Increase crop monitoring frequency',
        '* Ensure proper field sanitation',
        '* Apply preventive treatments to nearby plants'
    ],
    'Leaf Rust': [
        '* Apply fungicide treatment immediately',
        '* Remove infected leaves promptly',
        '* Reduce leaf wetness duration by improving air flow',
        '* Maintain proper crop spacing for ventilation',
        '* Monitor closely for disease progression'
    ],
    'Black Rust': [
        '* Apply suitable fungicide immediately',
        '* Remove infected leaves',
        '* Maintain crop spacing for air circulation',
        '* Monitor crop regularly for spread',
        '* Consider crop rotation next season'
    ]
}


def get_infection_severity(confidence, predicted_class):
    """
    Determine infection severity based on predicted disease class and confidence score.
    Returns "No Infection" immediately for healthy predictions.
    
    Args:
        confidence (float): Confidence score (0-1)
        predicted_class (str): The predicted disease class
        
    Returns:
        str: Severity level ("No Infection" for healthy, "Low Infection", "Moderate Infection", or "Severe Infection" for diseased)
    """
    # Check if the prediction is for a healthy plant
    healthy_labels = ['Healthy', 'healthy', 'No Disease', 'no disease']
    if predicted_class in healthy_labels:
        return "No Infection"
    
    # For diseased predictions, compute severity based on confidence
    confidence_pct = confidence * 100
    
    if confidence_pct < 40:
        return "Low Infection"
    elif confidence_pct < 70:
        return "Moderate Infection"
    else:
        return "Severe Infection"


def get_disease_recommendations(disease_class):
    """
    Get recommendations based on disease class.
    
    Args:
        disease_class (str): The predicted disease class
        
    Returns:
        list: List of recommendations
    """
    # Try exact match first, then with normalized version
    if disease_class in DISEASE_RECOMMENDATIONS:
        return DISEASE_RECOMMENDATIONS[disease_class]
    
    # Normalize class name (replace spaces with underscores)
    normalized_class = disease_class.replace(' ', '_')
    
    return DISEASE_RECOMMENDATIONS.get(
        normalized_class,
        DISEASE_RECOMMENDATIONS.get('Healthy', ['* No specific recommendations found'])
    )


def format_prediction_output(result, class_names):
    """
    Format prediction result into structured output.
    
    Args:
        result (dict): Prediction result from predict_disease()
        class_names (list): List of all class names
        
    Returns:
        str: Formatted output string
    """
    image_name = result.get('image', 'Unknown')
    predicted_class = result.get('predicted_class', 'Unknown')
    confidence = result.get('confidence', 0)
    all_predictions = result.get('all_predictions', [])
    output_path = result.get('output_path', '')
    
    # Get severity level (passing predicted_class to check if healthy)
    severity = get_infection_severity(confidence, predicted_class)
    
    # Get recommendations
    recommendations = get_disease_recommendations(predicted_class)
    
    # Build output string
    output = []
    output.append("\n" + "=" * 60)
    output.append("PREDICTION RESULTS")
    output.append("=" * 60)
    
    # 1. Image and Prediction Info
    output.append("\n[IMAGE INFORMATION]")
    output.append(f"   Image Name         : {image_name}")
    output.append(f"   Predicted Disease  : {predicted_class}")
    output.append(f"   Confidence Score   : {confidence * 100:.2f} %")
    
    # 2. Infection Severity
    output.append(f"\n[INFECTION ASSESSMENT]")
    output.append(f"   Severity Level     : {severity}")
    
    # 3. Probability Distribution
    output.append("\n[PROBABILITY DISTRIBUTION (All Classes)]")
    output.append("   " + "-" * 40)
    
    for class_idx, class_name in enumerate(class_names):
        prob = all_predictions[class_idx] if class_idx < len(all_predictions) else 0
        prob_pct = prob * 100
        
        # Create a visual bar
        bar_length = 20
        filled = int(bar_length * prob)
        bar = '#' * filled + '-' * (bar_length - filled)
        
        output.append(f"   {class_name:15} : {prob_pct:6.2f} % |{bar}|")
    
    # 4. Grad-CAM Information
    output.append(f"\n[GRAD-CAM ANALYSIS]")
    if output_path:
        output.append(f"   Heatmap Generated  : Yes")
        output.append(f"   Heatmap Saved At   : {output_path}")
        output.append(f"   Highlighted Area   : Model activation regions")
    else:
        output.append(f"   Heatmap Generated  : No")
    
    # 5. Recommendations
    output.append(f"\n[RECOMMENDATIONS]")
    output.append("   " + "-" * 40)
    for rec in recommendations:
        output.append(f"   {rec}")
    
    output.append("\n" + "=" * 60 + "\n")
    
    return "\n".join(output)


def format_batch_output(results, class_names):
    """
    Format batch prediction results into structured output.
    
    Args:
        results (list): List of prediction results
        class_names (list): List of all class names
        
    Returns:
        str: Formatted output string
    """
    output = []
    output.append("\n" + "=" * 60)
    output.append("BATCH PREDICTION RESULTS")
    output.append("=" * 60)
    
    output.append(f"\nTotal Images Processed : {len(results)}")
    output.append("-" * 60)
    
    for idx, result in enumerate(results, 1):
        image_name = result.get('image', 'Unknown')
        predicted_class = result.get('predicted_class', 'Unknown')
        confidence = result.get('confidence', 0)
        severity = get_infection_severity(confidence, predicted_class)
        
        output.append(f"\n{idx}. {image_name}")
        output.append(f"   Disease : {predicted_class} | Confidence : {confidence * 100:.2f}% | Severity : {severity}")
    
    output.append("\n" + "=" * 60 + "\n")
    
    return "\n".join(output)
