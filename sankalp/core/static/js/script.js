// SANKALP - Smart Campus Management System
// Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize popovers
    initializePopovers();
    
    // Setup form validation
    setupFormValidation();
    
    // Setup password toggle
    setupPasswordToggle();
    
    // Setup search functionality
    setupSearch();
    
    // Setup filters
    setupFilters();
});

// ==================== TOOLTIPS ====================
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ==================== POPOVERS ====================
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ==================== TOAST NOTIFICATIONS ====================
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast from DOM after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// ==================== FORM VALIDATION ====================
function setupFormValidation() {
    'use strict';
    
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            // Check if this is a login form
            const isLoginForm = form.id === 'loginForm';
            
            if (!isLoginForm) {
                // Registration form validations
                // Validate email format
                const emailInput = form.querySelector('input[type="email"]');
                if (emailInput && emailInput.value) {
                    if (!validateEmail(emailInput.value)) {
                        event.preventDefault();
                        event.stopPropagation();
                        emailInput.classList.add('is-invalid');
                        showToast('Invalid email format', 'error');
                        return;
                    }
                }
                
                // Check password strength on registration form
                const passwordInput = form.querySelector('input[name="password1"]');
                if (passwordInput && passwordInput.value) {
                    if (!validatePasswordStrength(passwordInput.value)) {
                        event.preventDefault();
                        event.stopPropagation();
                        passwordInput.classList.add('is-invalid');
                        showToast('Password must be at least 8 characters with letters and numbers', 'warning');
                        return;
                    }
                }
                
                // Check if passwords match on registration form
                const password1 = form.querySelector('input[name="password1"]');
                const password2 = form.querySelector('input[name="password2"]');
                if (password1 && password2 && password1.value && password2.value) {
                    if (password1.value !== password2.value) {
                        event.preventDefault();
                        event.stopPropagation();
                        password2.classList.add('is-invalid');
                        showToast('Passwords do not match', 'error');
                        return;
                    } else {
                        password2.classList.remove('is-invalid');
                    }
                }
            }
            
            // Basic validation for all forms
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
                showToast('Please fill in all required fields', 'warning');
            }
            
            form.classList.add('was-validated');
        }, false);
        
        // Real-time validation for password confirmation
        const password2 = form.querySelector('input[name="password2"]');
        if (password2) {
            password2.addEventListener('input', function(e) {
                const password1 = form.querySelector('input[name="password1"]');
                if (password1 && this.value && password1.value !== this.value) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });
        }
        
        // Real-time validation for required fields
        const requiredInputs = form.querySelectorAll('input[required]');
        requiredInputs.forEach(function(input) {
            input.addEventListener('blur', function(e) {
                if (!this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });
            
            input.addEventListener('input', function(e) {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });
}

// ==================== PASSWORD TOGGLE ====================
function setupPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Find the password input
            let passwordInput;
            if (this.hasAttribute('data-target')) {
                passwordInput = document.getElementById(this.getAttribute('data-target'));
            } else {
                passwordInput = this.parentElement.querySelector('input[type="password"], input[type="text"]');
            }
            
            if (!passwordInput) return;
            
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
                this.title = 'Hide Password';
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
                this.title = 'Show Password';
            }
        });
    });
}

// Validate email format
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate password strength
function validatePasswordStrength(password) {
    // Minimum 8 characters, at least 1 letter and 1 number
    const re = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/;
    return re.test(password);
}

// ==================== SEARCH FUNCTIONALITY ====================
function setupSearch() {
    const searchInputs = document.querySelectorAll('[data-search]');
    
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const targetId = input.getAttribute('data-search');
            const targetTable = document.getElementById(targetId);
            
            if (!targetTable) return;
            
            const rows = targetTable.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    });
}

// ==================== FILTERS ====================
function setupFilters() {
    const filterButtons = document.querySelectorAll('[data-filter]');
    
    filterButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const filterValue = this.getAttribute('data-filter');
            const targetId = this.getAttribute('data-target');
            const targetTable = document.getElementById(targetId);
            
            if (!targetTable) return;
            
            const rows = targetTable.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const status = row.getAttribute('data-status');
                row.style.display = filterValue === 'all' || status === filterValue ? '' : 'none';
            });
            
            // Update active button
            document.querySelectorAll('[data-filter][data-target="' + targetId + '"]').forEach(function(btn) {
                btn.classList.remove('active');
            });
            button.classList.add('active');
        });
    });
}

// ==================== NOTIFICATIONS (TOAST) ====================
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} border-0 shadow-lg" 
             role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
    toastContainer.innerHTML = toastHtml;
    
    document.body.appendChild(toastContainer);
    
    const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
    toast.show();
    
    // Remove after shown
    setTimeout(function() {
        toastContainer.remove();
    }, 5000);
}

// ==================== MODAL UTILITIES ====================
function openModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

function closeModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) {
        modal.hide();
    }
}

// ==================== CONFIRMATION DIALOG ====================
function confirmAction(message = 'Are you sure?', callback) {
    if (confirm(message)) {
        callback();
    }
}

// ==================== PAGINATION ====================
function goToPage(page) {
    const url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location = url.toString();
}

// ==================== TABLE SORTING ====================
function sortTable(columnIndex) {
    const table = event.target.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    let isAscending = true;
    const header = table.querySelectorAll('th')[columnIndex];
    
    if (header.classList.contains('sort-asc')) {
        isAscending = false;
        header.classList.remove('sort-asc');
        header.classList.add('sort-desc');
    } else {
        header.classList.remove('sort-desc');
        header.classList.add('sort-asc');
    }
    
    rows.sort(function(a, b) {
        const aValue = a.children[columnIndex].textContent.trim();
        const bValue = b.children[columnIndex].textContent.trim();
        
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        } else {
            return isAscending 
                ? aValue.localeCompare(bValue) 
                : bValue.localeCompare(aValue);
        }
    });
    
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

// ==================== DATA EXPORT ====================
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    let csv = [];
    
    // Get table headers
    const headers = [];
    table.querySelectorAll('th').forEach(function(header) {
        headers.push('"' + header.textContent.trim().replace(/"/g, '""') + '"');
    });
    csv.push(headers.join(','));
    
    // Get table rows
    table.querySelectorAll('tbody tr').forEach(function(row) {
        const cells = [];
        row.querySelectorAll('td').forEach(function(cell) {
            cells.push('"' + cell.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(cells.join(','));
    });
    
    // Create and download CSV file
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// ==================== IMAGE PREVIEW ====================
function previewImage(inputSelector, previewSelector) {
    const input = document.querySelector(inputSelector);
    const preview = document.querySelector(previewSelector);
    
    if (input) {
        input.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(event) {
                    preview.innerHTML = `
                        <div class="position-relative">
                            <img src="${event.target.result}" class="img-fluid rounded" style="max-height: 200px;">
                            <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0" 
                                    onclick="document.querySelector('${inputSelector}').value=''; this.parentElement.remove();">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    `;
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
}

// ==================== DRAG & DROP ====================
function setupDragAndDrop(dropZoneSelector, inputSelector) {
    const dropZone = document.querySelector(dropZoneSelector);
    const fileInput = document.querySelector(inputSelector);
    
    if (!dropZone || !fileInput) return;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        dropZone.style.backgroundColor = '#f0f0f0';
        dropZone.style.borderColor = '#667eea';
    }
    
    function unhighlight(e) {
        dropZone.style.backgroundColor = 'transparent';
        dropZone.style.borderColor = '#bfdbfe';
    }
    
    dropZone.addEventListener('drop', handleDrop, false);
    dropZone.addEventListener('click', () => fileInput.click());
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
    }
}

// ==================== COUNTDOWN TIMER ====================
function startCountdown(seconds, callback) {
    let remaining = seconds;
    
    const interval = setInterval(function() {
        remaining--;
        
        if (callback) {
            callback(remaining);
        }
        
        if (remaining <= 0) {
            clearInterval(interval);
        }
    }, 1000);
}

// ==================== LOCAL STORAGE UTILITIES ====================
const StorageUtil = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Failed to save to localStorage:', e);
        }
    },
    
    get: function(key) {
        try {
            const value = localStorage.getItem(key);
            return value ? JSON.parse(value) : null;
        } catch (e) {
            console.error('Failed to read from localStorage:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Failed to remove from localStorage:', e);
        }
    },
    
    clear: function() {
        try {
            localStorage.clear();
        } catch (e) {
            console.error('Failed to clear localStorage:', e);
        }
    }
};

// ==================== UTILITY FUNCTIONS ====================
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(date) {
    return new Date(date).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
