FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so

WORKDIR /app

# Install system dependencies (GDAL, build tools, curl)
RUN apt-get update && apt-get install -y \
    curl \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    build-essential \
    && ldconfig \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency management files
COPY pyproject.toml uv.lock ./

# Create virtual environment and install Python dependencies
RUN uv venv && uv pip install --upgrade pip && uv sync --frozen --compile-bytecode

# Copy the rest of the project
COPY . /app/

# Expose Django's default port
EXPOSE 8000

CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py runserver 0.0.0.0:8000"]
