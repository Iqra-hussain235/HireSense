/**
 * HireSense AI - Custom Animations
 * Smooth animations and interactive effects
 */

// Initialize animations when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeScrollAnimations();
    initializeHoverEffects();
    initializeLoaderAnimations();
    initializeCardEffects();
});

/**
 * Initialize all animations
 */
function initializeAnimations() {
    // Fade in elements
    const fadeElements = document.querySelectorAll('.animate-fade-in');
    fadeElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Slide in elements
    const slideElements = document.querySelectorAll('.animate-slide-in');
    slideElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Scale in elements
    const scaleElements = document.querySelectorAll('.animate-scale-in');
    scaleElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
    });
}

/**
 * Initialize scroll-based animations
 */
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements with scroll-animation class
    const scrollElements = document.querySelectorAll('.scroll-animation');
    scrollElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

/**
 * Initialize hover effects
 */
function initializeHoverEffects() {
    // 3D card effect
    const cards3D = document.querySelectorAll('.card-3d');
    cards3D.forEach(card => {
        card.addEventListener('mousemove', handle3DCardHover);
        card.addEventListener('mouseleave', reset3DCard);
    });
    
    // Glow effect
    const glowElements = document.querySelectorAll('.glow-effect');
    glowElements.forEach(el => {
        el.addEventListener('mouseenter', activateGlow);
        el.addEventListener('mouseleave', deactivateGlow);
    });
}

/**
 * Handle 3D card hover
 */
function handle3DCardHover(e) {
    const card = this;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;
    
    const inner = card.querySelector('.card-3d-inner');
    if (inner) {
        inner.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    }
}

/**
 * Reset 3D card
 */
function reset3DCard() {
    const inner = this.querySelector('.card-3d-inner');
    if (inner) {
        inner.style.transform = 'rotateX(0) rotateY(0)';
    }
}

/**
 * Activate glow effect
 */
function activateGlow() {
    this.style.boxShadow = '0 0 30px rgba(99, 102, 241, 0.5)';
}

/**
 * Deactivate glow effect
 */
function deactivateGlow() {
    this.style.boxShadow = '';
}

/**
 * Initialize loader animations
 */
function initializeLoaderAnimations() {
    // Progress step animations
    const progressSteps = document.querySelectorAll('.progress-step');
    progressSteps.forEach((step, index) => {
        setTimeout(() => {
            step.classList.add('active');
        }, index * 500);
        
        setTimeout(() => {
            step.classList.remove('active');
            step.classList.add('completed');
        }, index * 500 + 2000);
    });
}

/**
 * Initialize card effects
 */
function initializeCardEffects() {
    const cards = document.querySelectorAll('.premium-glass-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', handleCardHover);
        card.addEventListener('mouseleave', handleCardLeave);
    });
}

/**
 * Handle card hover
 */
function handleCardHover(e) {
    const card = this;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
}

/**
 * Handle card leave
 */
function handleCardLeave() {
    this.style.removeProperty('--mouse-x');
    this.style.removeProperty('--mouse-y');
}

/**
 * Smooth scroll to element
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Typing animation for text
 */
function typeText(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

/**
 * Counter animation for numbers
 */
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

/**
 * Initialize counter animations
 */
function initializeCounters() {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        if (target) {
            animateCounter(counter, target);
        }
    });
}

/**
 * Tab switching animation
 */
function switchTab(tabId) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Add active class to clicked tab
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    
    // Hide all tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
        content.style.opacity = '0';
    });
    
    // Show selected tab content with animation
    const selectedContent = document.getElementById(tabId);
    if (selectedContent) {
        selectedContent.style.display = 'block';
        setTimeout(() => {
            selectedContent.style.opacity = '1';
            selectedContent.style.transition = 'opacity 0.3s ease';
        }, 10);
    }
}

/**
 * Accordion animation
 */
function toggleAccordion(header) {
    const content = header.nextElementSibling;
    const isOpen = content.classList.contains('open');
    
    // Close all accordions
    document.querySelectorAll('.accordion-content').forEach(c => {
        c.classList.remove('open');
        c.style.maxHeight = '0';
    });
    
    // Open clicked accordion if it was closed
    if (!isOpen) {
        content.classList.add('open');
        content.style.maxHeight = content.scrollHeight + 'px';
    }
}

/**
 * File upload drag and drop
 */
function initializeFileUpload() {
    const dropZone = document.querySelector('.file-upload');
    if (!dropZone) return;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        });
    });
    
    dropZone.addEventListener('drop', handleDrop);
}

/**
 * Handle file drop
 */
function handleDrop(e) {
    const files = e.dataTransfer.files;
    handleFiles(files);
}

/**
 * Handle files
 */
function handleFiles(files) {
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.files = files;
        // Trigger change event
        const event = new Event('change');
        fileInput.dispatchEvent(event);
    }
}

/**
 * Show loading state
 */
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
        <div class="loader-container">
            <div class="loader-spinner"></div>
            <div class="loader-text">Processing...</div>
            <div class="progress-steps">
                <div class="progress-step active">
                    <span class="progress-step-icon">🧠</span>
                    Reading Resume...
                </div>
                <div class="progress-step">
                    <span class="progress-step-icon">✓</span>
                    Extracting Text
                </div>
                <div class="progress-step">
                    <span class="progress-step-icon">✓</span>
                    OCR Processing
                </div>
                <div class="progress-step">
                    <span class="progress-step-icon">✓</span>
                    Finding Skills
                </div>
                <div class="progress-step">
                    <span class="progress-step-icon">✓</span>
                    Calculating ATS
                </div>
                <div class="progress-step">
                    <span class="progress-step-icon">✓</span>
                    Almost Ready...
                </div>
            </div>
        </div>
    `;
}

/**
 * Hide loading state
 */
function hideLoading(containerId, content) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = content;
    container.style.opacity = '0';
    container.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        container.style.opacity = '1';
    }, 10);
}

/**
 * Update progress step
 */
function updateProgressStep(stepIndex, status) {
    const steps = document.querySelectorAll('.progress-step');
    if (steps[stepIndex]) {
        steps[stepIndex].classList.remove('active', 'completed');
        if (status === 'active') {
            steps[stepIndex].classList.add('active');
        } else if (status === 'completed') {
            steps[stepIndex].classList.add('completed');
        }
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        padding: 16px 24px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius-md);
        color: var(--text-primary);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

/**
 * Parallax effect for background
 */
function initializeParallax() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(el => {
            const speed = el.getAttribute('data-speed') || 0.5;
            el.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

/**
 * Magnetic button effect
 */
function initializeMagneticButtons() {
    const buttons = document.querySelectorAll('.btn-primary');
    
    buttons.forEach(button => {
        button.addEventListener('mousemove', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            button.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translate(0, 0)';
        });
    });
}

/**
 * Initialize all interactive effects
 */
function initializeInteractiveEffects() {
    initializeFileUpload();
    initializeParallax();
    initializeMagneticButtons();
}

// Export functions for use in Streamlit
if (typeof window !== 'undefined') {
    window.HireSenseAnimations = {
        smoothScrollTo,
        typeText,
        animateCounter,
        switchTab,
        toggleAccordion,
        showLoading,
        hideLoading,
        updateProgressStep,
        showToast,
        initializeInteractiveEffects
    };
}
