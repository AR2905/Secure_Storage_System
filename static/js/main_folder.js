function showKeyInput(file) {
    const modal = document.getElementById(`key-input-${file}`);
    const background = document.querySelector('body');
    
    modal.style.display = 'flex';
    background.classList.add('blur-background');
}

function sendKeys(file) {
    const key1 = document.getElementById(`key1-${file}`).value;
    const key2 = document.getElementById(`key2-${file}`).value;

    // Send the keys to your Flask API using a fetch request
    fetch(`/your-flask-endpoint?file=${file}&key1=${key1}&key2=${key2}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
        // You can handle the response from the Flask API here
    });
}
function goBack(file) {
    hideKeyInput(file);
}

function hideKeyInput(file) {
    const modal = document.getElementById(`key-input-${file}`);
    const background = document.querySelector('body');

    modal.style.display = 'none';
    background.classList.remove('blur-background');
}
