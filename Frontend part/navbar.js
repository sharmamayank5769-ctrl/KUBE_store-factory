function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const error = document.getElementById('error');

    // Pehla validation
    if (username === '' || password === '') {
        error.style.display = 'block';
        error.textContent = 'fill the empty space';
        return;
    }

    // Baad mein yahan Flask API call aayegi
    if (username === 'admin' && password === 'admin123') {
        alert('Login successfully!');
        window.location.href = 'Dashboard.html';
    } else {
        error.style.display = 'block';
        error.textContent = 'Username and password is wrong';
    }
}






















