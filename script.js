// Initialize scroll animations
function initializeScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = Math.random() * 0.3 + 's';
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.scroll-animate').forEach(el => {
        observer.observe(el);
    });
}

// Initialize smooth scroll navigation
function initializeNavigation() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Track analytics events
function trackEvents() {
    // Track button clicks
    document.querySelectorAll('a[href*="t.me"]').forEach(link => {
        link.addEventListener('click', () => {
            if (window.gtag) {
                window.gtag('event', 'telegram_click', {
                    'event_category': 'engagement',
                    'event_label': link.href
                });
            }
        });
    });

    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener('scroll', () => {
        const scrollPercentage = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        if (scrollPercentage > maxScroll) {
            maxScroll = scrollPercentage;
            if (scrollPercentage > 50 && window.gtag) {
                window.gtag('event', 'scroll_depth', {
                    'event_category': 'engagement',
                    'value': Math.round(scrollPercentage)
                });
            }
        }
    });
}

// Copy to clipboard utility
function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
}

// Initialize everything
document.addEventListener('DOMContentLoaded', function() {
    initializeScrollAnimations();
    initializeNavigation();
    trackEvents();

    // Register service worker for PWA
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js').catch(() => {});
    }
});