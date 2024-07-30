function enableSubmitButton() {
    const input = document.getElementById('imageInput');
    const submitButton = document.getElementById('submitButton');
    const originalImage = document.getElementById('originalImage');

    submitButton.disabled = !input.files.length;

    if (input.files.length) {
        const reader = new FileReader();
        reader.onload = function (e) {
            originalImage.src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

document.body.addEventListener('htmx:configRequest', function (event) {
    if (event.detail.elt.id === 'submitButton') {
        const input = document.getElementById('imageInput');
        if (input.files.length > 0) {
            event.detail.parameters['file'] = input.files[0];
        }
    }
});

document.body.addEventListener('htmx:beforeSend', function (event) {
    if (event.detail.elt.id === 'submitButton') {
        const comparison = document.getElementById('comparison');
        comparison.innerHTML = '<div class="spinner"></div>';
    }
});

document.body.addEventListener('htmx:afterSettle', function (event) {
    if (event.detail.elt.id === 'submitButton') {
        document.getElementById('downloadButton').style.display = 'inline-block';
    }
});

function downloadImage() {
    const upscaledImage = document.querySelector('img-comparison-slider img:last-child');
    const link = document.createElement('a');
    link.href = upscaledImage.src;
    link.download = 'upscaled_image.png';
    link.click();
}