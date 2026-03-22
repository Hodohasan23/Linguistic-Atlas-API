# Linguistic Atlas API — COMP3011 (Web Services & Web Data)

A FastAPI backend providing structured programmatic access to the Glottolog linguistic dataset, with filtering, analytics, authentication, user-curated language sets, and an MCP server for AI-assisted querying.

> **All endpoints are protected by an API key** via `X-API-Key`. Write operations additionally require a JWT bearer token.

---

## Links

| Resource | URL |
|---|---|
| Live API | https://web-production-88604.up.railway.app |
| API Documentation | https://web-production-88604.up.railway.app/docs |
| GitHub Repository | https://github.com/Hodohasan23/Linguistic-Atlas-API |

---

## Contents

- [Quickstart](#quickstart)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Configuration](#configuration)
- [Database and migrations](#database-and-migrations)
- [Dataset seeding](#dataset-seeding)
- [Run the API](#run-the-api)
- [Frontend](#frontend)
- [Testing](#testing)
- [MCP Server](#mcp-server)
- [API overview](#api-overview)
- [Deployment on Railway](#deployment-on-railway)
- [GenAI usage](#genai-usage)

---

## Quickstart

### Requirements

- Python 3.12+
- pip
- PostgreSQL running locally (or use the Railway managed instance directly)

### 1) Clone the repository

```bash
git clone https://github.com/Hodohasan23/Linguistic-Atlas-API.git
cd Linguistic-Atlas-API
```

### 2) Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows PowerShell
pip install -r requirements.txt
```

### 3) Set environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost/linguistic_atlas
API_KEY=secret123
SECRET_KEY=yoursecretkey
```

Notes:
- Never commit `.env` to version control — it is excluded via `.gitignore`
- To use the Railway database directly instead of a local PostgreSQL instance, set `DATABASE_URL` to the `DATABASE_PUBLIC_URL` value from your Railway dashboard

### 4) Run migrations

```bash
alembic upgrade head
```

### 5) Seed the dataset

```bash
python seed.py
```

This loads the Glottolog CSV files into PostgreSQL. The script handles per-record exceptions gracefully so a single malformed row does not abort the entire import. For large datasets over a residential connection this may take several minutes.

### 6) Run the API

```bash
uvicorn app.main:app --reload
```

Open Swagger UI: http://127.0.0.1:8000/docs

### 7) Run tests

```bash
pytest -v
```

---

## Tech stack

- **FastAPI** — HTTP routing, automatic OpenAPI docs, dependency injection
- **PostgreSQL** — relational datastore (Railway managed in production)
- **SQLModel** — bridges SQLAlchemy and Pydantic, single model definition for schema and validation
- **Alembic** — versioned schema migrations throughout development
- **JWT** via `python-jose` — authentication token issuance
- **bcrypt** via `passlib` — password hashing, raw passwords never stored
- **pytest** and FastAPI **TestClient** — integration tests against a live database
- **GitHub Actions** — CI pipeline (Ruff lint and pytest on every push to main)
- **Railway** — production deployment, managed PostgreSQL with persistent volume

---

## Project structure
```
app/
  main.py                       # FastAPI app entrypoint
  database.py                   # engine, session, get_session dependency
  config.py                     # settings and environment variable loading
  security.py                   # API key and JWT dependencies
  models/
    models.py                   # SQLModel ORM models (11 tables)
  routes/
    languages.py                # language endpoints
    language_sets.py            # language set CRUD
    analytics.py                # similarity scoring, set comparison
    auth.py                     # register, login, /auth/me
  services/
    language_service.py         # language query logic
    stats_service.py            # analytics and statistics logic

data/                           # raw Glottolog CSV source files
docs/                           # API documentation PDF
frontend/                       # standalone frontend interface
migrations/                     # Alembic migration versions
scripts/                        # utility scripts (seeding, setup)
tests/
  test_basic.py                 # core contract tests
  test_extended.py              # auth, filtering, analytics, error handling

mcp_server.py                   # MCP server for LLM-based querying
schema.erd                      # entity-relationship diagram
schema.sql                      # raw SQL schema
alembic.ini                     # Alembic configuration
Procfile                        # Railway process definition
requirements.txt                # Python dependencies
pytest.ini                      # pytest configuration
```
---

## Configuration

| Variable | Purpose | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `API_KEY` | Required on all endpoints via `X-API-Key` header | `secret123` |
| `SECRET_KEY` | JWT signing secret | `yoursecretkey` |

All three variables must be set before running the application. In CI they are set via GitHub Actions environment variables. On Railway they are injected via the Railway variable reference system. Locally they are loaded from the `.env` file.

---

## Database and migrations

Alembic manages schema changes throughout development. Each migration is versioned in `migrations/versions/`. To apply all migrations:

```bash
alembic upgrade head
```

For a fresh Railway deployment the schema was created with `SQLModel.metadata.create_all` in a single step, which is appropriate for a new deployment target with no prior data.

The schema consists of 11 tables: Language, LanguageName, Parameter, Code, ParameterValue, Tree, Media, User, LanguageSet, LanguageSetItem, and SetComparison. Foreign key constraints with cascading deletes are applied throughout.

---

## Dataset seeding

The dataset is derived from Glottolog and distributed across seven CSV files:

- `languages.csv` — 27,177 languages with Glottocodes, coordinates, macroarea, and endangerment level
- `names.csv` — alternative names and dialect variants
- `parameters.csv` — typological structural features
- `codes.csv` — classification values per parameter
- `values.csv` — parameter-value assignments per language
- `media.csv` — documentation metadata per language
- `trees.csv` — hierarchical family tree structure

To seed locally:

```bash
python seed_postgres.py
```

To seed the Railway database remotely:

```bash
DATABASE_URL=your_railway_public_url python seed.py
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

- Local Swagger UI: http://127.0.0.1:8000/docs
- Live deployment: https://web-production-88604.up.railway.app
- Live API docs: https://web-production-88604.up.railway.app/docs

---

## Frontend

A standalone frontend is included in the `frontend/` directory. It communicates with the deployed Railway API and provides:

- A searchable, paginated languages table with macroarea and level filtering
- An interactive map plotting all 27,177 languages as geographic pins coloured by macroarea, derived from the latitude and longitude coordinates stored in the database
- An analytics page visualising family distributions and macroarea breakdowns
- A language sets page allowing authenticated users to create, manage, and compare collections

To run the frontend locally, open `frontend/index.html` in a browser or serve it with any static file server:

```bash
cd frontend
npm install dev 
npm run dev 
```

Then open http://localhost:8080/ in your browser.

---

## Testing

Tests use pytest and FastAPI's TestClient against a real PostgreSQL database.

```bash
pytest -v
```

Make sure your `.env` file is configured before running tests locally. The suite is split across two files:

- `test_basic.py` — root, health, API key enforcement, JWT enforcement, 404 handling
- `test_extended.py` — auth flows, language filtering, pagination, language sets, analytics, error handling

CI runs both files on every push to main via GitHub Actions, spinning up a live PostgreSQL 15 service container with `--health-cmd pg_isready` health checks to prevent race conditions between container startup and test execution.

---

## MCP Server

An MCP server (`mcp_server.py`) exposes the API's core tools to LLM agents using the stdio transport from the Python MCP SDK. This allows AI assistants such as Claude to query linguistic data directly without manual HTTP calls.

### Install the MCP SDK

```bash
pip install mcp
```

### Add to Claude Desktop

Add the following to your `claude_desktop_config.json` (usually at `~/Library/Application Support/Claude/` on macOS):

```json
{
  "mcpServers": {
    "linguistic-atlas": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"]
    }
  }
}
```

### Run standalone

```bash
python mcp_server.py
```

---

## API overview

### Core
- `GET /` — root message confirming API is running
- `GET /health` — liveness check returning `{ "status": "ok" }`

### Languages
- `GET /languages` — list with filtering by macroarea, level, country; pagination via limit/offset
- `GET /languages/search` — search by name
- `GET /languages/{id}` — retrieve a single language by ID
- `GET /languages/{id}/names` — alternative names for a language
- `GET /languages/{id}/parameter-values` — typological features
- `GET /languages/families` — family classifications
- `GET /languages/macroareas` — available macroareas

### Language sets
- `GET /language-sets` — list sets for authenticated user (JWT required)
- `POST /language-sets` — create a named collection (JWT required)
- `GET /language-sets/{id}` — retrieve a set
- `POST /language-sets/{id}/items` — add a language to a set (JWT required)
- `DELETE /language-sets/{id}/items/{language_id}` — remove a language (JWT required)
- `DELETE /language-sets/{id}` — delete a set and all its items (JWT required)

### Analytics
- `GET /analytics/similarity` — similarity score between two languages combining Jaccard parameter intersection, geographic distance, and family classification
- `POST /analytics/compare-sets` — compare typological and geographic profiles of two language sets

### Auth
- `POST /auth/register` — register a new user account
- `POST /auth/login` — login and receive a JWT access token
- `GET /auth/me` — return the decoded token payload for the current user

---

## Deployment on Railway

The application is deployed on Railway with two services: a Uvicorn web service running on port 8080 and a managed PostgreSQL instance with a persistent volume attached.

### How it works

- `DATABASE_URL` is injected at runtime via Railway's variable reference syntax, linking the two services without hardcoding connection strings
- `API_KEY` and `SECRET_KEY` are set as separate Railway service variables
- Deployments trigger automatically on every push to main via GitHub integration
- The Railway database was seeded remotely by running the seed script locally against the `DATABASE_PUBLIC_URL`

### Redeploying from scratch

1. Create a new Railway project with a PostgreSQL plugin
2. Add the environment variables (`DATABASE_URL`, `API_KEY`, `SECRET_KEY`) in the Railway dashboard
3. Connect the GitHub repository — Railway will deploy automatically
4. Run the seed script locally pointing at `DATABASE_PUBLIC_URL`

---

## Security

All endpoints are protected using **API key authentication** via request headers.

Example:
```http
X-API-Key: secret123