function toggleInfoPopup() {
    var popup = document.getElementById('info-popup');
    var backdrop = document.getElementById('backdrop');
    popup.classList.toggle('active');
    backdrop.classList.toggle('active');
}

document.getElementById('backdrop').addEventListener('click', function() {
    toggleInfoPopup();
});
