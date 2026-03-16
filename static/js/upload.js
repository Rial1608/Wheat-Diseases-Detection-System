/**
 * Upload.js - Handle image upload and prediction
 */

let selectedFile = null;
let uploadChart = null;

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const detectBtn = document.getElementById('detectBtn');
    const resetBtn = document.getElementById('resetBtn');

    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('active');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('active');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('active');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect();
        }
    });

    // Detect button
    detectBtn.addEventListener('click', performPrediction);

    // Reset button
    resetBtn.addEventListener('click', resetUpload);
});

function handleFileSelect() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload JPG or PNG image.');
        return;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size exceeds 16MB limit. Please upload a smaller image.');
        return;
    }

    selectedFile = file;
    displayPreview(file);
    
    // Enable detect button
    document.getElementById('detectBtn').disabled = false;
    document.getElementById('resetBtn').disabled = false;
}

function displayPreview(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        const previewContainer = document.getElementById('previewContainer');
        const previewImage = document.getElementById('previewImage');
        const fileName = document.getElementById('fileName');
        
        previewImage.src = e.target.result;
        fileName.textContent = file.name;
        previewContainer.classList.remove('d-none');
        
        // Clear any previous alerts
        hideError();
        hideSuccess();
    };
    
    reader.readAsDataURL(file);
}

async function performPrediction() {
    if (!selectedFile) {
        showError('No file selected.');
        return;
    }

    // Show loading spinner
    const loadingSpinner = document.getElementById('loadingSpinner');
    const detectBtn = document.getElementById('detectBtn');
    loadingSpinner.classList.remove('d-none');
    detectBtn.disabled = true;

    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Send prediction request
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Prediction failed');
        }

        const data = await response.json();

        // Show success message
        showSuccess('Disease detection completed successfully!');

        // Redirect to results page after a short delay
        setTimeout(() => {
            window.location.href = '/results';
        }, 1500);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred during prediction.');
    } finally {
        loadingSpinner.classList.add('d-none');
        detectBtn.disabled = false;
    }
}

function resetUpload() {
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const detectBtn = document.getElementById('detectBtn');
    const resetBtn = document.getElementById('resetBtn');

    fileInput.value = '';
    selectedFile = null;
    previewContainer.classList.add('d-none');
    detectBtn.disabled = true;
    resetBtn.disabled = true;

    hideError();
    hideSuccess();
}

function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorAlert.classList.remove('d-none');
    scrollToAlert(errorAlert);
}

function hideError() {
    document.getElementById('errorAlert').classList.add('d-none');
}

function showSuccess(message) {
    const successAlert = document.getElementById('successAlert');
    const successMessage = document.getElementById('successMessage');
    if (message) successMessage.textContent = message;
    successAlert.classList.remove('d-none');
    scrollToAlert(successAlert);
}

function hideSuccess() {
    document.getElementById('successAlert').classList.add('d-none');
}

function scrollToAlert(element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Add keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !document.getElementById('detectBtn').disabled) {
        performPrediction();
    }
});
