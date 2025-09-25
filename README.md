# Traffic Manager Django REST Framework Project with Astral's `uv` and Docker

A RESTful API built with **Django** and **Django REST Framework (DRF)**, managed using **Astral's `uv`** for environment
and dependency management, and containerized with **Docker**.

---

## Features

- Pre-Commit (Black Code Format)
- RESTful API endpoints
- Dockerized setup for development and production
- Managed environment with `uv`

---

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.13
- [Astral's `uv`](https://docs.astral.sh/uv/) (for environment and dependency management)
- Docker & Docker Compose (for containerized setup)
- Git (optional)

---

## Project Setup (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/your-django-project.git
   cd your-django-project

## Docker Setup

1. **Build and start the containers**

    ```bash
    docker compose up -d --build

2. **Run migrations inside the container**
     ```bash
     docker compose exec web uv run python manage.py migrate

## Populate Database

1. **Populate Sensors**
    ```bash
   docker compose exec web uv run python manage.py import_sensors

2. **Populate Road Segments and Traffic Records**
    ```bash
   docker compose exec web uv run python manage.py import_traffic_and_routes
3. **Populate User and Token**
    ```bash
   docker compose exec web uv run python manage.py create_user_and_sensor_token

Admin user:
username: admin
password: 123

## Run Tests

1. **Run Tests on Docker**
    ```bash 
    docker compose exec web uv run pytest


## Explore the API

### 1. Using Postman (Import Collection File)

You can explore the API quickly by importing a Postman collection file.

**Steps:**

1. Open **Postman**.
2. Click on **Import** (top-left corner).
3. Select **File** and choose the Postman collection file `Traffic API.postman_collection.json`.
4. Click **Import**.

---

### 2. Using Swagger (DRF built-in docs)

Swagger provides an interactive API documentation page where you can try endpoints directly in your browser.

**Steps:**

1. Browse to http://127.0.0.1:8001/api/docs/swagger-ui/
2. Click on **Authorize** and enter the authentications.
3. Explore the different endpoints
