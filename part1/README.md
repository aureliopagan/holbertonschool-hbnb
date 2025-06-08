# HBnB - UML Documentation

## Part 1: Technical Documentation

### Context and Objective

This phase focuses on creating comprehensive technical documentation for the HBnB Evolution application, a simplified AirBnB-like platform. The documentation will clarify the system’s architecture, business logic, and internal interactions, serving as a blueprint for development.

---

### Problem Description

You are to document the architecture and design of HBnB Evolution, which supports:

- **User Management:** Registration, profile updates, and user roles (regular/admin).
- **Place Management:** Users can list properties with details (name, description, price, location, amenities).
- **Review Management:** Users can submit reviews (rating, comment) for places.
- **Amenity Management:** Manage amenities associated with places.

---

### Business Rules and Requirements

#### User Entity

- Attributes: first name, last name, email, password, is_admin (boolean).
- Operations: register, update profile, delete.
- Uniquely identified by ID.
- Tracks creation and update timestamps.

#### Place Entity

- Attributes: title, description, price, latitude, longitude.
- Owner: associated user.
- Amenities: list of amenities.
- Operations: create, update, delete, list.
- Uniquely identified by ID.
- Tracks creation and update timestamps.

#### Review Entity

- Attributes: rating, comment.
- Associated with a user and a place.
- Operations: create, update, delete, list by place.
- Uniquely identified by ID.
- Tracks creation and update timestamps.

#### Amenity Entity

- Attributes: name, description.
- Operations: create, update, delete, list.
- Uniquely identified by ID.
- Tracks creation and update timestamps.

---

### Architecture and Layers

The application uses a three-layer architecture:

- **Presentation Layer:** User-facing services and APIs.
- **Business Logic Layer:** Models and core logic.
- **Persistence Layer:** Data storage and retrieval.

All data is persisted in a database (to be specified in Part 3).

---

### Tasks

1. **High-Level Package Diagram:**  
    Illustrate the three-layer architecture and their interactions using the facade pattern.

2. **Detailed Class Diagram (Business Logic Layer):**  
    Model User, Place, Review, and Amenity entities, their attributes, methods, and relationships (including Place-Amenity associations).

3. **Sequence Diagrams for API Calls:**  
    Create sequence diagrams for at least four API calls (e.g., user registration, place creation, review submission, fetching places).

4. **Documentation Compilation:**  
    Combine all diagrams and explanatory notes into a single technical document.

---

### Conditions and Constraints

- Clearly represent data flow and interactions between layers.
- Use UML notation for all diagrams.
- Accurately reflect business rules and requirements.
- Ensure diagrams are detailed enough to guide implementation.

---

### Resources

- **UML Basics:**  
  [OOP - Introduction to UML](#)
- **Package Diagrams:**  
  [UML Package Diagram Overview](#)  
  [UML Package Diagrams Guide](#)
- **Class Diagrams:**  
  [UML Class Diagram Tutorial](#)  
  [How to Draw UML Class Diagrams](#)
- **Sequence Diagrams:**  
  [UML Sequence Diagram Tutorial](#)  
  [Understanding Sequence Diagrams](#)
- **Diagram Tools:**  
  [Mermaid.js Documentation](#)  
  [draw.io](#)

---

### Expected Outcome

By completing this part, you will have a detailed technical document that serves as a clear blueprint for the HBnB Evolution application, supporting both implementation and understanding of the system’s design and architecture.

---

Good luck! Use the provided resources and your research to overcome any challenges.