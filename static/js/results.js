/**
 * Results.js - Handle results page interactions
 */

let probabilityChart = null;

document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    setupEventListeners();
});

function initializePage() {
    // Get prediction data from page
    const predictionDataElement = document.getElementById('predictionData');
    
    // Initialize charts if data exists
    if (document.getElementById('probabilityChart')) {
        initializeProbabilityChart();
    }
    
    // Scroll to top
    window.scrollTo(0, 0);
}

function setupEventListeners() {
    const downloadBtn = document.getElementById('downloadReportBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadReport);
    }
}

function initializeProbabilityChart() {
    const ctx = document.getElementById('probabilityChart');
    if (!ctx) return;

    // Extract data from the page DOM
    const tableBody = document.querySelector('.list-group');
    if (!tableBody) return;

    const labels = [];
    const data = [];
    const colors = [
        '#28a745', // Green
        '#fd7e14', // Orange
        '#dc3545'  // Red
    ];

    // Parse the disease probabilities from the page
    const items = document.querySelectorAll('.list-group-item');
    items.forEach((item, index) => {
        const diseaseName = item.querySelector('span:first-child')?.textContent.trim();
        const probabilityBadge = item.querySelector('.badge')?.textContent.trim();
        
        if (diseaseName && probabilityBadge) {
            labels.push(diseaseName);
            const prob = parseFloat(probabilityBadge) / 100;
            data.push(prob);
        }
    });

    if (labels.length === 0) return;

    // Create chart
    probabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Prediction Probability',
                data: data,
                backgroundColor: colors.slice(0, data.length),
                borderColor: colors.slice(0, data.length),
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: '#2d7f4e',
                hoverBorderColor: '#1d5f2e'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: { size: 12, weight: '600' },
                        color: '#212529',
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8,
                    titleFont: { size: 13, weight: 'bold' },
                    bodyFont: { size: 12 },
                    callbacks: {
                        label: function(context) {
                            return (context.parsed.x * 100).toFixed(1) + '%';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        callback: function(value) {
                            return (value * 100).toFixed(0) + '%';
                        },
                        font: { size: 11 }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    }
                },
                y: {
                    ticks: { font: { size: 11, weight: '600' } },
                    grid: { display: false }
                }
            }
        }
    });
}

async function downloadReport() {
    const btn = document.getElementById('downloadReportBtn');
    const originalText = btn.innerHTML;
    
    try {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';

        const response = await fetch('/api/download-report', {
            method: 'POST'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to generate report');
        }

        // Get the PDF blob
        const blob = await response.blob();
        
        // Create a temporary URL for the blob
        const downloadUrl = window.URL.createObjectURL(blob);
        
        // Create a temporary link and trigger download
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `wheat_disease_report_${new Date().toISOString().slice(0,10)}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Clean up
        window.URL.revokeObjectURL(downloadUrl);

        // Show success message
        showDownloadSuccess();

    } catch (error) {
        console.error('Download error:', error);
        alert('Error generating report: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

function showDownloadSuccess() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'alert alert-success alert-dismissible fade show';
    messageDiv.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <strong>Success!</strong> Report downloaded successfully.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Export data as CSV (optional feature)
function exportDataAsCSV() {
    const prediction = getPredictionData();
    if (!prediction) return;

    const csv = [
        ['Wheat Disease Detection Report'],
        ['Date', new Date().toLocaleDateString()],
        [],
        ['Prediction Results'],
        ['Disease', prediction.disease],
        ['Confidence', prediction.confidence],
        ['Severity Level', prediction.severity],
        ['Infected Area %', prediction.infectedArea],
        [],
        ['Disease Probabilities'],
    ];

    // Add probabilities
    Object.entries(prediction.allPredictions || {}).forEach(([disease, prob]) => {
        csv.push([disease, (prob * 100).toFixed(1) + '%']);
    });

    // Convert to CSV string
    const csvString = csv.map(row => row.join(',')).join('\n');
    
    // Trigger download
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `prediction_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
}

function getPredictionData() {
    // Extract prediction data from page
    return {
        disease: document.querySelector('.result-badge')?.textContent || 'Unknown',
        confidence: document.querySelector('.confidence-value')?.textContent || 'N/A',
        severity: document.querySelector('.severity-badge')?.textContent || 'N/A',
        infectedArea: document.querySelector('.infected-area-value')?.textContent || 'N/A'
    };
}

// Add print functionality
function printResults() {
    window.print();
}

// Share results (if available)
function shareResults() {
    const shareData = {
        title: 'Wheat Disease Detection Results',
        text: 'Check out my wheat disease detection results!',
        url: window.location.href
    };

    if (navigator.share) {
        navigator.share(shareData).catch(err => console.log('Share failed:', err));
    } else {
        // Fallback - copy URL to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('Results link copied to clipboard!');
        });
    }
}
