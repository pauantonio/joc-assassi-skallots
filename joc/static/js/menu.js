document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/game-settings/')
        .then(response => response.json())
        .then(data => {
            const buttons = document.querySelectorAll('button');
            const disableUntil = new Date(data.disable_until);
            const gameStatus = data.game_status;
            const now = new Date();

            buttons.forEach(button => {
                if ((gameStatus === 'paused' || (gameStatus === 'disabled_until_time' && now < disableUntil))
                     && ['victim', 'ranking', 'cemetery'].includes(button.className)) {
                    button.disabled = true;
                }
            });
        });

    document.querySelectorAll('.buttons-list button').forEach(button => {
        button.addEventListener('click', () => {
            window.location.href = button.getAttribute('data-url');
        });
    });
});
