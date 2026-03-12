// Function to show alert messages
function showMessage(message, type = 'success') {
    const messageContainer = document.getElementById('messageContainer');

    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;

    const icon = type === 'success' ? 'fa-check-circle' :
        type === 'danger' ? 'fa-exclamation-circle' :
            type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';

    alertDiv.innerHTML = `
                    <i class="fas ${icon}"></i>
                    <span>${message}</span>
                `;

    messageContainer.appendChild(alertDiv);

    // Remove after 3 seconds
    setTimeout(() => {
        alertDiv.classList.add('slide-out');
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 300);
    }, 3000);
}

// Get CSRF token function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith((name || 'csrftoken') + '=')) {
                cookieValue = decodeURIComponent(cookie.substring((name || 'csrftoken').length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function reset(form, dis) {
    dis.forEach(element => {
        element.prop("disabled", true)
    });
    form[0].reset();
};