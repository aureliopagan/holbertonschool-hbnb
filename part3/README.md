# hbnb Project

## Overview
The hbnb project is a web application built using Flask that provides a RESTful API for managing users, places, reviews, and amenities. This project is designed to be modular and scalable, allowing for easy expansion and maintenance.

## Project Structure
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hbnb.git
   ```
2. Navigate to the project directory:
   ```
   cd hbnb
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python run.py
```
The application will start on the default Flask port (5000). You can access the API endpoints at `http://localhost:5000/api/v1/`.

## API Endpoints
- **Users**: Manage user accounts and authentication.
- **Places**: Manage listings of places.
- **Reviews**: Manage reviews for places.
- **Amenities**: Manage amenities associated with places.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.