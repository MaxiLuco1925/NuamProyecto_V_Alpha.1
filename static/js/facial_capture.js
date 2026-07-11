/**
 * Utilidades de captura facial para NUAM.
 * - iniciarCamara: pide permiso y muestra el stream en el <video>.
 * - capturarFrame: dibuja el frame actual en un <canvas> oculto y lo devuelve como base64 JPEG.
 * - obtenerCSRFToken: lee el token CSRF que Django ya deja en el DOM (cookie o input oculto).
 */

async function iniciarCamara(idVideo) {
    const video = document.getElementById(idVideo);
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 360, height: 270, facingMode: "user" },
            audio: false,
        });
        video.srcObject = stream;
    } catch (err) {
        alert("No se pudo acceder a la cámara. Revisa los permisos del navegador.");
        console.error(err);
    }
}

function capturarFrame(idVideo, idCanvas) {
    const video = document.getElementById(idVideo);
    const canvas = document.getElementById(idCanvas);
    const contexto = canvas.getContext('2d');
    contexto.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.85); // data:image/jpeg;base64,...
}

function obtenerCSRFToken() {
    const cookie = document.cookie
        .split('; ')
        .find((fila) => fila.startsWith('csrftoken='));
    if (cookie) return cookie.split('=')[1];

    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
}
