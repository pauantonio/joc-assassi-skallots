const sessionCookieInput = document.getElementById('session_cookie');
sessionCookieInput.value = document.cookie.replace(/(?:(?:^|.*;\s*)sessionid\s*\=\s*([^;]*).*$)|^.*$/, "$1");

document.addEventListener('DOMContentLoaded', function() {
    const errorElement = document.getElementById('login-error');
    const infoElement = document.getElementById('login-info');
    if (errorElement) {
        infoElement.style.display = 'none';
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                errorElement.style.display = 'none';
                infoElement.style.display = 'block';
            });
        });
    }
});
