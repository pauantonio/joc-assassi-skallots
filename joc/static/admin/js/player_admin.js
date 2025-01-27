function updateEsplaiChoices() {
    const territoriZonaSelect = document.getElementById('id_territori_zona');
    const esplaiSelect = document.getElementById('id_esplai');
    const territoriZona = territoriZonaSelect.value;

    fetch('/static/json/choices.json')
        .then(response => response.json())
        .then(data => {
            const esplaiChoices = {};
            data.TERRITORIS.forEach(territori => {
                esplaiChoices[territori.zona] = territori.esplais.map(esplai => ({
                    value: esplai.id,
                    text: esplai.nom
                }));
            });

            esplaiSelect.innerHTML = '<option value="">Seleccioneu un Centre</option>';
            if (territoriZona in esplaiChoices) {
                esplaiChoices[territoriZona].forEach(choice => {
                    const option = document.createElement('option');
                    option.value = choice.value;
                    option.text = choice.text;
                    esplaiSelect.appendChild(option);
                });
                esplaiSelect.removeAttribute('disabled');
            } else {
                esplaiSelect.setAttribute('disabled', 'disabled');
            }
        });
}

document.addEventListener('DOMContentLoaded', function() {
    const territoriZonaSelect = document.getElementById('id_territori_zona');
    if (territoriZonaSelect) {
        territoriZonaSelect.insertAdjacentHTML('afterbegin', '<option value="" selected>Seleccioneu un Territori/Zona</option>');
        territoriZonaSelect.addEventListener('change', updateEsplaiChoices);
        updateEsplaiChoices();
    }
});
