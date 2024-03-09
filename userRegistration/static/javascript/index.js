const confirmMessage = () => {
    alert('Your message has been sent.')
}

document.getElementById('submit').onsubmit = confirmMessage;