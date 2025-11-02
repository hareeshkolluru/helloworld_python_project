# Quick Reference Guide

## Full-Stack Setup Commands

### First Time Setup
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install backend dependencies
uv sync --extra dev

# Install frontend dependencies
cd frontend && npm install && cd ..

# Copy environment variables
cp .env.example .env
```

### Start Development (Both Frontend & Backend)
```bash
# Quick start - runs both servers
./dev.sh

# Or start separately:
# Terminal 1 - Backend
uv run uvicorn src.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

## Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React application with image upload and timeline |
| Backend API | http://localhost:8000 | FastAPI server |
| Swagger Docs | http://localhost:8000/docs | Interactive API documentation |
| ReDoc | http://localhost:8000/redoc | Alternative API documentation |

## API Endpoints

### Core Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/hello` | Simple greeting |
| GET | `/api/v1/hello?name=John` | Personalized greeting |

### Image Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/images` | Upload image with optional caption |
| GET | `/api/v1/images` | Get all images (timeline) |
| GET | `/api/v1/images/{filename}` | Serve specific image file |

## Development Commands

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test
uv run pytest tests/test_routes.py -v
```

### Code Quality
```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run mypy src

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Dependency Management
```bash
# Add new dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Remove dependency
uv remove <package>

# Update all dependencies
uv lock --upgrade
uv sync
```

## Project Structure

```
helloworld_python_project/
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py            # FastAPI app & entry point
│   ├── config.py          # Settings management
│   ├── models.py          # Pydantic models
│   └── routes.py          # API endpoints
├── tests/                 # Test suite
│   ├── conftest.py        # Test fixtures
│   ├── test_config.py
│   └── test_routes.py
├── .env.example           # Environment template
├── .gitignore
├── pyproject.toml         # Project config
├── uv.lock               # Locked dependencies
├── run.sh                # Quick start script
└── README.md
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| APP_NAME | "HelloWorld FastAPI" | Application name |
| APP_VERSION | "0.1.0" | Application version |
| DEBUG | true | Debug mode |
| HOST | 0.0.0.0 | Server host |
| PORT | 8000 | Server port |
| CORS_ORIGINS | http://localhost:3000 | CORS allowed origins |
| API_V1_PREFIX | /api/v1 | API version prefix |

## Useful URLs (when running)

- **Application**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
