document.addEventListener('DOMContentLoaded', (event) => {
    Promise.all([
        fetch('/api/game-settings/').then(response => response.json()),
        fetch('/api/player-victim-status/').then(response => response.json())
    ]).then(([gameData, playerVictimData]) => {
        const gameStatus = gameData.game_status;
        const playerStatus = playerVictimData.player_status;
        const victimStatus = playerVictimData.victim_status;
        const gameStartTime = new Date(gameData.start_time);
        const countdownElement = document.getElementById('countdown');

        const refreshOnStatusChange = (newGameStatus, newPlayerStatus, newVictimStatus) => {
            if (newGameStatus !== gameStatus || newPlayerStatus !== playerStatus || newVictimStatus !== victimStatus) {
                location.reload();
            }
        };

        if (countdownElement && gameStartTime) {
            const updateCountdown = () => {
                const now = new Date().getTime();
                const distance = gameStartTime - now;
    
                if (distance < 0) {
                    clearInterval(interval);
                    return;
                }
    
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
                let countdownText = '';
                if (days > 0) countdownText += `${days}d `;
                if (hours > 0) countdownText += `${hours}h `;
                if (minutes > 0) countdownText += `${minutes}m `;
                countdownText += `${seconds}s`;
    
                countdownElement.innerHTML = countdownText;
            };
    
            const interval = setInterval(updateCountdown, 1000);
            updateCountdown();
        }

        else if (gameStatus === 'paused') {
            buttonsToDisable = document.querySelector('#kill-button');
            buttonsToDisable.disabled = true;

            pauseMessage = document.querySelector('#pause-message');
            pauseMessage.style.display = 'block';
        }

        else if (gameStatus === 'finished') {
            buttonsToDisable = document.querySelector('#kill-button');
            buttonsToDisable.disabled = true;

            finishMessage = document.querySelector('#finish-message');
            finishMessage.style.display = 'block';
        }

        // Check for status changes every second
        setInterval(() => {
            Promise.all([
                fetch('/api/game-settings/').then(response => response.json()),
                fetch('/api/player-victim-status/').then(response => response.json())
            ]).then(([newGameData, newPlayerVictimData]) => {
                refreshOnStatusChange(newGameData.game_status, newPlayerVictimData.player_status, newPlayerVictimData.victim_status);
            });
        }, 1000);
    });
});