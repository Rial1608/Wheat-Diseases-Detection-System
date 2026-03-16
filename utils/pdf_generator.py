"""
PDF Report Generator for Wheat Disease Detection Results
"""

import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from PIL import Image as PILImage


def generate_pdf_report(prediction, uploaded_image_path, gradcam_image_path, results_folder):
    """
    Generate a comprehensive PDF report of the disease prediction.
    
    Args:
        prediction: Dictionary containing prediction results
        uploaded_image_path: Path to the original uploaded image
        gradcam_image_path: Path to the Grad-CAM visualization image
        results_folder: Path to save the PDF report
    
    Returns:
        Path to the generated PDF file
    """
    
    # Create PDF filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"wheat_disease_report_{timestamp}.pdf"
    pdf_path = os.path.join(results_folder, pdf_filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1d5f2e'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d7f4e'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderColor=colors.HexColor('#2d7f4e'),
        borderWidth=1,
        borderPadding=6,
        borderRightWidth=0,
        borderTopWidth=0,
        borderBottomWidth=2,
        borderLeftWidth=0
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Title
    elements.append(Paragraph('🌾 WHEAT DISEASE DETECTION REPORT 🌾', title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Report Information
    report_info_data = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Image File:', prediction.get('original_filename', 'Unknown')],
        ['Detection Date:', prediction.get('timestamp', 'Unknown')[:10]]
    ]
    
    report_table = Table(report_info_data, colWidths=[2*inch, 4*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c8e6c9'))
    ]))
    elements.append(report_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Prediction Results Section
    elements.append(Paragraph('PREDICTION RESULTS', heading_style))
    
    # Determine result color based on disease
    is_healthy = prediction['predicted_disease'].lower() == 'healthy'
    result_color = colors.HexColor('#28a745') if is_healthy else colors.HexColor('#dc3545')
    
    results_data = [
        ['Predicted Disease:', prediction['predicted_disease']],
        ['Confidence Score:', prediction['confidence_percentage']],
        ['Severity Level:', prediction['severity_level']],
        ['Infected Leaf Area:', f"{prediction['severity_percentage']}%"]
    ]
    
    results_table = Table(results_data, colWidths=[2*inch, 4*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('TEXTCOLOR', (1, 0), (1, 0), result_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONTSIZE', (1, 0), (1, 0), 13),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd'))
    ]))
    elements.append(results_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Disease Probability Distribution
    elements.append(Paragraph('DISEASE PROBABILITY DISTRIBUTION', heading_style))
    
    all_predictions = prediction.get('all_predictions', {})
    prob_data = [['Disease', 'Probability']]
    
    for disease, prob in sorted(all_predictions.items(), key=lambda x: x[1], reverse=True):
        prob_percentage = f"{prob*100:.1f}%"
        prob_data.append([disease, prob_percentage])
    
    prob_table = Table(prob_data, colWidths=[3*inch, 3*inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d7f4e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    elements.append(prob_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Images Section
    elements.append(Paragraph('IMAGE ANALYSIS', heading_style))
    
    # Add images if they exist
    try:
        image_elements = []
        image_width = 3*inch
        image_height = 2.25*inch
        
        # Original image
        if os.path.exists(uploaded_image_path):
            try:
                img = RLImage(uploaded_image_path, width=image_width, height=image_height)
                image_elements.append([Paragraph('Original Image', styles['Normal']), img])
            except Exception as e:
                image_elements.append([Paragraph('Original Image', styles['Normal']), Paragraph('[Image unavailable]', styles['Normal'])])
        
        # Grad-CAM image
        if os.path.exists(gradcam_image_path):
            try:
                img = RLImage(gradcam_image_path, width=image_width, height=image_height)
                image_elements.append([Paragraph('Grad-CAM Analysis', styles['Normal']), img])
            except Exception as e:
                image_elements.append([Paragraph('Grad-CAM Analysis', styles['Normal']), Paragraph('[Image unavailable]', styles['Normal'])])
        
        if image_elements:
            # Create a table with images side by side
            image_table = Table([image_elements], colWidths=[3.5*inch, 3.5*inch])
            image_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(image_table)
            elements.append(Spacer(1, 0.3*inch))
    
    except Exception as e:
        print(f"Error adding images to PDF: {e}")
    
    # Page break before recommendations
    elements.append(PageBreak())
    
    # Disease Information Section
    disease_info = prediction.get('disease_info', {})
    if disease_info:
        elements.append(Paragraph('DISEASE INFORMATION', heading_style))
        
        # Description
        description = disease_info.get('description', 'No description available')
        elements.append(Paragraph(description, normal_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Symptoms
        if disease_info.get('symptoms'):
            elements.append(Paragraph('Symptoms:', styles['Heading3']))
            symptoms_text = '<br/>'.join(['• ' + s for s in disease_info.get('symptoms', [])])
            elements.append(Paragraph(symptoms_text, normal_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Causes
        if disease_info.get('causes') and isinstance(disease_info['causes'], list):
            elements.append(Paragraph('Causes:', styles['Heading3']))
            causes_text = '<br/>'.join(['• ' + c for c in disease_info.get('causes', [])])
            elements.append(Paragraph(causes_text, normal_style))
            elements.append(Spacer(1, 0.15*inch))
    
    # Treatment Recommendations Section
    elements.append(Paragraph('TREATMENT & PREVENTION RECOMMENDATIONS', heading_style))
    
    recommendations = prediction.get('treatment_recommendations', [])
    for i, rec in enumerate(recommendations, 1):
        elements.append(Paragraph(f'{i}. {rec}', normal_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(
        'This report was generated by the AI Wheat Disease Detection System. '
        'Please consult an agricultural expert for final diagnosis and treatment decisions.',
        footer_style
    ))
    
    # Build PDF
    try:
        doc.build(elements)
        print(f"PDF report generated successfully: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"Error building PDF: {e}")
        raise


def create_summary_statistics_page(predictions):
    """
    Create a summary statistics page for batch reports.
    
    Args:
        predictions: List of prediction dictionaries
    
    Returns:
        List of PDF elements for the statistics page
    """
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Calculate statistics
    total = len(predictions)
    healthy = sum(1 for p in predictions if p['predicted_disease'].lower() == 'healthy')
    infected = total - healthy
    
    # Create summary table
    summary_data = [
        ['Statistic', 'Count', 'Percentage'],
        ['Total Predictions', str(total), '100%'],
        ['Healthy', str(healthy), f'{(healthy/total)*100:.1f}%' if total > 0 else '0%'],
        ['Infected', str(infected), f'{(infected/total)*100:.1f}%' if total > 0 else '0%']
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d7f4e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd'))
    ]))
    
    elements.append(summary_table)
    
    return elements
