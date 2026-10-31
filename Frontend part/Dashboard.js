document.addEventListener('DOMContentLoaded', function() {

    const token = localStorage.getItem('token');

    fetch('http://127.0.0.1:5000/store/getall', {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
        .then(response => response.json())
        .then(stores => {

            // Store Count Update
            document.getElementById('store-count').textContent = `${stores.length} / 3`;

            // Total Storage Calculate
            let totalStorage = 0;
            stores.forEach(function(store) {
                totalStorage += parseInt(store.storage);
            });
            document.getElementById('storage-count').textContent = `${totalStorage} / 5`;

            stores.forEach(function(store) {
                const card = document.createElement('div');
                card.className = `store-card ${store.status}`;

                // Ingress abhi nahi hai, isliye store kholne ke liye port-forward command dikhate hain
                const openCmd = `kubectl port-forward -n store-${store.store_id} svc/wordpress 8081:80`;

                card.innerHTML = `
                    <div class="card-top">
                        <span class="store-name">Store: ${store.store_id}</span>
                        <span class="badge ${store.status}">${store.status.toUpperCase()}</span>
                    </div>
                    <div class="card-info">
                        <div class="info-row">🌐 Open: <code>${openCmd}</code> then http://localhost:8081</div>
                        <div class="info-row">📦 Store ID: ${store.store_id}</div>
                        <div class="info-row">👤 User ID: ${store.user_id}</div>
                        <div class="info-row">💾 ${store.storage} Storage</div>
                        <div class="info-row">📅 Created: ${store.created_at}</div>
                    </div>
                    <div class="card-actions">
                        <button class="btn-delete" onclick="deleteStore(${store.id})">🗑 Delete</button>
                    </div>
                `;

                document.getElementById('stores-container').appendChild(card);
            });

            // Koi store provisioning mein hai to 10 second baad page refresh (status badalne ke liye)
            if (stores.some(function(s) { return s.status === 'provisioning'; })) {
                setTimeout(function() { location.reload(); }, 10000);
            }
        })
        .catch(err => {
            console.log('Error:', err);
        });

    document.querySelector('.btn-create').addEventListener('click', function() {
        window.location.href = 'new-store.html';
    });

});

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}

function deleteStore(id) {
    if (confirm('Store delete karna chahte ho?')) {
        const token = localStorage.getItem('token');

        fetch(`http://127.0.0.1:5000/store/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        });
    }
}