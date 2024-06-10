document.addEventListener('DOMContentLoaded', (event) => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const addCardForm = document.getElementById('addCardForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            try {
                const response = await fetch('http://127.0.0.1:8000/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({ username: email, password })
                });
                const result = await response.json();
                if (response.ok) {
                    alert('Login successful!');
                    localStorage.setItem('token', result.access_token);
                    console.log('Stored Token:', localStorage.getItem('token'));

                    // Show profile section and fetch profile
                    const profileSection = document.getElementById('profile');
                    if (profileSection) {
                        profileSection.style.display = 'block';
                    }
                    fetchProfile();
                    fetchCards();
                    fetchTransactions();
                } else {
                    alert(result.detail || 'Login failed!');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Login failed!');
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;
            const email = document.getElementById('registerEmail').value;
            const phoneNumber = document.getElementById('registerPhoneNumber').value;

            try {
                const response = await fetch('http://127.0.0.1:8000/users/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password, email, phone_number: phoneNumber })
                });
                const result = await response.json();
                if (response.ok) {
                    alert('Registration successful!');
                } else {
                    alert(result.detail || 'Registration failed!');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Registration failed!');
            }
        });
    }

    async function fetchProfile() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No token found');
            }
            console.log('Fetched Token:', token);

            const response = await fetch('http://127.0.0.1:8000/users/profile', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch profile');
            }
            const profile = await response.json();
            console.log('Profile:', profile);  // Log the profile response for debugging

            document.getElementById('profileUsername').value = profile.username;
            document.getElementById('profileEmail').value = profile.email;
            document.getElementById('profilePhoneNumber').value = profile.phone_number;
        } catch (error) {
            console.error('Error fetching profile:', error);
            alert('Failed to fetch profile');
        }
    }

    async function fetchCards() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No token found');
            }

            const response = await fetch('http://127.0.0.1:8000/cards', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch cards');
            }
            const cards = await response.json();
            console.log('Cards:', cards);

            const cardList = document.getElementById('cardList');
            cardList.innerHTML = '';
            cards.forEach(card => {
                const li = document.createElement('li');
                li.textContent = `${card.number} (${card.type}) - Expires: ${card.expiration_date}`;
                cardList.appendChild(li);
            });
        } catch (error) {
            console.error('Error fetching cards:', error);
            alert('Failed to fetch cards');
        }
    }

    if (addCardForm) {
        addCardForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const number = document.getElementById('cardNumber').value;
            const expiration_date = document.getElementById('cardExpiration').value;
            const cvv = document.getElementById('cardCVV').value;
            const type = document.getElementById('cardType').value;

            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('No token found');
                }

                const response = await fetch('http://127.0.0.1:8000/cards', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ number, expiration_date, cvv, type })
                });
                const result = await response.json();
                if (response.ok) {
                    alert('Card added successfully!');
                    fetchCards();
                } else {
                    alert(result.detail || 'Failed to add card');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to add card');
            }
        });
    }

    async function fetchTransactions() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No token found');
            }

            const response = await fetch('http://127.0.0.1:8000/transactions', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch transactions');
            }
            const transactions = await response.json();
            console.log('Transactions:', transactions);

            const transactionList = document.getElementById('transactionList');
            transactionList.innerHTML = '';
            transactions.forEach(transaction => {
                const li = document.createElement('li');
                li.textContent = `Amount: ${transaction.amount}, Status: ${transaction.status}, Date: ${transaction.created_at}`;
                transactionList.appendChild(li);
            });
        } catch (error) {
            console.error('Error fetching transactions:', error);
            alert('Failed to fetch transactions');
        }
    }
});
