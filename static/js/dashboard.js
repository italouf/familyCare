/* Dashboard JavaScript for FamilyCare Redesign */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize draggable cards
    initDraggableCards();
    
    // Initialize water progress
    updateWaterProgress();
    
    // Initialize mood tracker
    initMoodTracker();
    
    // Initialize floating action button
    initFloatingActionButton();
    
    // Initialize night mode toggle
    initNightModeToggle();
    
    // Initialize emergency dial buttons
    initEmergencyDialButtons();
    
    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initHealthChart();
    }
    
    // Initialize carousels
    initCarousels();
    
    // Show welcome toast
    showToast('Bem-vindo ao seu Dashboard!', 'Seu painel personalizado está pronto.');
});

// Draggable Cards Functionality
function initDraggableCards() {
    const containers = document.querySelectorAll('.draggable-container');
    
    if (containers.length === 0) return;
    
    containers.forEach(container => {
        const cards = container.querySelectorAll('.draggable-card');
        
        cards.forEach(card => {
            card.addEventListener('dragstart', () => {
                card.classList.add('dragging');
            });
            
            card.addEventListener('dragend', () => {
                card.classList.remove('dragging');
                // Save the new order to user preferences
                saveCardOrder();
            });
        });
        
        container.addEventListener('dragover', e => {
            e.preventDefault();
            const draggingCard = document.querySelector('.dragging');
            if (!draggingCard) return;
            
            const afterElement = getDragAfterElement(container, e.clientY);
            if (afterElement) {
                container.insertBefore(draggingCard, afterElement);
            } else {
                container.appendChild(draggingCard);
            }
        });
    });
}

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable-card:not(.dragging)')];
    
    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

function saveCardOrder() {
    // This function would save the card order to user preferences
    // For example, using localStorage or sending to server
    const containers = document.querySelectorAll('.draggable-container');
    const order = {};
    
    containers.forEach((container, containerIndex) => {
        const cards = container.querySelectorAll('.draggable-card');
        order[containerIndex] = [];
        
        cards.forEach(card => {
            order[containerIndex].push(card.dataset.cardId);
        });
    });
    
    // For demo, just save to localStorage
    localStorage.setItem('cardOrder', JSON.stringify(order));
}

// Water Progress Functionality
function updateWaterProgress() {
    const progressBar = document.querySelector('.water-progress');
    if (!progressBar) return;
    
    const percentage = progressBar.getAttribute('aria-valuenow') || 0;
    progressBar.style.width = `${percentage}%`;
    
    // Update circular progress if exists
    const circularProgress = document.querySelector('.circular-progress');
    if (circularProgress) {
        circularProgress.style.setProperty('--progress', `${percentage * 3.6}deg`);
        circularProgress.querySelector('span').textContent = `${percentage}%`;
    }
}

// Mood Tracker Functionality
function initMoodTracker() {
    const moodEmojis = document.querySelectorAll('.mood-emoji');
    if (moodEmojis.length === 0) return;
    
    moodEmojis.forEach(emoji => {
        emoji.addEventListener('click', function() {
            // Remove selected class from all emojis
            moodEmojis.forEach(e => e.classList.remove('selected'));
            
            // Add selected class to clicked emoji
            this.classList.add('selected');
            
            // Save mood selection
            const mood = this.dataset.mood;
            saveMoodSelection(mood);
            
            // Show confirmation toast
            showToast('Humor Registrado', `Você está se sentindo ${getMoodText(mood)} hoje.`);
        });
    });
}

function getMoodText(mood) {
    const moods = {
        'great': 'ótimo',
        'good': 'bem',
        'neutral': 'neutro',
        'bad': 'mal',
        'terrible': 'terrível'
    };
    
    return moods[mood] || mood;
}

function saveMoodSelection(mood) {
    // This function would save the mood selection
    // For demo, just save to localStorage
    localStorage.setItem('currentMood', mood);
    localStorage.setItem('lastMoodDate', new Date().toISOString());
}

// Floating Action Button Functionality
function initFloatingActionButton() {
    const fab = document.querySelector('.floating-action-btn');
    if (!fab) return;
    
    fab.addEventListener('click', function() {
        // Show action menu or modal
        const actionMenu = document.getElementById('action-menu');
        if (actionMenu) {
            actionMenu.classList.toggle('show');
        } else {
            // If no menu exists, show modal for adding new item
            showAddItemModal();
        }
    });
}

function showAddItemModal() {
    // This would show a modal for adding new items
    // For demo purposes, we'll just show an alert
    alert('Funcionalidade para adicionar novo item será implementada em breve!');
}

// Night Mode Toggle Functionality
function initNightModeToggle() {
    const toggles = document.querySelectorAll('.night-mode-toggle, .night-mode-toggle-float');
    if (toggles.length === 0) return;
    
    // Check if night mode is already enabled
    const isNightMode = localStorage.getItem('nightMode') === 'true';
    if (isNightMode) {
        document.body.classList.add('night-mode');
        toggles.forEach(toggle => {
            if (toggle.type === 'checkbox') {
                toggle.checked = true;
            }
        });
    }
    
    toggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const isNowNightMode = document.body.classList.toggle('night-mode');
            localStorage.setItem('nightMode', isNowNightMode);
            
            // Sync all toggles
            toggles.forEach(t => {
                if (t.type === 'checkbox') {
                    t.checked = isNowNightMode;
                }
            });
            
            // Show confirmation toast
            const message = isNowNightMode ? 'Modo noturno ativado' : 'Modo noturno desativado';
            showToast('Configuração Salva', message);
        });
    });
}

// Emergency Dial Buttons Functionality
function initEmergencyDialButtons() {
    const dialButtons = document.querySelectorAll('.emergency-dial');
    if (dialButtons.length === 0) return;
    
    dialButtons.forEach(button => {
        button.addEventListener('click', function() {
            const phone = this.dataset.phone;
            const name = this.dataset.name;
            
            // In a real app, this would trigger a call
            // For demo, just show confirmation
            showToast('Ligando...', `Iniciando chamada para ${name}: ${phone}`);
        });
    });
}

// Health Chart Functionality
function initHealthChart() {
    const chartCanvas = document.getElementById('healthChart');
    if (!chartCanvas) return;
    
    const ctx = chartCanvas.getContext('2d');
    
    // Sample data - in a real app, this would come from the backend
    const data = {
        labels: ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
        datasets: [
            {
                label: 'Consumo de Água (ml)',
                data: [1500, 2000, 1800, 2200, 1600, 1900, 2100],
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                tension: 0.4,
                fill: true
            },
            {
                label: 'Atividade Física (min)',
                data: [30, 45, 0, 60, 20, 0, 45],
                borderColor: '#20c997',
                backgroundColor: 'rgba(32, 201, 151, 0.1)',
                tension: 0.4,
                fill: true
            }
        ]
    };
    
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Carousel Functionality
function initCarousels() {
    // This assumes you're using Bootstrap's carousel
    // If using a custom carousel, additional initialization would be needed
    const carousels = document.querySelectorAll('.carousel');
    if (carousels.length === 0) return;
    
    // Bootstrap 5 automatically initializes carousels
    // This is just for any additional customization
    carousels.forEach(carousel => {
        // Example: set interval to 5 seconds
        carousel.setAttribute('data-bs-interval', '5000');
    });
}

// Toast Notification Functionality
function showToast(title, message) {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">${title}</strong>
                <small>Agora</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    document.querySelector('.toast-container').insertAdjacentHTML('beforeend', toastHTML);
    
    // Initialize and show the toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 5000 });
    toast.show();
    
    // Remove toast from DOM after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}