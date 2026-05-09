# CutUrl

A modern URL shortening backend built with FastAPI, providing a RESTful API for creating, managing, and tracking shortened links with automatic 302 redirection.

## Features

- **FastAPI backend** with SQLAlchemy ORM
- **Owner code protection**: each link returns an opaque owner code for management operations
- **Click tracking**: records click counts, country, device, and last click timestamp
- **Expiration and usage limits**: support for either `expires_at` or `max_uses`
- **SQLite default + PostgreSQL support** via `DATABASE_URL`
- **Docker Compose support** for easy backend deployment
- **Interactive API docs** via FastAPI `/docs`

## Getting Started
### Prerequisites

- Python 3.14+
- `pip` for Python dependency installation
- `Docker` and `Docker Compose` if you want to run the backend with containers

## Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tedport/cuturl.git
   cd cuturl
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database:
   - By default, the backend uses SQLite at `sqlite:///db.sql`
   - To use PostgreSQL, set `DATABASE_URL` in your environment

4. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

5. Run the backend:
   ```bash
   uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Compose

The `docker-compose.yml` file includes a Postgres database and the backend service. Start both with:

```bash
docker-compose up -d
```

The backend will be available on `http://localhost:8000`.

## Configuration

Environment variables:

- `DATABASE_URL` — database connection string (default: `sqlite:///db.sql`)

## API Endpoints

### Create a shortened link

- Method: `POST`
- URL: `/links/`
- Body:
  - `url` (required): original URL
  - `slug` (optional): custom slug matching `[a-z0-9_-]{3,32}` and not reserved
  - `expires_at` (optional): expiration timestamp
  - `max_uses` (optional): maximum number of redirects

> Note: `expires_at` and `max_uses` are mutually exclusive.

Response includes the created link and an `owner_code` used for deactivation.

### Get link info

- Method: `GET`
- URL: `/links/{slug}`

Returns public metadata for the link without exposing the owner code.

### Get link statistics

- Method: `GET`
- URL: `/links/{slug}/stats`

Returns click analytics including total clicks, clicks by country, clicks by device, and last click timestamp.

### Deactivate a link

- Method: `DELETE`
- URL: `/links/{slug}`
- Query parameter: `code` (owner code returned when the link was created)

This marks the link inactive so it no longer redirects.

### Redirect to original URL

- Method: `GET`
- URL: `/{slug}`

Performs a `302` redirect to the original URL and records the click.

## Validation and limits

- Slugs must be 3–32 characters, lowercase letters, numbers, hyphens, or underscores
- Reserved slugs: `links`, `docs`, `openapi.json`, `redoc`
- Link creation is rate limited to 10 requests per 30 minutes per IP
- Click tracking resolves country via `ip-api.com` and stores the request `User-Agent`

## API Documentation

Open `http://localhost:8000/docs` when the app is running for Swagger UI and interactive endpoint testing.

## Support

- **Issues**: Report bugs via [GitHub Issues](https://github.com/tedport/cuturl/issues)

