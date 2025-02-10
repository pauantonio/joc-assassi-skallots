document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.buttons-list button').forEach(button => {
        button.addEventListener('click', () => {
            window.location.href = button.getAttribute('data-url');
        });
    });
});
