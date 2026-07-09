document.addEventListener('DOMContentLoaded', function() {

    const stores = [
        {
            id: '2c2486f9',
            status: 'ready',
            storage: '3Gi',
            owner: 'demo_user',
            url: 'http://store-2c2486f9.storefactory.local',
            created: '2/13/2026, 5:36:09 PM',
            password: 'Wgr^3czxSs$U+F+@'
        },
        {
            id: 'a1b2c3d4',
            status: 'provisioning',
            storage: '2Gi',
            owner: 'demo_user',
            url: 'http://store-a1b2c3d4.storefactory.local',
            created: '7/2/2026, 10:15:00 AM',
            password: 'xyz123abc'
        },
        {
            id: 'def45678',
            status: 'failed',
            storage: '2Gi',
            owner: 'demo_user',
            url: 'http://store-def45678.storefactory.local',
            created: '7/1/2026, 3:20:00 PM',
            password: 'abc456def'
        },
    ];

    stores.forEach(function(store) {
        const card = document.createElement('div');
        card.className = `store-card ${store.status}`;

        card.innerHTML = `
            <div class="card-top">
                <span class="store-name">Store: ${store.id}</span>
                <span class="badge ${store.status}">${store.status.toUpperCase()}</span>
            </div>
            <div class="card-info">
                <div class="info-row">🌐 <a href="${store.url}">${store.url}</a></div>
                <div class="info-row">📦 Namespace: store-${store.id}</div>
                <div class="info-row">👤 Owner: ${store.owner}</div>
                <div class="info-row">💾 ${store.storage} Storage</div>
                <div class="info-row">📅 Created: ${store.created}</div>
            </div>
            <div class="creds">
                <div class="creds-label">CREDENTIALS</div>
                <div class="cred-row"><span>User: </span>admin</div>
                <div class="cred-row"><span>Pass: </span>${store.password}</div>
            </div>
            <div class="card-actions">
                <button class="btn-visit">Visit Store</button>
                <button class="btn-admin">Admin Panel</button>
                <button class="btn-delete" onclick="deleteStore('${store.id}')">🗑 Delete</button>
            </div>
        `;

        document.getElementById('stores-container').appendChild(card);
    });

});

function logout() {
    window.location.href = 'index.html';
}

function deleteStore(id) {
    if (confirm('Do you want to delete the store ')) {
        
        // Saare cards dhundo
        const cards = document.querySelectorAll('.store-card');
        
        // Har card check karo
        cards.forEach(function(card) {
            
            // Agar is card mein wo id hai
            if (card.innerHTML.includes(id)) {
                
                // Card hatao
                card.remove();
            }
        });
    }
}
document.querySelector('.btn-create').addEventListener('click', function(){
    window.location.href = 'new-store.html';
})