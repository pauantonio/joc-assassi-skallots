const profilePictureInput = document.getElementById('profile-picture-input');
profilePictureInput?.addEventListener('change', function() {
    // @ts-ignore
    if (this.files?.length) {
        const profileForm = document.getElementById('profile-form');
        // @ts-ignore
        profileForm?.submit();
    }
});