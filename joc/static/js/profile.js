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
            const gameStatus = data.game_status;

            if (gameStatus === 'finished') {
                const buttonsToDisable = document.querySelector('#profile-picture-input');
                buttonsToDisable.style.display = 'none';
            }
        });
});