console.log("JS is load !");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM is ready");

    // Password generate
    document.getElementById('generate-btn').addEventListener('click', function() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$!';
        let password = '';
        for (let i = 0; i < 16; i++) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        document.getElementById('admin-password').value = password;
    });

    // Password copy
    document.getElementById('copy-btn').addEventListener('click', function() {
        const password = document.getElementById('admin-password').value;
        navigator.clipboard.writeText(password);
        alert('Password copied!');
    });

    
    document.getElementById('launch-btn').addEventListener('click', function() {

    // check store
        fetch('http://127.0.0.1:5000/store/getall')
            .then(response => response.json())
            .then(stores => {

                if (stores.length >= 3) {
                    alert('Store limit reached (3/3). delete any one store');
                    return;
                }

                
                const storage = document.getElementById('storage-size').value;
                const storeId = Math.random().toString(36).substring(2, 10);

                fetch('http://127.0.0.1:5000/store/addone', {
                    method: 'POST',
                    body: new URLSearchParams({
                        store_id: storeId,
                        user_id: 1,
                        storage: storage + 'Gi'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    window.location.href = 'Dashboard.html';
                })
                .catch(err => {
                    console.log(err);
                    alert('Store has some problem');
                });

            })
            .catch(err => {
                console.log(err);
                alert('Could not check store limit');
            });
    });

    // Cancel button
    document.getElementById('cancel-btn').addEventListener('click', function() {
        window.location.href = 'Dashboard.html';
    });

    // Close button
    document.getElementById('close-btn').addEventListener('click', function() {
        window.location.href = 'Dashboard.html';
    });

});