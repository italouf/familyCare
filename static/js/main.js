// Main JavaScript file for FamilyCare

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })
    
    // Water consumption progress bar animation
    const waterProgressBars = document.querySelectorAll('.water-progress');
    waterProgressBars.forEach(progressBar => {
        const value = progressBar.getAttribute('aria-valuenow');
        progressBar.style.width = value + '%';
    });
    
    // Night mode toggle functionality
    const nightModeToggle = document.querySelector('.night-mode-toggle');
    if (nightModeToggle) {
        nightModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('night-mode');
            
            // Save preference to localStorage
            const isNightMode = document.body.classList.contains('night-mode');
            localStorage.setItem('nightMode', isNightMode);
            
            // If using server-side night mode, send request to update user preference
            if (isNightMode) {
                // Example AJAX request to update night mode preference
                // fetch('/modo_noturno/toggle/', { method: 'POST' });
            }
        });
        
        // Check if night mode was previously enabled
        const isNightMode = localStorage.getItem('nightMode') === 'true';
        if (isNightMode) {
            document.body.classList.add('night-mode');
        }
    }
    
    // Emergency contact quick dial
    const emergencyButtons = document.querySelectorAll('.emergency-dial');
    emergencyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const phoneNumber = this.getAttribute('data-phone');
            const contactName = this.getAttribute('data-name');
            
            if (confirm(`Deseja ligar para ${contactName}?`)) {
                window.location.href = `tel:${phoneNumber}`;
            }
        });
    });
});