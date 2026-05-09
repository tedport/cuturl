# CutUrl

A modern URL shortening service built with FastAPI, providing a RESTful API for creating, managing, and tracking shortened links with automatic redirection functionality.

## Features

- **FastAPI-powered API**: High-performance asynchronous web framework for building APIs
- **Secure link management**: Password-protected links with hashed codes for owner access
- **Click tracking**: Monitor link usage with detailed statistics including click counts, timestamps, and user agents
- **Expiration and limits**: Set expiration dates and maximum click limits for links
- **PostgreSQL database**: Robust data storage with SQLAlchemy ORM and Alembic migrations
- **Docker support**: Easy deployment with containerized setup using Docker Compose
- **Automatic redirection**: Seamless 302 redirects from short slugs to original URLs

## Getting Started
### Prerequisites

- Python 3.14+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (if running locally without Docker)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tedport/cuturl.git
   cd cuturl
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - For Docker deployment: Run `docker-compose up -d` to start PostgreSQL
   - For local PostgreSQL: Update `DATABASE_URL` in your environment variables

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the application:**
   ```bash
   fastapi run
   ```
   The API will be available at `http://localhost:8000`

### Usage Examples

**Create a shortened link:**
```bash
curl -X POST "http://localhost:8000/links/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "password": "mypassword"}'
```

**Access link statistics:**
```bash
curl "http://localhost:8000/links/abc123/stats"
```

**Redirect to original URL:**
```bash
curl -L "http://localhost:8000/abc123"
```

**Deactivate a link:**
```bash
curl -X DELETE "http://localhost:8000/links/abc123"
```

## API Documentation

For detailed API documentation, visit `/docs` when the application is running, which provides an interactive Swagger UI.

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/tedport/cuturl/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/tedport/cuturl/discussions)

