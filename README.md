# Project Nexus: A Production-Ready E-commerce Backend

## Overview

This project is a high-performance, scalable, and secure backend system for an e-commerce product catalog. It is built with Django, containerized with Docker, and follows modern best practices including automated testing, CI/CD, and comprehensive API documentation.

## Key Features

-   **Full CRUD APIs:** For Products, Categories, and User Management.
-   **Secure JWT Authentication:** Stateless authentication using JSON Web Tokens.
-   **Advanced API Functionality:**
    -   Powerful filtering by category and price range.
    -   Full-text search across product names and descriptions.
    -   Sorting by multiple fields (name, price, etc.).
    -   Efficient pagination for large datasets.
-   **Role-Based Permissions:** Read-only access for all users, but write access is restricted to Admin/Staff users.
-   **High Performance:** API responses for the product catalog are cached using **Redis** to minimize database load.
-   **Security:** **Rate limiting** is implemented to protect against brute-force attacks and API abuse.
-   **Live API Documentation:** Interactive Swagger UI for easy API exploration and testing.
-   **Automated Testing:** Comprehensive unit and integration test suite.
-   **CI/CD Pipeline:** GitHub Actions automatically tests every push and pull request to the main branch.
-   **Containerized Environment:** Fully containerized with Docker and Docker Compose for consistent development and production environments.

## Technology Stack

-   **Backend:** Django, Django REST Framework
-   **Database:** PostgreSQL
-   **Caching:** Redis
-   **Web Server:** Gunicorn & WhiteNoise
-   **Deployment:** Docker, Docker Compose
-   **CI/CD:** GitHub Actions
-   **API Documentation:** drf-spectacular (Swagger UI)

---

## Getting Started

### Prerequisites

-   Python 3.11+
-   Docker and Docker Compose
-   An `.env` file (see `.env.example`)

### 1. Local Development Setup (Without Docker)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/monokpe/alx-project-nexus.git
    cd alx-project-nexus
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Copy the example `.env.example` file to `.env` and fill in your database credentials and a new `SECRET_KEY`.
    ```bash
    cp .env.example .env
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Populate the database with sample data (Optional):**
    ```bash
    python manage.py seed_db --number 50
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000`.

### 2. Docker Setup (Recommended)

This is the easiest way to run the entire application stack, including PostgreSQL and Redis.

1.  **Clone the repository and create your `.env` file** as described above.

2.  **Build and run the containers:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Run database migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **Populate the database (Optional):**
    ```bash
    docker-compose exec web python manage.py seed_db --number 50
    ```
    The application will be running and accessible at `http://127.0.0.1:8000`.

---

## API Documentation

Once the application is running, the interactive Swagger UI documentation is available at:
**`http://127.0.0.1:8000/api/schema/swagger-ui/`**

### API Endpoints Overview

| Method | Endpoint                          | Description                               |
| :----- | :-------------------------------- | :---------------------------------------- |
| `POST` | `/api/v1/users/register/`         | Register a new user.                      |
| `POST` | `/api/v1/token/`                  | Obtain a JWT access/refresh token pair.   |
| `GET`  | `/api/v1/products/`               | List all products (with filters).         |
| `POST` | `/api/v1/products/`               | Create a new product (Admin only).        |
| `GET`  | `/api/v1/products/{id}/`          | Retrieve a single product.                |
| `PUT`  | `/api/v1/products/{id}/`          | Update a product (Admin only).            |
| `GET`  | `/api/v1/categories/`             | List all categories.                      |
| `POST` | `/api/v1/categories/`             | Create a new category (Admin only).       |

---

## Running Tests

To run the automated test suite, use the following command:

```bash
python manage.py test
```
Or when using Docker:
```bash
docker-compose exec web python manage.py test
```
