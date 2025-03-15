document.addEventListener('DOMContentLoaded', () => {
    const profilePictureInput = document.getElementById('profile-picture-input');
    profilePictureInput.addEventListener('change', () => {
        if (profilePictureInput.files.length) {
            document.getElementById('profile-form').submit();
        }
    });

    fetch('/api/game-settings/')
        .then(response => response.json())
        .then(data => {
            if (data.game_status === 'finished') {
                profilePictureInput.style.display = 'none';
            }
        });
});