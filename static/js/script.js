window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    alertTimeOut();
    document.getElementById('msg').addEventListener('click', dismissAlert);
});

function alertTimeOut() {
    setTimeout(() => { $("#msg").fadeOut(1500); }, 1000);

}

function dismissAlert() {
    document.getElementById('msg').style.display = 'none';
}