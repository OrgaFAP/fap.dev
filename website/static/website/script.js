// Theme management
const html = document.documentElement;
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

// Check for saved theme preference or default to light mode
function getTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        return savedTheme;
    }

    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }

    return 'light';
}

function setTheme(theme) {
    if (theme === 'dark') {
        html.classList.add('dark');
        themeIcon.textContent = '☀️';
    } else {
        html.classList.remove('dark');
        themeIcon.textContent = '🌙';
    }
    localStorage.setItem('theme', theme);
}

// Initialize theme
setTheme(getTheme());

// Toggle theme on button click
themeToggle.addEventListener('click', () => {
    const currentTheme = html.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
});

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
    }
});

// Typewriter animation for h1
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    element.style.opacity = '1';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// Initialize typewriter effect on page load
window.addEventListener('DOMContentLoaded', () => {
    const h1 = document.querySelector('main h1');
    if (h1) {
        const originalText = h1.textContent;
        h1.style.opacity = '0';
        setTimeout(() => {
            typeWriter(h1, originalText, 80);
        }, 300);
    }
});
