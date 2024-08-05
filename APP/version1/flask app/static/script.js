document.addEventListener('DOMContentLoaded', (event) => {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date1').value = today;
});

async function fetchDairas() {
    const wilaya = document.getElementById('wilaya').value;
    const dairaSelect = document.getElementById('daira');
    dairaSelect.innerHTML = '<option value="">اختر الدائرة</option>';

    if (wilaya) {
        const response = await fetch(`/get_dairas/${wilaya}`);
        const dairas = await response.json();
        
        dairas.forEach(daira => {
            const option = document.createElement('option');
            option.value = daira;
            option.textContent = daira;
            dairaSelect.appendChild(option);
        });
    }

    fetchBaladias(); // Clear baladias when wilaya changes
}

async function fetchBaladias() {
    const daira = document.getElementById('daira').value;
    const baladiaSelect = document.getElementById('baladia');
    baladiaSelect.innerHTML = '<option value="">اختر البلدية</option>';

    if (daira) {
        const response = await fetch(`/get_baladias/${daira}`);
        const baladias = await response.json();
        
        baladias.forEach(baladia => {
            const option = document.createElement('option');
            option.value = baladia;
            option.textContent = baladia;
            baladiaSelect.appendChild(option);
        });
    }
}


document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ username, password })
        });

        if (response.ok) {
            window.location.href = '/second_page'; // Redirect to the second page
        } else {
            const errorText = await response.text();
            document.getElementById('error-message').textContent = errorText;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = 'An error occurred. Please try again.';
    }
});

