document.addEventListener('DOMContentLoaded', (event) => {
    fetch('/api/game-settings/')
        .then(response => response.json())
        .then(data => {
            const gameStatus = data.game_status;
            const gameStartTime = new Date(data.start_time);
            const countdownElement = document.getElementById('countdown');

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
        });
});

function toggleVictimsPopup() {
    var popup = document.getElementById('popup-container');
    var backdrop = document.getElementById('backdrop');
    popup.classList.toggle('active');
    backdrop.classList.toggle('active');
}