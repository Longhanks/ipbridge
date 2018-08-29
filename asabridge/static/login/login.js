'use strict';

$(document).ready(function() {
    let usernameInput = document.getElementById('usernameInput');
    let passwordInput = document.getElementById('passwordInput');
    let form = document.getElementById('loginForm');

    usernameInput.addEventListener('input', function() {
        usernameInput.classList.remove('is-invalid');
        passwordInput.classList.remove('is-invalid');
    }, false);

    passwordInput.addEventListener('input', function() {
        usernameInput.classList.remove('is-invalid');
        passwordInput.classList.remove('is-invalid');
    }, false);

    form.addEventListener('submit', function (event) {
        let valid = true;
        if (!usernameInput.checkValidity()) {
            usernameInput.classList.add("is-invalid");
            valid = false;
        }
        if (!passwordInput.checkValidity()) {
            passwordInput.classList.add("is-invalid");
            valid = false;
        }
        if (!valid) {
            event.preventDefault();
            event.stopPropagation();
        }
    }, false);
});
