'use strict';

$(document).ready(function() {
    let urlInput = document.getElementById('urlInput');
    let form = document.getElementById('addReadinglistItemForm');

    urlInput.addEventListener('input', function() {
        urlInput.classList.remove('is-invalid');
    }, false);

    form.addEventListener('submit', function (event) {
        if (!urlInput.checkValidity()) {
            urlInput.classList.add("is-invalid");
            event.preventDefault();
            event.stopPropagation();
        }
    }, false);
});
