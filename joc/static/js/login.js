const sessionCookieInput = document.getElementById('session_cookie');
sessionCookieInput.value = document.cookie.replace(/(?:(?:^|.*;\s*)sessionid\s*\=\s*([^;]*).*$)|^.*$/, "$1");

document.addEventListener('DOMContentLoaded', function() {
    const errorElement = document.getElementById('login-error');
    const infoElement = document.getElementById('login-info');
    const codeInputs = document.querySelectorAll('.code-inputs input');
    const birthDateInputs = document.querySelectorAll('.birth-date-inputs input');
    const codeHiddenInput = document.getElementById('code');
    const birthDateHiddenInput = document.getElementById('birth_date');
    const loginForm = document.getElementById('login-form');
    const loginButton = loginForm.querySelector('button[type="submit"]');

    checkFormValidity();

    function checkFormValidity() {
        let allFilled = true;
        codeInputs.forEach(input => {
            if (!input.value) {
                allFilled = false;
            }
        });
        if (birthDateInputs[0].value.length !== 2 || birthDateInputs[1].value.length !== 2 || birthDateInputs[2].value.length !== 4) {
            allFilled = false;
        }
        loginButton.disabled = !allFilled;
    }

    function validateInput(input) {
        input.value = input.value.replace(/\D/g, '');
        if (input.value.length > input.maxLength) {
            input.value = input.value.slice(0, input.maxLength);
        }
    }

    function preventPaste(event) {
        event.preventDefault();
    }

    if (errorElement) {
        infoElement.style.display = 'none';
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                errorElement.style.display = 'none';
                infoElement.style.display = 'block';
            });
        });

        // Restore code input values from hidden input
        const codeValue = codeHiddenInput.value;
        if (codeValue) {
            codeInputs.forEach((input, index) => {
                input.value = codeValue[index] || '';
            });
        }

        // Restore birth date input values from hidden input
        const birthDateValue = birthDateHiddenInput.value;
        if (birthDateValue) {
            const [year, month, day] = birthDateValue.split('-');
            birthDateInputs[0].value = day;
            birthDateInputs[1].value = month;
            birthDateInputs[2].value = year;
        }
    }

    codeInputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            validateInput(input);
            if (input.value.length === 1) {
                if (index < codeInputs.length - 1) {
                    codeInputs[index + 1].focus();
                } else {
                    birthDateInputs[0].focus();
                }
            }
            checkFormValidity();
        });
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                codeInputs[index - 1].focus();
            }
            checkFormValidity();
        });
        input.addEventListener('paste', preventPaste);
    });

    birthDateInputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            validateInput(input);
            if (input.value.length === input.maxLength) {
                if (index < birthDateInputs.length - 1) {
                    birthDateInputs[index + 1].focus();
                } else {
                    loginButton.focus();
                }
            }
            checkFormValidity();
        });
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                birthDateInputs[index - 1].focus();
            }
            checkFormValidity();
        });
        input.addEventListener('paste', preventPaste);
    });

    loginForm.addEventListener('submit', (e) => {
        let codeValue = '';
        codeInputs.forEach(input => {
            codeValue += input.value;
        });
        codeHiddenInput.value = codeValue;

        const year = birthDateInputs[2].value;
        const month = birthDateInputs[1].value.padStart(2, '0');
        const day = birthDateInputs[0].value.padStart(2, '0');
        birthDateHiddenInput.value = `${year}-${month}-${day}`;
    });
});
