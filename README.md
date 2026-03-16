# 🌾 Wheat Disease Detection Web Application

A professional AI-powered web application for detecting wheat diseases using deep learning (CNN) with Grad-CAM visualization, infection severity analysis, and comprehensive reporting.

## 📋 Features

- **AI-Powered Disease Detection**: CNN deep learning model for accurate wheat disease classification
- **Drag & Drop Interface**: Simple image upload with preview
- **Grad-CAM Visualization**: Visual explanation showing which image regions influenced the prediction
- **Infection Severity Estimation**: Calculates infected leaf area percentage
- **Disease Information Panel**: Detailed information about detected diseases
- **Treatment Recommendations**: Disease-specific prevention and treatment advice
- **PDF Report Generation**: Automated report download with all analysis
- **Analytics Dashboard**: Track predictions and view disease distribution statistics
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Professional UI**: Agricultural theme with modern green color palette

## 🎯 Supported Diseases

1. **Healthy** - No disease detected (Green badge)
2. **Brown Rust** - Fungal infection caused by Puccinia triticina (Orange badge)
3. **Yellow Rust** - Stripe rust disease caused by Puccinia striiformis (Red badge)

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0.0
- **Deep Learning**: TensorFlow / Keras 2.15.0
- **Image Processing**: OpenCV, PIL
- **PDF Generation**: ReportLab
- **Scientific Computing**: NumPy, SciPy

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom agricultural theme with responsive design
- **JavaScript** - Interactive features and Chart.js visualizations
- **Bootstrap 5.3** - Responsive grid system
- **Chart.js** - Interactive data visualizations
- **Font Awesome 6.4** - Icons

## 📁 Project Structure

```
project-WDD-front/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── wheat-disease-detection/       # Original ML project directory
│   ├── models/
│   │   └── cnn_model.py           # CNN model architecture
│   ├── inference/
│   │   └── predict.py             # Prediction functions
│   ├── utils/
│   │   ├── gradcam.py             # Grad-CAM visualization
│   │   ├── preprocessing.py       # Image preprocessing
│   │   └── visualize.py           # Visualization utilities
│   └── results/
│       └── wheat_disease_model.h5 # Trained model file
│
├── utils/                          # Web app utility modules
│   ├── __init__.py
│   ├── infection_severity.py      # Infection severity estimation
│   ├── disease_knowledge.py       # Disease information & recommendations
│   └── pdf_generator.py           # PDF report generation
│
├── templates/                      # HTML templates
│   ├── index.html                 # Upload page
│   ├── results.html               # Prediction results page
│   └── dashboard.html             # Analytics dashboard
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Main stylesheet (agricultural theme)
│   └── js/
│       ├── upload.js              # Upload page functionality
│       ├── results.js             # Results page functionality
│       └── dashboard.js           # Dashboard functionality
│
└── uploads/                        # Uploaded images (auto-created)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- At least 2GB free disk space
- The trained model file: `wheat_disease_model.h5`

### Step 1: Clone/Setup Project

```bash
cd c:\project-WDD-front
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: TensorFlow installation may take several minutes on first install.

### Step 4: Verify Model File

Ensure the trained model exists:
```
wheat-disease-detection/results/wheat_disease_model.h5
```

### Step 5: Run Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🌐 Usage

### 1. Upload Image
- Navigate to the home page (`/`)
- Drag & drop a wheat leaf image or click to browse
- Supported formats: JPG, JPEG, PNG (Max 16MB)

### 2. Detect Disease
- Click "Detect Disease" button
- Wait for AI analysis (5-10 seconds)
- Automatically redirected to results page

### 3. View Results (`/results`)
- Predicted disease with confidence score
- Infection severity level and percentage
- Grad-CAM visualization showing disease regions
- Disease information and treatment recommendations
- Option to download PDF report

### 4. Download PDF Report
- Click "Download Report" button
- Includes: image, Grad-CAM, predictions, recommendations
- PDF automatically opens in browser or downloads

### 5. View Dashboard (`/dashboard`)
- Total predictions made
- Disease distribution chart
- Health vs infected ratio
- Average confidence by disease
- Recent predictions table
- Option to clear history

## 📊 API Endpoints

### Prediction API
```
POST /api/predict
- Input: Multipart form with 'file' field
- Output: JSON with disease prediction, confidence, severity, etc.
```

### Dashboard Data
```
GET /api/dashboard-data
- Output: JSON with statistics for dashboard
```

### Download Report
```
POST /api/download-report
- Output: PDF file download
```

### Prediction History
```
GET /api/prediction-history
- Output: JSON array of all predictions
```

### Clear History
```
POST /api/clear-history
- Output: JSON confirmation
```

## 🎨 Customization

### Change Agricultural Colors
Edit `static/css/style.css` - Modify CSS variables at the top:
```css
--primary-green: #1d5f2e;
--light-green: #2d7f4e;
--danger-red: #dc3545;
```

### Add More Diseases
Edit `utils/disease_knowledge.py` - Add entries to `DISEASE_DATABASE` dictionary

### Modify Infection Severity Thresholds
Edit `utils/infection_severity.py` - Adjust `estimate_infection_severity()` function

## 📈 Performance Tips

1. **Image Size**: Optimize input images (224x224 or smaller)
2. **Batch Processing**: Use `/api/predict` multiple times for accuracy
3. **Cache**: Clear browser cache if styles don't update
4. **Session**: Predictions stored in Flask session (expires on browser close)

## 🐛 Troubleshooting

### Model Not Loading
```
Error: "Model not loaded"
Solution: Verify wheat_disease_model.h5 exists in correct path
```

### Port Already in Use
```bash
# Change port in app.py: app.run(port=5001)
```

### Slow Predictions
- First prediction may be slow (TensorFlow initialization)
- Check GPU availability: `nvidia-smi`
- Ensure sufficient RAM (4GB minimum)

### File Upload Issues
- Check file size (max 16MB)
- Verify file format (JPG, PNG)
- Ensure `/uploads` directory exists

## 📝 Configuration

### Session Settings
Edit `app.py`:
```python
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Model Path
Edit `app.py`:
```python
MODEL_PATH = 'wheat-disease-detection/results/wheat_disease_model.h5'
CLASS_NAMES = ['Healthy', 'Brown_rust', 'Yellow_rust']
```

## 📊 Developed Features

✅ Image upload with drag-and-drop  
✅ Real-time disease detection  
✅ Grad-CAM visual explanations  
✅ Infection severity estimation  
✅ Disease information panels  
✅ Treatment recommendations  
✅ PDF report generation  
✅ Analytics dashboard  
✅ Prediction history tracking  
✅ Responsive mobile-friendly design  
✅ Professional agricultural UI theme  

## 🔐 Security Notes

- Do not set `debug=True` in production
- Change `app.secret_key` to a secure random value
- Validate all file uploads
- Implement user authentication for production use
- Use HTTPS in production

## 📜 License

MIT License - Free to use and modify

## 🤝 Contributing

To improve the system:
1. Collect more disease samples
2. Fine-tune the CNN model
3. Add more disease categories
4. Enhance UI/UX
5. Optimize prediction speed

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review error messages in console
3. Verify all dependencies installed
4. Check model file exists

---

**Wheat Disease Detection System** - Powered by AI  
Agricultural AI Solutions © 2024
