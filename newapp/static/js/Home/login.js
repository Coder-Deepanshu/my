const roleBtns = document.querySelectorAll('.role-btn');
const roleInput = document.getElementById('role');
const loginBtn = document.querySelector('.login-btn');

roleBtns.forEach(btn => {
    btn.addEventListener('click', function () {
        // Remove active class from all buttons
        roleBtns.forEach(b => b.classList.remove('active'));

        // Add active class to clicked button
        this.classList.add('active');

        // Update the role value
        const role = this.getAttribute('data-role');
        roleInput.value = role;

        // Update login button style based on role
        loginBtn.className = 'login-btn';

        if (role === 'admin') {
            loginBtn.classList.add('admin');
        } else if (role === 'faculty') {
            loginBtn.classList.add('faculty');
        } else {
            loginBtn.classList.add('student');
        }
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Forgot password functionality
document.getElementById('recoverPasswordBtn').addEventListener('click', function () {
    const collegeId = document.getElementById('collegeId').value;
    const resultDiv = document.getElementById('recoveryResult');

    if (!collegeId) {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>Please enter your College ID
                </div>
            `;
        return;
    }

    // Show loading state
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Searching for your account...</p>
            </div>
        `;

    // Create form data for POST request
    const formData = new FormData();
    formData.append('collegeId', collegeId);

    // Make AJAX call to your Django view
    fetch('{% url "forgot_password" %}', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                resultDiv.innerHTML = `
                    <div class="alert alert-success">
                        <h6><i class="fas fa-check-circle me-2"></i>Account Recovery Information</h6>
                        <p><strong>Username:</strong> ${data.username}</p>
                        <p><strong>User ID:</strong> ${data.user_id}</p>
                        <p><strong>Password:</strong> ${data.password}</p>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle me-2"></i>${data.error || 'No account found with the provided College ID'}
                    </div>
                `;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>An error occurred while processing your request. Please try again.
                </div>
            `;
            console.error('Error:', error);
        });
});

// Toggle password visibility
document.querySelectorAll('.input-group-text').forEach(el => {
    if (el.querySelector('i.fa-lock')) {
        el.addEventListener('click', function () {
            const passwordInput = document.getElementById('id_password');
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            // Toggle eye icon
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
});

// Form submission with animation
document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Show loading animation
    showLoginOverlay();

    // Form data collect karein
    const formData = new FormData(this);

    // AJAX request bhejein
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                if (data.otp_required) {
                    // OTP required - redirect to OTP page
                    showSuccess(data.message || 'OTP sent to your email');
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 3000);
                } else {
                    // Direct login successful
                    showSuccess(data.message || 'Login successful!');
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 3000);
                }
            } else {
                showError(data.error || 'Login failed!');
            }
        })
        .catch(error => {
            showError('An error occurred. Please try again.');
            console.error('Error:', error);
        });
});

// Updated overlay functions
function showLoginOverlay() {
    const overlay = document.getElementById('overlay');
    const statusTitle = document.getElementById('statusTitle');
    const statusSub = document.getElementById('statusSub');
    const statusIcon = document.getElementById('statusIcon');
    const dottedRing = document.getElementById('dottedRing');

    overlay.style.display = 'flex';
    overlay.classList.add('show');
    overlay.setAttribute('aria-hidden', 'false');

    statusCard.classList.remove('success', 'error');
    statusTitle.textContent = 'Signing In';
    statusSub.textContent = 'Please wait while we authenticate your credentials';
    statusIcon.innerHTML = '<div class="loading-dots"><span></span><span></span><span></span></div>';
    dottedRing.style.animation = 'rotate 8s linear infinite';
}

// Initialize animations
document.addEventListener('DOMContentLoaded', function () {
    // Animate elements with delay
    const animatedElements = document.querySelectorAll('.animate__animated');
    animatedElements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
    });
});

// for submit the user id to verify
const submitIDBtn = document.querySelector('#submitIDBtn');
const form = document.querySelector('#userIDForm');

submitIDBtn.addEventListener('click', () => {
    const userID = document.querySelector('#userID')

    console.log(userID.value)
    showOverlay();
    fetch('/verify_collegeID/', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ 'userID': userID.value })
    })
        .then(res => res.json())
        .then(data => {
            const userIDModal = document.querySelector('#userIDModal');
            if (data.error) {
                form.reset();
                showError(data.error);
                userIDModal.style.display = 'flex';
            } else if (data.success) {
                form.reset();
                showSuccess(data.success);
                userIDModal.style.display = 'none';
            }
        })
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const overlay = document.getElementById('overlay');
const statusCard = document.getElementById('statusCard');
const statusTitle = document.getElementById('statusTitle');
const statusSub = document.getElementById('statusSub');
const statusIcon = document.getElementById('statusIcon');
const dottedRing = document.getElementById('dottedRing');

function showOverlay() {
    overlay.classList.add('show');
    overlay.setAttribute('aria-hidden', 'false');
    statusCard.classList.remove('success', 'error');
    statusTitle.textContent = 'Verifying Account';
    statusSub.textContent = 'Please wait while we verify your credentials';
    statusIcon.innerHTML = '<div class="loading-dots"><span></span><span></span><span></span></div>';
    dottedRing.style.animation = 'rotate 8s linear infinite';
}

function showSuccess(message) {
    statusCard.classList.remove('error');
    statusCard.classList.add('success');
    statusTitle.textContent = 'Verified Successfully';
    statusSub.textContent = message || 'Your account has been verified successfully';
    dottedRing.style.animation = 'none';

    setTimeout(() => {
        overlay.classList.remove('show');
        overlay.setAttribute('aria-hidden', 'true');
        // if (redirectUrl) window.location.href = redirectUrl;
    }, 3000);
}

function showError(message) {
    statusCard.classList.remove('success');
    statusCard.classList.add('error');
    statusTitle.textContent = 'Verification Failed';
    statusSub.textContent = message || 'Unable to verify your account. Please try again.';
    dottedRing.style.animation = 'none';

    setTimeout(() => {
        overlay.classList.remove('show');
        overlay.setAttribute('aria-hidden', 'true');
    }, 3000);
}

// STABLE DEVICE FINGERPRINT SYSTEM
// Persistent Storage Key
const FINGERPRINT_STORAGE_KEY = 'edutrack_device_fingerprint_v2';

// Main Stable Fingerprint Generator
async function generateStableFingerprint() {
    try {
        // Pehle localStorage se check karo
        let storedFingerprint = localStorage.getItem(FINGERPRINT_STORAGE_KEY);

        if (storedFingerprint) {
            console.log("Using stored fingerprint:", storedFingerprint);
            return storedFingerprint;
        }

        // Naya fingerprint generate karo
        console.log("Generating new stable fingerprint...");

        const fingerprintComponents = await Promise.all([
            getHardwareFingerprint(),
            getCanvasFingerprint(),
            getWebGLFingerprint(),
            getSystemFingerprint(),
            generatePersistentUUID()
        ]);

        const combinedString = fingerprintComponents.join('|');
        const finalFingerprint = hashSHA256(combinedString);

        // localStorage me save karo (10 years ke liye)
        localStorage.setItem(FINGERPRINT_STORAGE_KEY, finalFingerprint);

        console.log("New fingerprint generated:", finalFingerprint);
        return finalFingerprint;

    } catch (error) {
        console.error("Fingerprint generation failed:", error);
        return generateFallbackFingerprint();
    }
}

// Hardware-based Fingerprint (Most Stable)
async function getHardwareFingerprint() {
    const components = [];

    // CPU Cores (rarely changes)
    components.push('cpu_cores:' + (navigator.hardwareConcurrency || 'unknown'));

    // Device Memory (rarely changes)
    components.push('ram:' + (navigator.deviceMemory || 'unknown'));

    // Architecture
    components.push('platform:' + (navigator.platform || 'unknown'));

    // Max Touch Points
    components.push('touch_points:' + (navigator.maxTouchPoints || 'unknown'));

    return components.join('|');
}

// Advanced Canvas Fingerprint (Very Stable)
function getCanvasFingerprint() {
    try {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = 240;
        canvas.height = 60;

        // Complex drawing for stability
        ctx.textBaseline = 'alphabetic';
        ctx.font = '14px "Arial", "Helvetica", sans-serif';

        // Background gradient
        const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
        gradient.addColorStop(0, '#ff0000');
        gradient.addColorStop(0.5, '#00ff00');
        gradient.addColorStop(1, '#0000ff');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Complex text rendering
        ctx.fillStyle = '#ffffff';
        ctx.fillText('BrowserFingerprintStable2024', 10, 20);

        ctx.fillStyle = 'rgba(255, 255, 0, 0.7)';
        ctx.fillText('EdutrackDeviceID', 15, 40);

        // Shapes and paths
        ctx.beginPath();
        ctx.arc(200, 30, 15, 0, Math.PI * 2);
        ctx.strokeStyle = '#ff00ff';
        ctx.lineWidth = 2;
        ctx.stroke();

        return canvas.toDataURL();

    } catch (error) {
        return 'canvas_fallback_' + Math.random().toString(36).substr(2, 9);
    }
}

// WebGL Fingerprint (Hardware Specific - Very Stable)
function getWebGLFingerprint() {
    try {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

        if (!gl) return 'webgl_not_supported';

        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        const vendor = gl.getParameter(debugInfo ? debugInfo.UNMASKED_VENDOR_WEBGL : gl.VENDOR);
        const renderer = gl.getParameter(debugInfo ? debugInfo.UNMASKED_RENDERER_WEBGL : gl.RENDERER);

        // Additional WebGL parameters for stability
        const version = gl.getParameter(gl.VERSION);
        const shadingLanguageVersion = gl.getParameter(gl.SHADING_LANGUAGE_VERSION);

        return `webgl:${vendor}|${renderer}|${version}|${shadingLanguageVersion}`;

    } catch (error) {
        return 'webgl_error';
    }
}

// System Information (Relatively Stable)
function getSystemFingerprint() {
    const components = [];

    // Timezone (rarely changes for same location)
    components.push('timezone:' + Intl.DateTimeFormat().resolvedOptions().timeZone);

    // Language (rarely changes)
    components.push('language:' + navigator.language);

    // Screen properties (relatively stable)
    components.push('color_depth:' + screen.colorDepth);
    components.push('pixel_ratio:' + (window.devicePixelRatio || 1));

    // Browser features (stable)
    components.push('cookies:' + navigator.cookieEnabled);
    components.push('java:' + (navigator.javaEnabled ? navigator.javaEnabled() : false));

    return components.join('|');
}

// Generate Persistent UUID (Fallback)
function generatePersistentUUID() {
    let uuid = localStorage.getItem('edutrack_persistent_uuid');

    if (!uuid) {
        // Cryptographically strong UUID generate karo
        uuid = 'edutrack_' +
            Date.now().toString(36) +
            Math.random().toString(36).substr(2, 9) +
            performance.now().toString(36).replace('.', '');

        localStorage.setItem('edutrack_persistent_uuid', uuid);
    }

    return uuid;
}

// Advanced Hash Function (SHA-256 simulation)
function hashSHA256(str) {
    // Simple SHA-256 simulation for fingerprint
    // Production me proper crypto library use karo
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }

    // Additional processing for better distribution
    const baseHash = Math.abs(hash).toString(16);
    const timestamp = Date.now().toString(36);

    return 'edt_' + baseHash + '_' + timestamp;
}

// Fallback Fingerprint
function generateFallbackFingerprint() {
    let fallbackId = localStorage.getItem('edutrack_fallback_id');

    if (!fallbackId) {
        fallbackId = 'fallback_' +
            navigator.platform + '_' +
            navigator.hardwareConcurrency + '_' +
            Date.now().toString(36);

        localStorage.setItem('edutrack_fallback_id', fallbackId);
    }

    return fallbackId;
}

// Collect Additional Device Info for Server
function collectDeviceInfo() {
    const deviceInfo = {
        screen_resolution: screen.width + 'x' + screen.height,
        user_agent: navigator.userAgent,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        language: navigator.language,
        platform: navigator.platform,
        hardware_concurrency: navigator.hardwareConcurrency || 'unknown',
        device_memory: navigator.deviceMemory || 'unknown',
        cookie_enabled: navigator.cookieEnabled,
        touch_support: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
        pixel_ratio: window.devicePixelRatio || 1,
        localStorage_support: !!window.localStorage,
        session_storage_support: !!window.sessionStorage,
        timestamp: new Date().toISOString()
    };

    // Hidden fields me add karo
    const form = document.getElementById('loginForm');

    // Pehle existing device info fields remove karo
    const existingFields = form.querySelectorAll('input[name^="device_"]');
    existingFields.forEach(field => field.remove());

    // New fields add karo
    for (const [key, value] of Object.entries(deviceInfo)) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = `device_${key}`;
        input.value = value;
        form.appendChild(input);
    }
}

// Initialize Fingerprint on Page Load
document.addEventListener('DOMContentLoaded', function () {
    console.log("Initializing stable device fingerprint...");

    generateStableFingerprint().then(fp => {
        document.getElementById('fingerprint').value = fp;
        console.log("Stable Device Fingerprint Ready:", fp);

        // Additional backup storage
        sessionStorage.setItem('current_fingerprint', fp);

    }).catch(error => {
        console.error("Fingerprint initialization failed:", error);
        document.getElementById('fingerprint').value = generateFallbackFingerprint();
    });
});

// Form Submission Handler
document.getElementById('loginForm').addEventListener('submit', function (e) {
    // Device info collect karo
    collectDeviceInfo();

    // Fingerprint verify karo
    const fingerprint = document.getElementById('fingerprint').value;
    if (!fingerprint) {
        console.warn("No fingerprint found, generating...");
        generateStableFingerprint().then(fp => {
            document.getElementById('fingerprint').value = fp;
            console.log("Fingerprint generated for submission:", fp);
        });
    }

    console.log("Submitting login with fingerprint:", fingerprint);
});

// Recovery Mechanism - Agar fingerprint lost ho jaye
function recoverFingerprint() {
    const storedFP = localStorage.getItem(FINGERPRINT_STORAGE_KEY);
    const persistentUUID = localStorage.getItem('edutrack_persistent_uuid');
    const fallbackID = localStorage.getItem('edutrack_fallback_id');

    if (storedFP) {
        return storedFP;
    } else if (persistentUUID) {
        return hashSHA256(persistentUUID + '|' + getSystemFingerprint());
    } else if (fallbackID) {
        return fallbackID;
    } else {
        return generateStableFingerprint();
    }
}

// Periodic Fingerprint Validation (Optional)
setInterval(() => {
    const currentFP = document.getElementById('fingerprint').value;
    const storedFP = localStorage.getItem(FINGERPRINT_STORAGE_KEY);

    if (currentFP !== storedFP && storedFP) {
        console.warn("Fingerprint mismatch detected, recovering...");
        document.getElementById('fingerprint').value = storedFP;
    }
}, 30000); // Every 30 seconds check karo

// Existing form submission handler ko modify karo
const originalFormSubmit = document.getElementById('loginForm').onsubmit;
document.getElementById('loginForm').onsubmit = function (e) {
    // Pehle device info collect karo
    collectDeviceInfo();

    // Fingerprint ensure karo
    if (!document.getElementById('fingerprint').value) {
        generateStableFingerprint().then(fp => {
            document.getElementById('fingerprint').value = fp;
            // Form submit karo
            if (originalFormSubmit) {
                originalFormSubmit.call(this, e);
            } else {
                this.submit();
            }
        });
        return false;
    }

    if (originalFormSubmit) {
        return originalFormSubmit.call(this, e);
    }
};