# Dockerized URL Shortener

A containerized URL Shortener application built with **Flask, MySQL, Redis, Nginx, Docker, and Docker Compose**.

## Architecture

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 │ HTTP :8080
                                 ▼
                        ┌─────────────────┐
                        │      NGINX      │
                        │  Reverse Proxy  │
                        └────────┬────────┘
                                 │
                                 │ :5000
                                 ▼
                        ┌─────────────────┐
                        │    FLASK APP    │
                        │  URL SHORTENER  │
                        └────────┬────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             ┌──────────────┐         ┌──────────────┐
             │    MYSQL     │         │    REDIS     │
             │   Database   │         │    Cache     │
             └──────┬───────┘         └──────┬───────┘
                    │                        │
                    ▼                        ▼
             ┌──────────────┐         ┌──────────────┐
             │  mysql_data  │         │  redis_data  │
             │    volume    │         │    volume    │
             └──────────────┘         └──────────────┘

                 Docker Network: url-network
```

## Features

* Shorten long URLs
* Redirect short URLs to original URLs
* Track click counts
* View URL statistics
* MySQL persistent storage
* Redis caching
* Nginx reverse proxy
* Dockerized deployment
* Docker Compose orchestration
* Automated testing with Pytest
* Code quality checks with Ruff
* CI/CD with GitHub Actions

## Tech Stack

| Technology     | Purpose               |
| -------------- | --------------------- |
| Flask          | Backend API           |
| MySQL          | Persistent database   |
| Redis          | Caching               |
| Nginx          | Reverse proxy         |
| Docker         | Containerization      |
| Docker Compose | Service orchestration |
| Pytest         | Unit testing          |
| Ruff           | Code quality          |
| GitHub Actions | CI/CD                 |
| Docker Hub     | Image registry        |

## Project Structure

```text
url-shortener/
├── app/
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_app.py
├── nginx/
│   └── nginx.conf
├── mysql/
│   └── init.sql
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Nandana9797/url-shortener.git
cd url-shortener
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and provide your own credentials:

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=urlshortener
MYSQL_USER=urluser
MYSQL_PASSWORD=your_password
```

> **Do not commit `.env` to GitHub.** Only `.env.example` should be included in the public repository.

### 3. Start the Application

```bash
docker compose up -d --build
```

### 4. Check Containers

```bash
docker compose ps
```

### 5. Access the Application

Open:

```text
http://localhost:8080
```

## Testing

Run the test suite:

```bash
python -m pytest
```

Run tests in verbose mode:

```bash
pytest -v
```

## Code Quality

```bash
ruff check app tests
```

## Docker Image

Docker Hub:

```text
nandana9797/url-shortener:v1.0
```

Pull the image:

```bash
docker pull nandana9797/url-shortener:v1.0
```

## CI/CD

GitHub Actions performs:

```text
Git Push
   ↓
Install Dependencies
   ↓
Ruff Check
   ↓
Run Tests
   ↓
Build Docker Image
   ↓
Push Image to Docker Hub
```

## Security

* `.env` is excluded from version control.
* `.env.example` contains only placeholder values.
* Database credentials should never be committed to a public repository.
* Use strong credentials for production deployments.

## Author

**Nandana Ajai**

GitHub: https://github.com/Nandana9797
