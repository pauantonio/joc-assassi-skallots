document.addEventListener('DOMContentLoaded', (event) => {
    const countdownElement = document.getElementById('countdown');
    if (countdownElement) {
        const dateAttribute = countdownElement.getAttribute('start-time');
        if (!dateAttribute) {
            console.error('Missing start-time attribute in countdown element');
            return;
        }
        const targetDate = Date.parse(dateAttribute);

        const updateCountdown = () => {
            const now = new Date().getTime();
            const distance = targetDate - now;

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
});