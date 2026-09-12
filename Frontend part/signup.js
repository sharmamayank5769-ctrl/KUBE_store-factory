document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('signup-btn').addEventListener('click', function() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const error = document.getElementById('error');

        if (username === '' || password === '') {
            error.style.display = 'block';
            error.textContent = 'fill the username or password';
            return;
        }

        fetch('http://127.0.0.1:5000/user/addone', {
            method: 'POST',
            body: new URLSearchParams({
                username: username,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            alert('sucessfully created account');
            window.location.href = 'index.html';
        })
        .catch(err => {
            console.log(err);
            error.style.display = 'block';
            error.textContent = 'something went wrong';
        });
    });

});