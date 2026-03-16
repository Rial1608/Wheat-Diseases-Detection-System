/**
 * Dashboard.js - Handle analytics dashboard
 */

let diseaseChart = null;
let healthChart = null;
let confidenceChart = null;

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    setupEventListeners();
});

function setupEventListeners() {
    const clearBtn = document.getElementById('clearHistoryBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearHistory);
    }
}

async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard-data');
        
        if (!response.ok) {
            throw new Error('Failed to load dashboard data');
        }

        const data = await response.json();
        
        // Update statistics
        updateStatistics(data);
        
        // Initialize charts
        initializeDiseaseChart(data);
        initializeHealthChart(data);
        initializeConfidenceChart(data);
        
        // Update predictions table
        updatePredictionsTable(data);
        
        // Show/hide empty state
        toggleEmptyState(data);
        
        // Show clear history button if there are predictions
        if (data.total_predictions > 0) {
            document.getElementById('clearHistoryBtn').style.display = 'block';
        }

    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showDashboardError(error.message);
    }
}

function updateStatistics(data) {
    // Total predictions
    document.getElementById('totalPredictions').textContent = data.total_predictions;
    
    // Healthy count
    document.getElementById('healthyCount').textContent = data.healthy_count;
    
    // Infected count
    document.getElementById('infectedCount').textContent = data.infected_count;
    
    // Health rate percentage
    const healthRate = data.total_predictions > 0 
        ? ((data.healthy_count / data.total_predictions) * 100).toFixed(1)
        : 0;
    document.getElementById('healthRate').textContent = healthRate + '%';
}

function initializeDiseaseChart(data) {
    const ctx = document.getElementById('diseaseDistributionChart');
    if (!ctx) return;

    const distribution = data.disease_distribution;
    const labels = Object.keys(distribution);
    const values = Object.values(distribution);
    
    const colors = {
        'Healthy': '#28a745',
        'Brown_rust': '#fd7e14',
        'Yellow_rust': '#dc3545'
    };

    const bgColors = labels.map(label => colors[label] || '#6c757d');

    if (diseaseChart) diseaseChart.destroy();

    diseaseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: bgColors,
                borderColor: 'white',
                borderWidth: 2,
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12, weight: '600' },
                        color: '#212529',
                        padding: 15,
                        usePointStyle: true
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
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function initializeHealthChart(data) {
    const ctx = document.getElementById('healthStatusChart');
    if (!ctx) return;

    const healthyCount = data.healthy_count;
    const infectedCount = data.infected_count;

    if (healthChart) healthChart.destroy();

    healthChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Healthy', 'Infected'],
            datasets: [{
                data: [healthyCount, infectedCount],
                backgroundColor: ['#28a745', '#dc3545'],
                borderColor: 'white',
                borderWidth: 2,
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12, weight: '600' },
                        color: '#212529',
                        padding: 15,
                        usePointStyle: true
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
                            const total = healthyCount + infectedCount;
                            const percentage = total > 0 
                                ? ((context.parsed / total) * 100).toFixed(1)
                                : 0;
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function initializeConfidenceChart(data) {
    const ctx = document.getElementById('confidenceChart');
    if (!ctx) return;

    const confidenceData = data.average_confidence_by_disease;
    const labels = Object.keys(confidenceData);
    const values = Object.values(confidenceData);

    const colors = {
        'Healthy': '#28a745',
        'Brown_rust': '#fd7e14',
        'Yellow_rust': '#dc3545'
    };

    const bgColors = labels.map(label => colors[label] || '#6c757d');

    if (confidenceChart) confidenceChart.destroy();

    confidenceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Confidence',
                data: values,
                backgroundColor: bgColors,
                borderColor: bgColors,
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: '#2d7f4e'
            }]
        },
        options: {
            indexAxis: 'x',
            responsive: true,
            maintainAspectRatio: true,
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
                            return (context.parsed.y * 100).toFixed(1) + '%';
                        }
                    }
                }
            },
            scales: {
                y: {
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
                x: {
                    ticks: { font: { size: 11, weight: '600' } },
                    grid: { display: false }
                }
            }
        }
    });
}

function updatePredictionsTable(data) {
    const tableBody = document.getElementById('predictionsTableBody');
    const recentCount = document.getElementById('recentCount');
    
    if (!tableBody) return;

    const predictions = data.recent_predictions || [];
    recentCount.textContent = predictions.length;

    if (predictions.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted py-4">
                    <i class="fas fa-inbox display-4 mb-2"></i><br>No predictions yet
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = predictions.map(pred => {
        const date = new Date(pred.timestamp);
        const dateStr = date.toLocaleDateString();
        const timeStr = date.toLocaleTimeString();
        
        const diseaseColors = {
            'Healthy': '#28a745',
            'Brown_rust': '#fd7e14',
            'Yellow_rust': '#dc3545'
        };
        
        const severityColors = {
            'Healthy': '#28a745',
            'Trace': '#ffc107',
            'Low Infection': '#fd7e14',
            'Moderate Infection': '#fd7e14',
            'Severe Infection': '#dc3545'
        };

        return `
            <tr>
                <td>
                    <small>${dateStr}<br>${timeStr}</small>
                </td>
                <td>
                    <small>${pred.original_filename}</small>
                </td>
                <td>
                    <span class="badge" style="background-color: ${diseaseColors[pred.predicted_disease] || '#6c757d'};">
                        ${pred.predicted_disease}
                    </span>
                </td>
                <td>
                    <strong>${(pred.confidence * 100).toFixed(1)}%</strong>
                </td>
                <td>
                    <span class="badge" style="background-color: ${severityColors[pred.severity_level] || '#6c757d'};">
                        ${pred.severity_level}
                    </span>
                </td>
                <td>
                    <strong>${pred.severity_percentage}%</strong>
                </td>
            </tr>
        `;
    }).join('');
}

function toggleEmptyState(data) {
    const emptyState = document.getElementById('emptyState');
    if (data.total_predictions === 0) {
        emptyState.style.display = 'block';
    } else {
        emptyState.style.display = 'none';
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear all prediction history? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/api/clear-history', {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Failed to clear history');
        }

        // Reload dashboard
        loadDashboardData();
        document.getElementById('clearHistoryBtn').style.display = 'none';
        
        // Show success message
        const successDiv = document.createElement('div');
        successDiv.className = 'alert alert-success alert-dismissible fade show';
        successDiv.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <strong>Success!</strong> Prediction history cleared.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.container-fluid').insertBefore(successDiv, document.querySelector('.row'));
        
        setTimeout(() => successDiv.remove(), 4000);

    } catch (error) {
        console.error('Error clearing history:', error);
        alert('Error clearing history: ' + error.message);
    }
}

function showDashboardError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <strong>Error!</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container-fluid').insertBefore(errorDiv, document.querySelector('.row'));
}

// Auto-refresh dashboard every 30 seconds
setInterval(function() {
    // Commented out for now - enable if you want auto-refresh
    // loadDashboardData();
}, 30000);
