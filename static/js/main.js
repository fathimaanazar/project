// Blood Donation Platform - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    console.log('Blood Donation Platform initialized');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize blood type compatibility
    initializeBloodTypeHelpers();
    
    // Initialize notification system
    initializeNotifications();
    
    // Initialize dashboard features
    initializeDashboard();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Enhanced form validation
 */
function initializeFormValidation() {
    // Custom validation for blood donation eligibility
    const ageInputs = document.querySelectorAll('input[type="date"][name*="birth"]');
    ageInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateAge(this);
        });
    });
    
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[name*="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    });
    
    // Real-time password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.name === 'password') {
            input.addEventListener('input', function() {
                checkPasswordStrength(this);
            });
        }
    });
}

/**
 * Validate age for blood donation eligibility
 */
function validateAge(input) {
    const birthDate = new Date(input.value);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    
    const feedbackDiv = input.parentElement.querySelector('.age-feedback') || 
                       createFeedbackElement(input.parentElement, 'age-feedback');
    
    if (age < 16) {
        input.classList.add('is-invalid');
        feedbackDiv.innerHTML = '<small class="text-danger"><i class="fas fa-exclamation-triangle"></i> Must be at least 16 years old to donate blood</small>';
        feedbackDiv.style.display = 'block';
    } else if (age > 65) {
        input.classList.remove('is-invalid');
        input.classList.add('is-warning');
        feedbackDiv.innerHTML = '<small class="text-warning"><i class="fas fa-info-circle"></i> Donors over 65 may require additional medical clearance</small>';
        feedbackDiv.style.display = 'block';
    } else {
        input.classList.remove('is-invalid', 'is-warning');
        feedbackDiv.style.display = 'none';
    }
}

/**
 * Format phone number input
 */
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 6) {
        value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
    } else if (value.length >= 3) {
        value = value.replace(/(\d{3})(\d{0,3})/, '($1) $2');
    }
    input.value = value;
}

/**
 * Check password strength
 */
function checkPasswordStrength(input) {
    const password = input.value;
    const strengthDiv = input.parentElement.querySelector('.password-strength') || 
                       createFeedbackElement(input.parentElement, 'password-strength');
    
    let strength = 0;
    let feedback = [];
    
    // Length check
    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');
    
    // Uppercase check
    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('One uppercase letter');
    
    // Lowercase check
    if (/[a-z]/.test(password)) strength++;
    else feedback.push('One lowercase letter');
    
    // Number check
    if (/[0-9]/.test(password)) strength++;
    else feedback.push('One number');
    
    // Special character check
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    else feedback.push('One special character');
    
    const strengthClasses = ['danger', 'warning', 'info', 'primary', 'success'];
    const strengthLabels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    
    if (password.length > 0) {
        strengthDiv.innerHTML = `
            <div class="password-strength-meter mt-2">
                <div class="progress" style="height: 4px;">
                    <div class="progress-bar bg-${strengthClasses[strength-1] || 'danger'}" 
                         style="width: ${(strength/5)*100}%"></div>
                </div>
                <small class="text-${strengthClasses[strength-1] || 'danger'}">
                    ${strengthLabels[strength-1] || 'Very Weak'}
                    ${feedback.length > 0 ? ' - Need: ' + feedback.join(', ') : ''}
                </small>
            </div>
        `;
        strengthDiv.style.display = 'block';
    } else {
        strengthDiv.style.display = 'none';
    }
}

/**
 * Create feedback element
 */
function createFeedbackElement(parent, className) {
    const div = document.createElement('div');
    div.className = className;
    div.style.display = 'none';
    parent.appendChild(div);
    return div;
}

/**
 * Blood type compatibility helpers
 */
function initializeBloodTypeHelpers() {
    const bloodTypeSelects = document.querySelectorAll('select[name*="blood_type"]');
    
    bloodTypeSelects.forEach(select => {
        select.addEventListener('change', function() {
            showBloodTypeInfo(this);
        });
    });
}

/**
 * Show blood type compatibility information
 */
function showBloodTypeInfo(select) {
    const bloodType = select.value;
    if (!bloodType) return;
    
    const compatibility = getBloodTypeCompatibility(bloodType);
    const infoDiv = select.parentElement.querySelector('.blood-type-info') || 
                   createFeedbackElement(select.parentElement, 'blood-type-info');
    
    if (compatibility) {
        infoDiv.innerHTML = `
            <div class="alert alert-info mt-2 p-2">
                <small>
                    <strong>${bloodType}</strong> can donate to: ${compatibility.canDonateTo.join(', ')}<br>
                    <strong>${bloodType}</strong> can receive from: ${compatibility.canReceiveFrom.join(', ')}
                </small>
            </div>
        `;
        infoDiv.style.display = 'block';
    }
}

/**
 * Get blood type compatibility data
 */
function getBloodTypeCompatibility(bloodType) {
    const compatibility = {
        'O-': { canDonateTo: ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'], canReceiveFrom: ['O-'] },
        'O+': { canDonateTo: ['O+', 'A+', 'B+', 'AB+'], canReceiveFrom: ['O-', 'O+'] },
        'A-': { canDonateTo: ['A-', 'A+', 'AB-', 'AB+'], canReceiveFrom: ['O-', 'A-'] },
        'A+': { canDonateTo: ['A+', 'AB+'], canReceiveFrom: ['O-', 'O+', 'A-', 'A+'] },
        'B-': { canDonateTo: ['B-', 'B+', 'AB-', 'AB+'], canReceiveFrom: ['O-', 'B-'] },
        'B+': { canDonateTo: ['B+', 'AB+'], canReceiveFrom: ['O-', 'O+', 'B-', 'B+'] },
        'AB-': { canDonateTo: ['AB-', 'AB+'], canReceiveFrom: ['O-', 'A-', 'B-', 'AB-'] },
        'AB+': { canDonateTo: ['AB+'], canReceiveFrom: ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'] }
    };
    
    return compatibility[bloodType] || null;
}

/**
 * Initialize notification system
 */
function initializeNotifications() {
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.transition = 'opacity 0.5s ease-out';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentElement) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });
    
    // Initialize notification bell (if exists)
    const notificationBell = document.getElementById('notificationBell');
    if (notificationBell) {
        notificationBell.addEventListener('click', function() {
            markNotificationsAsRead();
        });
    }
}

/**
 * Mark notifications as read
 */
function markNotificationsAsRead() {
    // This would typically make an AJAX call to mark notifications as read
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        badge.style.display = 'none';
    }
}

/**
 * Initialize dashboard features
 */
function initializeDashboard() {
    // Initialize progress bars with animation
    animateProgressBars();
    
    // Initialize dashboard statistics counters
    animateCounters();
    
    // Initialize real-time updates (if needed)
    initializeRealTimeUpdates();
}

/**
 * Animate progress bars
 */
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = targetWidth;
        }, 100);
    });
}

/**
 * Animate number counters
 */
function animateCounters() {
    const counters = document.querySelectorAll('.dashboard-stat, .text-primary h4, .text-success h4, .text-info h4, .text-warning h4');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        if (isNaN(target)) return;
        
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            counter.textContent = Math.floor(current);
            
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            }
        }, 20);
    });
}

/**
 * Initialize real-time updates
 */
function initializeRealTimeUpdates() {
    // This would typically set up WebSocket connections or periodic AJAX calls
    // For now, we'll just set up periodic page updates for critical sections
    
    if (window.location.pathname.includes('dashboard')) {
        // Refresh dashboard stats every 5 minutes
        setInterval(() => {
            refreshDashboardStats();
        }, 300000);
    }
}

/**
 * Refresh dashboard statistics
 */
function refreshDashboardStats() {
    // This would make an AJAX call to get updated statistics
    console.log('Refreshing dashboard stats...');
    // Implementation would depend on backend API
}

/**
 * Utility functions
 */

// Show loading state
function showLoading(element) {
    element.classList.add('loading');
    element.setAttribute('disabled', 'disabled');
}

// Hide loading state
function hideLoading(element) {
    element.classList.remove('loading');
    element.removeAttribute('disabled');
}

// Show confirmation dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Calculate days between dates
function daysBetween(date1, date2) {
    const oneDay = 24 * 60 * 60 * 1000;
    return Math.round(Math.abs((date1 - date2) / oneDay));
}

// Blood donation eligibility checker
function checkDonationEligibility(lastDonationDate) {
    if (!lastDonationDate) return true;
    
    const lastDonation = new Date(lastDonationDate);
    const today = new Date();
    const daysSince = daysBetween(today, lastDonation);
    
    return daysSince >= 56;
}

// Get urgency color class
function getUrgencyColorClass(urgency) {
    const colors = {
        'low': 'success',
        'medium': 'warning', 
        'high': 'danger',
        'critical': 'dark'
    };
    return colors[urgency] || 'secondary';
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
    
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value, this.dataset.target);
            }, 300);
        });
    });
}

// Perform search
function performSearch(query, target) {
    if (!query || !target) return;
    
    const targetElements = document.querySelectorAll(target);
    
    targetElements.forEach(element => {
        const searchText = element.textContent.toLowerCase();
        const matches = searchText.includes(query.toLowerCase());
        
        element.style.display = matches ? '' : 'none';
    });
}

// Export functionality
function exportData(data, filename, type = 'csv') {
    let content, mimeType;
    
    if (type === 'csv') {
        content = convertToCSV(data);
        mimeType = 'text/csv';
    } else if (type === 'json') {
        content = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.href = url;
    link.download = filename;
    link.click();
    
    window.URL.revokeObjectURL(url);
}

// Convert data to CSV format
function convertToCSV(data) {
    if (!data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csvHeaders = headers.join(',');
    
    const csvRows = data.map(row => {
        return headers.map(header => {
            const value = row[header];
            return typeof value === 'string' ? `"${value}"` : value;
        }).join(',');
    });
    
    return [csvHeaders, ...csvRows].join('\n');
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

// Handle window resize events
window.addEventListener('resize', function() {
    // Recalculate layouts if needed
    const tables = document.querySelectorAll('.table-responsive');
    tables.forEach(table => {
        // Force table redraw on mobile
        if (window.innerWidth < 768) {
            table.style.fontSize = '0.875rem';
        } else {
            table.style.fontSize = '';
        }
    });
});

// Error handling for AJAX requests
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    
    // Show user-friendly error message
    const errorAlert = document.createElement('div');
    errorAlert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
    errorAlert.style.top = '20px';
    errorAlert.style.right = '20px';
    errorAlert.style.zIndex = '9999';
    errorAlert.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        An error occurred. Please refresh the page and try again.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(errorAlert);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (errorAlert.parentElement) {
            errorAlert.remove();
        }
    }, 10000);
});

console.log('Blood Donation Platform JavaScript loaded successfully');
