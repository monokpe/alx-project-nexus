# Project Nexus API

[![CI](https://github.com/monokpe/alx-project-nexus/actions/workflows/ci.yml/badge.svg)](https://github.com/monokpe/alx-project-nexus/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/monokpe/alx-project-nexus/blob/main/LICENSE)

A robust and scalable e-commerce backend built with Django and the Django REST Framework.

## What's New

- **Admin Panel Overhaul**: The admin panel has been significantly improved with a modern UI, custom actions, advanced filtering, data visualization, and model history.

## Overview

Project Nexus provides a comprehensive set of RESTful API endpoints to power an e-commerce platform. It includes functionality for product management, user authentication with JWT, and more. The project is fully containerized with Docker for consistent development and production environments.

### Key Features

*   **User Authentication**: Secure user registration and login using JSON Web Tokens (JWT).
*   **Product Management**: Full CRUD (Create, Read, Update, Delete) operations for products.
*   **Interactive API Documentation**: Explore and test the API live using the automatically generated Swagger/OpenAPI interface.
*   **Containerized Environment**: Uses Docker and Docker Compose for easy and reliable local development.
*   **CI/CD Pipeline**: Includes a GitHub Actions workflow for automated linting and testing.

### Admin Panel Improvements

*   **Custom Admin Actions**: Bulk update product stock to "in stock" or "out of stock" with a single click.
*   **Modern UI**: A modern and responsive admin theme using `django-jazzmin`.
*   **Advanced Filtering**: Filter products by price range.
*   **Data Visualization**: A chart showing the number of products per category.
*   **Model History/Reversion**: Version control for product and category models, allowing you to see a history of changes and revert to a previous version if needed.

## Technology Stack

*   **Backend**: Django, Django REST Framework
*   **Database**: PostgreSQL
*   **Cache**: Redis
*   **API Documentation**: drf-spectacular (Swagger UI)
*   **Server**: Gunicorn
*   **Containerization**: Docker, Docker Compose

## Getting Started: Local Development

This project is fully containerized. The only prerequisites are having **Docker** and **Docker Compose** installed.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/monokpe/alx-project-nexus.git
    cd alx-project-nexus
    ```

2.  **Set up environment variables:**
    Create a `.env` file by copying the example file. The default values are configured for the local Docker setup.
    ```bash
    cp .env.example .env
    ```

3.  **Build and Run the Containers:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images, start the Django, PostgreSQL, and Redis services, and run database migrations automatically. The web application will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access the interactive API documentation in your browser. This is the easiest way to explore and test all the available endpoints.

*   **Swagger UI:** [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

The root of the site (`/`) will automatically redirect you to this documentation page.

## Deployment

This application is deployed on **Render** for the web service, with the database and cache hosted on **Aiven**.

### Render (Web Service)

The web service is set up manually in the Render dashboard. It requires the following environment variables to be set:

*   `SECRET_KEY`: A unique, private key.
*   `DEBUG`: Set to `0` for production.
*   `ALLOWED_HOSTS`: The `.onrender.com` domain for your service.
*   `DB_URL`: The **Service URI** for your Aiven PostgreSQL database.
*   `REDIS_URL`: The **Service URI** for your Aiven Valkey (Redis) instance.

### Aiven (Database & Cache)

The free tier on Aiven is used to provide the PostgreSQL and Redis (Valkey) services.

1.  Sign up for a free account on [Aiven.io](https://aiven.io/).
2.  Create a new **PostgreSQL** service on the free plan.
3.  Create a new **Valkey** (Redis-compatible) service on the free plan.
4.  For each service, find its **Connection information** and copy the **Service URI**. These URIs are the values you will use for the `DB_URL` and `REDIS_URL` environment variables in Render.

## CI/CD

This repository uses **GitHub Actions** for Continuous Integration. The workflow is defined in `.github/workflows/ci.yml` and automatically runs the following checks on every push or pull request to the `main` branch:
*   Installs dependencies
*   Lints the code with `ruff`
*   Runs the full test suite using `python manage.py test`