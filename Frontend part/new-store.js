// Storage update
document.getElementById('storage-size').addEventListener('input', function() {
    const size = parseInt(this.value) || 2;
    document.getElementById('total-storage').textContent = size + 1;
});

// Password generate
function generatePassword() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$!';
    let password = '';
    for (let i = 0; i < 16; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    document.getElementById('admin-password').value = password;
}

// Password copy
function copyPassword() {
    const password = document.getElementById('admin-password').value;
    navigator.clipboard.writeText(password);
    alert('Password copied!');
}

// Add product
document.getElementById('add-product-btn').addEventListener('click', function() {
    const row = document.createElement('div');
    row.className = 'product-row';
    row.innerHTML = `
        <input type="text" placeholder="Product Name">
        <input type="number" placeholder="Price">
        <input type="text" placeholder="Description">
        <button class="delete-product" onclick="this.parentElement.remove()">🗑</button>
    `;
    document.getElementById('products-list').appendChild(row);
});

// Existing delete buttons
document.querySelectorAll('.delete-product').forEach(function(btn) {
    btn.addEventListener('click', function() {
        btn.parentElement.remove();
    });
});

// Launch store
function launchStore() {
    const password = document.getElementById('admin-password').value;
    if (!password) {
        alert('Password is required');
        return;
    }
    alert('Store is launch !!');
    window.location.href = 'Dashboard.html';
}