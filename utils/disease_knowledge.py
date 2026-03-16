"""
Disease information and treatment recommendations for wheat diseases.
"""

DISEASE_DATABASE = {
    'Healthy': {
        'description': 'The wheat plant shows no signs of disease.',
        'scientific_name': 'N/A',
        'symptoms': [
            'Green, healthy leaves',
            'No discoloration or spots',
            'Normal plant growth'
        ],
        'causes': 'N/A',
        'recommendations': [
            'Continue regular monitoring',
            'Maintain proper irrigation schedule',
            'Ensure adequate nutrient levels in soil',
            'Practice crop rotation'
        ],
        'danger_level': 0,
        'color': '#28a745'
    },
    
    'Brown_rust': {
        'description': 'Brown rust (Leaf Rust) is a fungal disease caused by Puccinia triticina that affects wheat leaves and stems. It can significantly reduce crop yield and quality if not managed properly.',
        'scientific_name': 'Puccinia triticina',
        'symptoms': [
            'Reddish-brown pustules on leaf surfaces',
            'Yellow halos around pustules',
            'Symptoms first appear on lower leaves',
            'Progressive movement up the plant as it matures',
            'Leaves may become necrotic and die prematurely'
        ],
        'causes': [
            'Fungal infection by Puccinia triticina',
            'Favorable conditions: warm, wet weather (15-22°C)',
            'High humidity and dew periods',
            'Infected plant residue from previous seasons',
            'Susceptible wheat varieties'
        ],
        'recommendations': [
            'Apply suitable fungicide (e.g., azole or strobilurin fungicides)',
            'Use resistant wheat varieties when possible',
            'Remove and destroy infected plant debris',
            'Ensure proper field sanitation',
            'Avoid overhead irrigation that promotes leaf wetness',
            'Plant disease-free seed stock',
            'Monitor fields regularly for early detection',
            'Follow integrated pest management (IPM) guidelines',
            'Implement crop rotation (avoid planting wheat in consecutive years)',
            'Apply fungicide at early stages of disease development for best results'
        ],
        'danger_level': 8,
        'color': '#fd7e14'
    },
    
    'Yellow_rust': {
        'description': 'Yellow rust (Stripe Rust) is a fungal disease caused by Puccinia striiformis that forms characteristic yellow stripes on wheat leaves. It thrives in cool conditions and can cause severe damage.',
        'scientific_name': 'Puccinia striiformis f. sp. tritici',
        'symptoms': [
            'Yellow or orange-yellow stripes on leaves',
            'Stripes run parallel to leaf veins',
            'Symptoms first appear on upper leaf surfaces',
            'May progress to stem bases in severe cases',
            'Infected areas may turn brown and necrotic with age',
            'Heavy infections cause premature drying of foliage'
        ],
        'causes': [
            'Fungal infection by Puccinia striiformis f. sp. tritici',
            'Cool weather conditions (10-15°C optimal)',
            'High humidity and leaf moisture',
            'Infected seeds or volunteer wheat plants',
            'Wind-borne spore dispersal from nearby fields',
            'Susceptible wheat varieties'
        ],
        'recommendations': [
            'Apply fungicide treatments (triazoles or combination fungicides)',
            'Select resistant wheat varieties (resistance breeding important)',
            'Remove infected volunteer wheat and grasses',
            'Implement strict field sanitation',
            'Avoid planting wheat close to other susceptible cereal crops',
            'Monitor weather forecasts for favorable disease conditions',
            'Scout fields weekly during epidemic conditions',
            'Apply fungicide early in disease development for maximum effectiveness',
            'Manage irrigation to reduce leaf wetness duration',
            'Implement multi-year crop rotation',
            'Destroy infected crop residue',
            'Consider delayed planting to avoid cool season susceptibility'
        ],
        'danger_level': 9,
        'color': '#dc3545'
    }
}


def get_disease_info(disease_class):
    """
    Get detailed information about a disease.
    
    Args:
        disease_class: String representing the disease class name
    
    Returns:
        Dictionary with disease information
    """
    
    # Handle specific naming conventions
    disease_key = disease_class
    if disease_class not in DISEASE_DATABASE:
        # Try to find a case-insensitive match
        for key in DISEASE_DATABASE.keys():
            if key.lower() == disease_class.lower():
                disease_key = key
                break
        else:
            # Return default unknown disease info
            return {
                'description': 'Unknown disease',
                'scientific_name': 'Unknown',
                'symptoms': ['Unable to determine'],
                'causes': ['Unable to determine'],
                'recommendations': ['Please consult an agricultural expert'],
                'danger_level': 5,
                'color': '#6c757d'
            }
    
    return DISEASE_DATABASE[disease_key]


def get_treatment_recommendations(disease_class):
    """
    Get treatment and prevention recommendations for a disease.
    
    Args:
        disease_class: String representing the disease class name
    
    Returns:
        List of recommendation strings
    """
    
    disease_info = get_disease_info(disease_class)
    return disease_info.get('recommendations', ['No specific recommendations available.'])


def get_danger_level(disease_class):
    """
    Get the danger level (severity ranking) of a disease.
    
    Args:
        disease_class: String representing the disease class name
    
    Returns:
        Integer between 0-10 (0 = healthy, 10 = most dangerous)
    """
    
    disease_info = get_disease_info(disease_class)
    return disease_info.get('danger_level', 5)


def get_disease_symptoms(disease_class):
    """
    Get a list of symptoms for a disease.
    
    Args:
        disease_class: String representing the disease class name
    
    Returns:
        List of symptom descriptions
    """
    
    disease_info = get_disease_info(disease_class)
    return disease_info.get('symptoms', [])


def get_disease_color(disease_class):
    """
    Get a standard color code for a disease for UI purposes.
    
    Args:
        disease_class: String representing the disease class name
    
    Returns:
        String representing hex color code
    """
    
    disease_info = get_disease_info(disease_class)
    return disease_info.get('color', '#6c757d')


def get_all_diseases():
    """
    Get a list of all diseases in the database.
    
    Returns:
        List of disease class names
    """
    
    return list(DISEASE_DATABASE.keys())


def format_recommendations_for_display(disease_class):
    """
    Format recommendations as HTML for display.
    
    Args:
        disease_class: String representing the disease class name
    
    Returns:
        String containing HTML-formatted recommendations
    """
    
    recommendations = get_treatment_recommendations(disease_class)
    
    html = '<ul class="recommendation-list">\n'
    for rec in recommendations:
        html += f'  <li>{rec}</li>\n'
    html += '</ul>\n'
    
    return html
