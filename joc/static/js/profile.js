const profilePictureInput = document.getElementById('profile-picture-input');
profilePictureInput.addEventListener('change', function() {
    if (this.files.length) {
        const profileForm = document.getElementById('profile-form');
        profileForm.submit();
    }
});