document.addEventListener('DOMContentLoaded', () => {
    const profilePictureInput = document.getElementById('profile-picture-input');
    profilePictureInput.addEventListener('change', () => {
        if (profilePictureInput.files.length) {
            document.getElementById('profile-form').submit();
        }
    });
});

function toggleLogoutPopup() {
    var popup = document.getElementById('popup-container');
    var backdrop = document.getElementById('backdrop');
    popup.classList.toggle('active');
    backdrop.classList.toggle('active');
}