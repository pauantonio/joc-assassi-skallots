function togglePopup() {
    var popup = document.getElementById('popup-container');
    var backdrop = document.getElementById('backdrop');
    popup.classList.toggle('active');
    backdrop.classList.toggle('active');
}