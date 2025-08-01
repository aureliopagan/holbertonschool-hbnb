document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded');
    
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

    // ALWAYS fetch places when on the main page, regardless of authentication
    if (document.getElementById('places-list')) {
        console.log('Places list found, fetching places...');
        fetchPlaces();
    }

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
    console.log('Place ID from URL:', placeId);
    
    if (placeId) {
        console.log('Fetching place details for ID:', placeId);
        fetchPlaceDetails(placeId);
    } else {
        console.log('No place ID found in URL');
        // Show a message if no place ID is provided
        const placeDetailsContainer = document.getElementById('place-details');
        if (placeDetailsContainer) {
            placeDetailsContainer.innerHTML = '<p>No place ID provided in URL. Please navigate from the places list.</p>';
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
        if (loginLink) loginLink.style.display = 'block';
        if (addReview) addReview.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (addReview) addReview.style.display = 'flex';
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

// Function to fetch places data from the API - Modified to work without token
async function fetchPlaces(token = null) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Only add Authorization header if token is provided
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://localhost:5000/api/v1/places', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places); // Display places if fetch is successful
        } else {
            console.error('Failed to fetch places data');
            // Show error message to user
            const placesList = document.querySelector('#places-list');
            if (placesList) {
                placesList.innerHTML = '<p>Failed to load places. Please try again later.</p>';
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        // Show error message to user
        const placesList = document.querySelector('#places-list');
        if (placesList) {
            placesList.innerHTML = '<p>Error loading places. Please check your connection.</p>';
        }
    }
}

// Function to display places in the DOM
function displayPlaces(places) {
    const placesList = document.querySelector('#places-list');
    if (!placesList) return;
    
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
    const placeId = urlParams.get('id');
    console.log('URL search params:', window.location.search);
    console.log('Extracted place ID:', placeId);
    return placeId;
}

// Function to fetch place details using the place ID - Modified to work without token for basic details
async function fetchPlaceDetails(placeId) {
    console.log('Starting fetchPlaceDetails for ID:', placeId);
    
    try {
        const apiUrl = `http://localhost:5000/api/v1/places/${placeId}`;
        console.log('Making API call to:', apiUrl);
        
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('API response status:', response.status);
        console.log('API response ok:', response.ok);

        if (response.ok) {
            const placeDetails = await response.json();
            console.log('Place details received:', placeDetails);
            displayPlaceDetails(placeDetails); // Call function to display the place details
        } else {
            console.error('Failed to fetch place details. Status:', response.status);
            const errorText = await response.text();
            console.error('Error response:', errorText);
            
            const placeDetailsContainer = document.getElementById('place-details');
            if (placeDetailsContainer) {
                placeDetailsContainer.innerHTML = `<p>Failed to load place details. Status: ${response.status}</p>`;
            }
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        const placeDetailsContainer = document.getElementById('place-details');
        if (placeDetailsContainer) {
            placeDetailsContainer.innerHTML = '<p>Error loading place details. Please check your connection and console for details.</p>';
        }
    }
}

// Function to display place details in the DOM - COMPLETELY REWRITTEN TO MATCH EXPECTED DESIGN
function displayPlaceDetails(place) {
    console.log('Starting displayPlaceDetails with data:', place);
    
    const placeDetailsContainer = document.getElementById('place-details');
    if (!placeDetailsContainer) {
        console.error('place-details container not found');
        return;
    }

    console.log('place-details container found, creating content...');

    // Clear the container and create the main structure
    placeDetailsContainer.innerHTML = '';
    
    // Create and add the place heading
    const heading = document.createElement('h1');
    heading.textContent = place.title || 'No title available';
    placeDetailsContainer.appendChild(heading);
    
    console.log('Added heading:', heading.textContent);

    // Create the place info card (similar to your expected design)
    const placeInfoCard = document.createElement('div');
    placeInfoCard.className = 'place-info';
    
    placeInfoCard.innerHTML = `
        <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown Host'}</p>
        <p><strong>Price per night:</strong> $${place.price || 'N/A'}</p>
        <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
        <p><strong>Amenities:</strong> ${place.amenities && place.amenities.length > 0 
            ? place.amenities.map(a => a.name).join(', ') 
            : 'No amenities listed'}</p>
    `;
    
    placeDetailsContainer.appendChild(placeInfoCard);
    console.log('Added place info card');

    // Display reviews in the reviews section
    console.log('Displaying reviews:', place.reviews);
    displayReviews(place.reviews || []);

    // Display review form for authenticated users
    const addReviewSection = document.getElementById('add-review');
    const token = getCookie('token');
    
    if (addReviewSection && token) {
        console.log('User is authenticated, showing review form');
        addReviewSection.innerHTML = `
            <div class="review-header">
                <h3>Add a Review</h3>
            </div>
            <form id="review-form">
                <label for="rating">Rating (1-5):</label>
                <input type="number" id="rating" name="rating" min="1" max="5" required>
                
                <label for="comment">Comment:</label>
                <textarea id="comment" name="comment" rows="4" required></textarea>
                
                <button type="submit" class="submit">Submit Review</button>
            </form>
        `;

        // Handle review submission
        const reviewForm = document.getElementById('review-form');
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value;

            await submitReview(place.id, rating, comment);
        });
    } else {
        console.log('User not authenticated, not showing review form');
    }
    
    console.log('displayPlaceDetails completed');
}

// Completely rewritten function to properly display reviews in card format
function displayReviews(reviews) {
    console.log('Starting displayReviews with:', reviews);
    
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) {
        console.error('reviews section not found');
        return;
    }

    // Clear the section
    reviewsSection.innerHTML = '';

    // Add reviews header
    const reviewHeader = document.createElement('div');
    reviewHeader.className = 'review-header';
    reviewHeader.innerHTML = '<h2>Reviews</h2>';
    reviewsSection.appendChild(reviewHeader);
    
    console.log('Added reviews header');

    if (!reviews || reviews.length === 0) {
        const noReviewsMsg = document.createElement('p');
        noReviewsMsg.textContent = 'No reviews available';
        noReviewsMsg.style.textAlign = 'center';
        reviewsSection.appendChild(noReviewsMsg);
        console.log('No reviews to display');
        return;
    }

    // Create individual review cards
    reviews.forEach((review, index) => {
        console.log(`Creating review card ${index}:`, review);
        
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        // Create star rating display
        const stars = '★'.repeat(review.rating || 0) + '☆'.repeat(5 - (review.rating || 0));
        
        reviewCard.innerHTML = `
            <h3>${review.user ? review.user.first_name + ' ' + review.user.last_name + ':' : 'Anonymous:'}</h3>
            <p>${review.text || 'No comment provided'}</p>
            <p><strong>Rating:</strong> ${stars}</p>
        `;
        
        reviewsSection.appendChild(reviewCard);
        console.log(`Added review card ${index}`);
    });
    
    console.log('displayReviews completed');
}

// Function to submit a new review
async function submitReview(placeId, rating, comment) {
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to submit a review.');
        window.location.href = 'login.html';
        return;
    }

    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rating: parseInt(rating), 'text': comment })
        });

        if (response.ok) {
            alert('Review added successfully!');
            // Refresh the place details to show the new review
            fetchPlaceDetails(placeId);
        } else {
            const errorData = await response.json();
            alert('Review failed: ' + errorData.error);
        } 
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred. Please try again.');
    }
}