# Linguistic Atlas API — COMP3011 (Web Services & Web Data)

A FastAPI backend providing structured programmatic access to the Glottolog linguistic dataset, with filtering, analytics, authentication, user-curated language sets (Testimonies), and an MCP server for AI-assisted querying.

---

## Links

| Resource | URL |
|---|---|
| Live API | https://web-production-88604.up.railway.app |
| API Documentation | https://web-production-88604.up.railway.app/docs |
| GitHub Repository | https://github.com/Hodohasan23/Linguistic-Atlas-API |

---

## API Access

All endpoints require the following header on every request:
```
X-API-Key: secret123
```

**In Swagger UI**: click the green **Authorize** button at the top right of the `/docs` page, enter `secret123` in the APIKeyHeader field, and click Authorize. All requests will then include the key automatically.

**In curl**:
```bash
curl -H "X-API-Key: secret123" https://web-production-88604.up.railway.app/languages
```

**In Postman**: add a header with key `X-API-Key` and value `secret123`.

---

## Admin Access

The first user to register on the system is automatically assigned the ADMIN role. All subsequent registrations receive the USER role. Admin privileges are required for delete operations on Testimonies.

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
- [Security](#security)
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
ANTHROPIC_API_KEY=your_anthropic_key
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
python -m scripts.seed_postgres
```

This loads the Glottolog CSV files into PostgreSQL. The script handles per-record exceptions gracefully so a single malformed row does not abort the entire import. Loading all 144,887 ParameterValue records may take several minutes over a residential connection.

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
- **Ruff** — linting and code style enforcement
- **pytest** and FastAPI **TestClient** — integration tests against a live database
- **GitHub Actions** — CI pipeline (Ruff lint and pytest on every push to main)
- **Railway** — production deployment, managed PostgreSQL with persistent volume
- **Anthropic API** — powers the `/ask` natural language interface

---

## Project structure
```
app/
  main.py                       # FastAPI app entrypoint
  models/
    models.py                   # SQLModel ORM models (11 tables)
  core/
    config.py                   # settings and environment variable loading
    security.py                 # API key dependency, JWT require_user, require_admin
  db/
    session.py                  # engine, get_engine, get_session dependency
  languages/
    routes.py                   # language, families, macroarea endpoints
  language_sets/
    routes.py                   # language set CRUD and insights (Testimonies)
  analytics/
    routes.py                   # similarity, comparison, outliers, lineage, coverage
    service.py                  # analytics query logic
    algorithms.py               # scoring and computation functions
  auth/
    routes.py                   # register, login, /auth/me
  ask/
    routes.py                   # /ask AI natural language interface
data/
  raw/                          # raw Glottolog CSV source files
  processed/                    # cleaned/transformed data
docs/
  ERD.png                       # entity-relationship diagram
frontend/                       # standalone frontend interface
migrations/                     # Alembic migration versions
scripts/
  seed_postgres.py              # Glottolog CSV seeding script
tests/
  test_core.py                  # root, health, API key, 404 contract tests
  test_endpoints.py             # auth flows, languages, sets, analytics
  test_features.py              # endangerment, stats, testimonies, insights
  seed_test.py                  # data-dependent tests, CI-tolerant
.github/
  workflows/
    ci.yml                      # lint + test jobs against PostgreSQL 15
mcp_server.py                   # MCP server exposing API tools via stdio transport
schema.erd                      # entity-relationship diagram source
schema.sql                      # raw SQL schema
alembic.ini                     # Alembic configuration
Procfile                        # Railway process definition (Uvicorn port 8080)
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
| `ANTHROPIC_API_KEY` | Required for the `/ask` endpoint | `sk-ant-...` |

All variables must be set before running the application. In CI they are set via GitHub Actions environment variables. On Railway they are injected via the Railway variable reference system. Locally they are loaded from the `.env` file.

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
- `values.csv` — 144,887 parameter-value assignments per language
- `media.csv` — documentation metadata per language
- `trees.csv` — hierarchical family tree structure

To seed locally:
```bash
python -m scripts.seed_postgres
```

To seed the Railway database remotely:
```bash
DATABASE_URL=your_railway_public_url python -m scripts.seed_postgres
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

A standalone frontend is included in the `frontend/` directory. To use it, run it locally:
```bash
cd frontend
npm install
npm run dev
```

Check the terminal output for the port (typically 5173 for Vite). The frontend communicates with the live Railway API and provides:

- A searchable, paginated languages table with macroarea and level filtering
- An interactive map plotting all 27,177 languages as geographic pins coloured by macroarea
- An analytics page visualising family distributions and macroarea breakdowns
- A language sets page allowing authenticated users to create, manage, and compare collections

---

## Testing

Tests use pytest and FastAPI's TestClient against a real PostgreSQL database. The suite totals 69 tests across four files.
```bash
pytest -v
```

Make sure your `.env` file is configured with `DATABASE_URL` and `API_KEY` before running tests locally.

- `test_core.py` — root, health, API key enforcement, JWT enforcement, 404 handling
- `test_endpoints.py` — auth flows, language filtering, pagination, language sets, analytics, error handling
- `test_features.py` — endangerment profile, underdocumented stats, ISO lookup, families, macroareas, insights, lineage, coverage, map coordinates
- `seed_test.py` — data-dependent tests written to be tolerant of an empty database in CI

CI runs all four files on every push to main via GitHub Actions, spinning up a live PostgreSQL 15 service container with `--health-cmd pg_isready` health checks to prevent race conditions between container startup and test execution.

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

### Auth
- `POST /auth/register` — register a new user account (first user becomes admin)
- `POST /auth/login` — login and receive a JWT access token
- `GET /auth/me` — return the decoded token payload for the current user

### Languages
- `GET /languages` — paginated list with filtering by macroarea, level, and country
- `GET /languages/map` — lightweight coordinate data for all languages with known positions
- `GET /languages/search` — search by name with endangerment status included inline
- `GET /languages/random` — discover a random language
- `GET /languages/iso/{iso_code}` — look up a language by ISO 639-3 code
- `GET /languages/{id}` — retrieve a single language by Glottolog ID
- `GET /languages/{id}/names` — all known names for a language across sources
- `GET /languages/{id}/classification` — trace the genealogical family tree
- `GET /languages/{id}/parameters` — typological features
- `GET /languages/{id}/endangerment` — AES status, plain-English risk summary, years since last documentation

### Families
- `GET /families` — browse language families
- `GET /families/{family_id}` — get a family by Glottolog ID
- `GET /families/{family_id}/languages` — list languages within a family

### Macroareas
- `GET /macroareas` — list all geographic macroareas
- `GET /macroareas/{macroarea}/languages` — browse languages by macroarea

### Stats
- `GET /stats/languages-per-macroarea` — language distribution by macroarea
- `GET /stats/languages-per-family` — top 50 families by language count
- `GET /stats/endangerment-breakdown` — counts per AES level across the full dataset
- `GET /stats/underdocumented` — endangered languages unstudied since before a configurable year

### Testimonies (Language Sets)
- `GET /language-sets` — list all Testimonies
- `POST /language-sets` — create a named collection (JWT required)
- `GET /language-sets/{id}` — retrieve a Testimony
- `PATCH /language-sets/{id}` — update a Testimony (JWT required)
- `DELETE /language-sets/{id}` — delete a Testimony permanently (admin JWT required)
- `POST /language-sets/{id}/languages` — add a language to a Testimony (JWT required)
- `GET /language-sets/{id}/languages` — list all languages in a Testimony
- `DELETE /language-sets/{id}/languages/{item_id}` — remove a language (JWT required)
- `GET /language-sets/{id}/insights` — full analysis: endangerment breakdown, family diversity, geographic spread, languages likely extinct before 2100, least documented language

### Analytics
- `GET /analytics/similarity` — normalised 0–1 similarity score between two languages
- `POST /analytics/compare-sets` — overlap comparison between two Testimonies
- `GET /analytics/outliers` — languages with missing classification, isolate status, or very low parameter coverage
- `GET /analytics/lineage/{language_id}` — trace a language back to its oldest known ancestor
- `GET /analytics/coverage/{language_id}` — typological parameter coverage score
- `GET /analytics/language-sets/{set_id}/profile` — family distribution, macroarea coverage, and diversity score for a Testimony

### Ask the Atlas
- `POST /ask` — submit a natural language question; routed to appropriate analytical endpoints via the Anthropic API

---

## Deployment on Railway

The application is deployed on Railway with two services: a Uvicorn web service running on port 8080 and a managed PostgreSQL instance with a persistent volume attached.

### How it works

- `DATABASE_URL` is injected at runtime via Railway's variable reference syntax (`${{Postgres.DATABASE_URL}}`), linking the two services without hardcoding connection strings
- `API_KEY`, `SECRET_KEY`, and `ANTHROPIC_API_KEY` are set as separate Railway service variables
- Deployments trigger automatically on every push to main via GitHub integration
- The Railway database was seeded remotely by running the seed script locally against `DATABASE_PUBLIC_URL`

### Redeploying from scratch

1. Create a new Railway project with a PostgreSQL plugin
2. Add the environment variables in the Railway dashboard
3. Connect the GitHub repository — Railway will deploy automatically
4. Run the seed script locally pointing at `DATABASE_PUBLIC_URL`

---

## Security

All endpoints are protected using API key authentication via the `X-API-Key` request header. The API key provides a consistent baseline access control layer across all endpoints and protects the Anthropic-powered `/ask` endpoint from unconstrained use. Write operations on language sets additionally require a JWT bearer token issued on successful login. Delete operations are restricted to admin users via a role guard on the token payload.
```http
X-API-Key: secret123
Authorization: Bearer your_jwt_token
```

Raw passwords are never stored — bcrypt hashing is applied at registration and verified at login.

---

## GenAI usage

Generative AI tools including Claude and ChatGPT were used throughout this project for architecture research, feature design, debugging, and MCP server implementation. Full conversation logs are included in the technical report appendix as required by the assessment brief.