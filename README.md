# Project Nexus: A Production-Ready E-commerce Backend

## Overview

This project is a high-performance, scalable, and secure backend system for a full e-commerce platform. It is built with Django, containerized with Docker, and follows modern best practices including automated testing, CI/CD, and comprehensive API documentation.

## Key Features

-   **Full CRUD APIs:** For Products, Categories, and User Management.
-   **Secure JWT Authentication:** Stateless authentication using JSON Web Tokens.
-   **User Address Management:** Allows users to manage multiple shipping addresses.
-   **Product Reviews and Ratings:** Users can review products, with ratings automatically aggregated and updated on the product.
-   **Shopping Cart Functionality:** Persistent shopping carts for authenticated users, with functionality to add, update, and remove items.
-   **Order Placement:** Users can create an order directly from their shopping cart.
-   **Stripe Payment Integration:** A complete workflow to create and process payments for orders using Stripe.
-   **Advanced API Functionality:**
    -   Powerful filtering by category and price range.
    -   Full-text search across product names and descriptions.
    -   Sorting by multiple fields (name, price, etc.).
    -   Efficient pagination for large datasets.
-   **Role-Based Permissions:** Granular permissions for users, authors, and admins.
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
-   **Payments:** Stripe
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
    Copy the example `.env.example` file to `.env` and fill in your credentials. You will need database credentials and your **Stripe API keys**.
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

#### Users & Auth
| Method | Endpoint                          | Description                               |
| :----- | :-------------------------------- | :---------------------------------------- |
| `POST` | `/api/v1/users/register/`         | Register a new user.                      |
| `POST` | `/api/v1/token/`                  | Obtain a JWT access/refresh token pair.   |

#### Products & Categories
| Method | Endpoint                          | Description                               |
| :----- | :-------------------------------- | :---------------------------------------- |
| `GET`  | `/api/v1/products/`               | List all products (with filters).         |
| `POST` | `/api/v1/products/`               | Create a new product (Admin only).        |
| `GET`  | `/api/v1/products/{id}/`          | Retrieve a single product.                |
| `GET`  | `/api/v1/categories/`             | List all categories.                      |

#### User Addresses
| Method | Endpoint                          | Description                               |
| :----- | :-------------------------------- | :---------------------------------------- |
| `GET`  | `/api/v1/users/addresses/`        | List addresses for the current user.      |
| `POST` | `/api/v1/users/addresses/`        | Create a new address for the user.        |
| `GET`  | `/api/v1/users/addresses/{id}/`   | Retrieve a specific address.              |
| `PUT`  | `/api/v1/users/addresses/{id}/`   | Update an address.                        |
| `DEL`  | `/api/v1/users/addresses/{id}/`   | Delete an address.                        |

#### Product Reviews
| Method | Endpoint                                  | Description                               |
| :----- | :---------------------------------------- | :---------------------------------------- |
| `GET`  | `/api/v1/products/{product_id}/reviews/`  | List reviews for a product.               |
| `POST` | `/api/v1/products/{product_id}/reviews/`  | Create a new review for a product.        |
| `GET`  | `/api/v1/products/{product_id}/reviews/{id}/` | Retrieve a specific review.               |
| `PUT`  | `/api/v1/products/{product_id}/reviews/{id}/` | Update your review (Author only).         |

#### Shopping Cart
| Method | Endpoint                          | Description                               |
| :----- | :-------------------------------- | :---------------------------------------- |
| `GET`  | `/api/v1/cart/`                   | Retrieve the current user's cart.         |
| `POST` | `/api/v1/cart/items/`             | Add a product to the cart.                |
| `PATCH`| `/api/v1/cart/items/{item_id}/`   | Update the quantity of an item.           |
| `DEL`  | `/api/v1/cart/items/{item_id}/`   | Remove an item from the cart.             |

#### Orders & Payments
| Method | Endpoint                                  | Description                               |
| :----- | :---------------------------------------- | :---------------------------------------- |
| `POST` | `/api/v1/orders/`                         | Create an order from the user's cart.     |
| `GET`  | `/api/v1/orders/`                         | List the current user's order history.    |
| `GET`  | `/api/v1/orders/{id}/`                    | Retrieve a specific order.                |
| `POST` | `/api/v1/orders/{id}/create_payment_intent/` | Get a Stripe client secret to pay for an order. |
| `POST` | `/api/v1/stripe-webhook/`                 | (Internal) Listens for Stripe events.     |

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