document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const url = button.getAttribute('data-url');
            window.location.href = url;
        });
    });
});
