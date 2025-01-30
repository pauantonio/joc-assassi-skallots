document.addEventListener('DOMContentLoaded', function() {
    const sessionCookieInput = document.getElementById('session_cookie');
    sessionCookieInput.value = document.cookie.replace(/(?:(?:^|.*;\s*)sessionid\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    const errorElement = document.getElementById('login-error');
    const infoElement = document.getElementById('login-info');
    const codeInputs = document.querySelectorAll('.code-inputs input');
    const birthDateInputs = document.querySelectorAll('.birth-date-inputs input');
    const codeHiddenInput = document.getElementById('code');
    const birthDateHiddenInput = document.getElementById('birth_date');
    const loginForm = document.getElementById('login-form');
    const loginButton = loginForm.querySelector('button[type="submit"]');

    function checkFormValidity() {
        const allCodeInputsFilled = [...codeInputs].every(input => input.value);
        const dayFilled = birthDateInputs[0].value.length === 2;
        const monthFilled = birthDateInputs[1].value.length === 2;
        const yearFilled = birthDateInputs[2].value.length === 4;

        const allFilled = allCodeInputsFilled && dayFilled && monthFilled && yearFilled;
        loginButton.disabled = !allFilled;
    }

    function validateInput(input) {
        input.value = input.value.replace(/\D/g, '').slice(0, input.maxLength);
    }

    function preventPaste(event) {
        event.preventDefault();
    }

    function restoreInputValues() {
        const codeValue = codeHiddenInput.value;
        if (codeValue) {
            codeInputs.forEach((input, index) => {
                input.value = codeValue[index] || '';
            });
        }

        const birthDateValue = birthDateHiddenInput.value;
        if (birthDateValue) {
            const [year, month, day] = birthDateValue.split('-');
            birthDateInputs[0].value = day || '';
            birthDateInputs[1].value = month || '';
            birthDateInputs[2].value = year || '';
        }
    }

    function handleInputEvent(input, index, inputsArray, nextFocusElement) {
        validateInput(input);
        checkFormValidity();
        const isLastInput = index === inputsArray.length - 1;
        const isInputFilled = input.value.length === input.maxLength;

        if (isInputFilled && !isLastInput) {
            inputsArray[index + 1].focus();
        } else if (isInputFilled && nextFocusElement) {
            nextFocusElement.focus();
        }
    }

    function handleKeyDownEvent(event, input, index, inputsArray) {
        checkFormValidity();
        if (event.key === 'Backspace' && input.value === '' && index > 0) {
            inputsArray[index - 1].focus();
        }
    }

    if (errorElement) {
        infoElement.style.display = 'none';
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', () => {
                errorElement.style.display = 'none';
                infoElement.style.display = 'block';
            });
        });
        restoreInputValues();
    }

    codeInputs.forEach((input, index) => {
        input.addEventListener('input', () => handleInputEvent(input, index, codeInputs, birthDateInputs[0]));
        input.addEventListener('keydown', (e) => handleKeyDownEvent(e, input, index, codeInputs));
        input.addEventListener('paste', preventPaste);
    });

    birthDateInputs.forEach((input, index) => {
        input.addEventListener('input', () => handleInputEvent(input, index, birthDateInputs, loginButton));
        input.addEventListener('keydown', (e) => handleKeyDownEvent(e, input, index, birthDateInputs));
        input.addEventListener('paste', preventPaste);
    });

    loginForm.addEventListener('submit', (e) => {
        codeHiddenInput.value = [...codeInputs].map(input => input.value).join('');
        const year = birthDateInputs[2].value;
        const month = birthDateInputs[1].value.padStart(2, '0');
        const day = birthDateInputs[0].value.padStart(2, '0');
        birthDateHiddenInput.value = `${year}-${month}-${day}`;
    });

    checkFormValidity();
});
