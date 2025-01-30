document.addEventListener('DOMContentLoaded', () => {
    const profilePictureInput = document.getElementById('profile-picture-input');
    profilePictureInput.addEventListener('change', () => {
        if (profilePictureInput.files.length) {
            document.getElementById('profile-form').submit();
        }
    });
});