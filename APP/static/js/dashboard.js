document.addEventListener('DOMContentLoaded', function () {
    const scanForm = document.getElementById('scanForm');
    const scanInput = document.getElementById('scanInput');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const searchInput = document.getElementById('searchInput');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const toggleBtn = document.querySelector('.toggle-btn');

    // Handle form submission for scanning
    scanForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const urlToScan = scanInput.value.trim();

        if (!urlToScan) {
            alert("Please enter a URL to scan.");
            return;
        }

        loadingSpinner.style.display = 'block';

        fetch('/admin/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // Include JWT cookie
            body: JSON.stringify({ url: urlToScan })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to scan the URL. Please try again later.');
            }
            return response.json();
        })
        .then(data => {
            alert('Scan complete! Check the results on the dashboard.');
            updateDashboard(data);
        })
        .catch(error => {
            alert(error.message);
        })
        .finally(() => {
            loadingSpinner.style.display = 'none';
        });
    });

    // Update dashboard metrics and cards
    function updateDashboard(data) {
        document.getElementById('total-threats').textContent = data.total_threats || '0';
        document.getElementById('recent-scans').textContent = data.recent_scans || '0';
        document.getElementById('last-updated').textContent = data.last_updated || 'N/A';

        const cardsContainer = document.getElementById('cardsContainer');
        cardsContainer.innerHTML = '';

        if (Array.isArray(data.threats)) {
            data.threats.forEach(threat => {
                const card = document.createElement('div');
                card.classList.add('threat-card');
                card.innerHTML = `
                    <div class="card-content">
                        <h4>${threat.name}</h4>
                        <p class="description">${threat.description}</p>
                    </div>
                `;
                cardsContainer.appendChild(card);
            });
        }
    }

    // Live search filtering
    searchInput.addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        document.querySelectorAll('.threat-card').forEach(card => {
            const text = card.querySelector('.description').textContent.toLowerCase();
            card.style.display = text.includes(searchTerm) ? 'block' : 'none';
        });
    });

    // Toggle sidebar visibility
    window.toggleSidebar = function() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    };

    // Close sidebar when overlay is clicked
    overlay.addEventListener('click', function () {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });
});

// CSV download function
function downloadCSV() {
    fetch('/admin/export-csv', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) throw new Error("Failed to download CSV");
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'threat_data.csv';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        alert("Error: " + error.message);
    });
}

// Logout function
function logout() {
    fetch('/logout', {
        method: 'GET',
        credentials: 'include'
    })
    .then(() => {
        window.location.href = '/';
    });
}
