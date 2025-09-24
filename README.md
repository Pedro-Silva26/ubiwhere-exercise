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
    docker-compose up --build

2. **Run migrations inside the container**
     ```bash
     docker-compose exec web uv run python manage.py migrate

3. **Access the API**

Open http://127.0.0.1:8000

## Populate Database

1. **Populate Sensors**
    ```bash
   docker-compose exec web uv run python manage.py import_sensors

2. **Populate Road Segments and Traffic Records**
    ```bash
   docker-compose exec web uv run python manage.py import_traffic_and_routes

## Run Tests

1. **Run Tests on Docker**
    ```bash 
    docker-compose exec web uv run python manage.py test
