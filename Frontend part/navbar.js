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
    //  Backend Request
    fetch('http://127.0.0.1:5000/user/login', {
        method: 'POST',
        body: new URLSearchParams({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            localStorage.setItem('isLoggedIn', 'true');   
            localStorage.setItem('username', username);  
            window.location.href = 'Dashboard.html';
        } else {
            error.style.display = 'block';
            error.textContent = 'Username or password is wrong';
        }
    })
    .catch(err => {
        console.log(err);
        error.style.display = 'block';
        error.textContent = 'you are not connected';
    });
}

   























