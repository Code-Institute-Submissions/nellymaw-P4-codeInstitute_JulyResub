window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    alertTimeOut();
    document.getElementById('dismissible-alert').addEventListener('click', dismissAlert);
});

function alertTimeOut() {
    setTimeout(() => { $("#dismissible-alert").fadeOut(1500); }, 1000);

}

function dismissAlert() {
    document.getElementById('dismissible-alert').style.display = 'none';
}