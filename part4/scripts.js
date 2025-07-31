document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const priceFilter = document.getElementById('price-filter');
    const loginLink = document.getElementById('login-link');
    const addReview = document.getElementById('add-review');

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // Check user authentication on page load
    checkAuthentication(loginLink, addReview);

    // Set up price filter dropdown
    if (priceFilter) {
        priceFilter.innerHTML = `
            <option value="10">10</option>
            <option value="50">50</option>
            <option value="100">100</option>
            <option value="All">All</option>
        `;
        
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }

    // If we're on the place detail page, load the place data
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        const token = getCookie('token');
        if (token) {
            fetchPlaceDetails(token, placeId);
        }
    }
});

// Helper function to get a cookie value by name
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

// Function to check if the user is authenticated
function checkAuthentication(loginLink, addReview) {
    const token = getCookie('token');

    if (!token) {
        loginLink.style.display = 'block';
        if (addReview) {
            addReview.style.display = 'none';
        }
    } else {
        loginLink.style.display = 'none';
        if (addReview) {
            addReview.style.display = 'flex';
        }
        fetchPlaces(token); // Fetch places if the user is authenticated
    }
}

// Function to log in the user
async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html'; // Reload page after login
        } else {
            const errorData = await response.json();
            alert('Login failed: ' + errorData.error);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again.');
    }
}

// Function to fetch places data from the API
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places); // Display places if fetch is successful
        } else {
            console.error('Failed to fetch places data');
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// Function to display places in the DOM
function displayPlaces(places) {
    const placesList = document.querySelector('#places-list');
    placesList.innerHTML = ''; // Clear any previous content

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places available</p>';
        return;
    }

    const list = document.createElement('ul');
    list.classList.add('place-list');

    places.forEach(place => {
        const li = document.createElement('li');
        li.classList.add('place-card');
        li.innerHTML = `
            <h2>${place.title || 'No title available'}</h2>
            <p>Price per night: $${place.price || 'N/A'}</p>
            <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        list.appendChild(li); // Append each li to the ul
    });

    placesList.appendChild(list);
}

// Function to filter places by price
function filterPlacesByPrice(selectedPrice) {
    const placesList = document.querySelector('#places-list');
    const placeCards = Array.from(placesList.getElementsByClassName('place-card'));

    placeCards.forEach(place => {
        const priceText = place.querySelector('p').textContent;
        const price = parseInt(priceText.replace('Price per night: $', '').trim());

        if (selectedPrice === 'All' || price <= selectedPrice) {
            place.style.display = 'flex'; // Show the place if it meets the filter criteria
        } else {
            place.style.display = 'none'; // Hide the place if it doesn't meet the filter criteria
        }
    });
}

// Helper function to get place ID from URL
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Function to fetch place details using the place ID
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const placeDetails = await response.json();
            displayPlaceDetails(placeDetails); // Call function to display the place details
        } else {
            console.error('Failed to fetch place details');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// Function to display place details in the DOM
function displayPlaceDetails(place) {
    const placeDetailsContainer = document.getElementById('place-details');

    placeDetailsContainer.innerHTML = `
        <h1>${place.title || 'No title available'}</h1>
        <p><strong>Price:</strong> $${place.price || 'N/A'}</p>
        <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
        <p><strong>Amenities:</strong> ${place.amenities.name || 'No amenities listed'}</p>
        <div id="reviews">
            <h3>Reviews:</h3>
            ${place.reviews.map(review => `
                <div class="review-card">
                    <p>Rating: ${review.rating}</p>
                    <p>${review.text}</p>
                </div>
            `).join('') || '<br>No reviews listed'}
        </div>
    `;

    // Display review form for authenticated users
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.innerHTML = `
            <h3>Add a Review:</h3>
            <form id="review-form">
                <label for="rating">Rating (1-5):</label>
                <input type="number" id="rating" name="rating" min="1" max="5" required>
                <br>
                <label for="comment">Comment:</label>
                <textarea id="comment" name="comment" required></textarea>
                <br>
                <button type="submit">Submit Review</button>
            </form>
        `;

        // Handle review submission
        const reviewForm = document.getElementById('review-form');
        reviewForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value;

            submitReview(place.id, rating, comment); // Submit the review
        });
    }
}

// Function to submit a new review
async function submitReview(placeId, rating, comment) {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'index.html';
            return;
        }
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            try {
                const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ rating, 'text': comment })
                });

                if (response.ok) {
                    alert('Review added successfully!');
                    reviewForm.reset();
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    alert('Review failed: ' + errorData.error);
                } 
            } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again.');
    }
        });
    }
}