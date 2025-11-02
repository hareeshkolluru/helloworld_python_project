# Hell### Backend
- 🚀 **FastAPI** framework for high performance
- 🔤 **Type hints** throughout with Pydantic validation
- 🧪 **Pytest** for comprehensive testing
- 🔒 **CORS** middleware configured
- ⚙️ **Environment-based** configuration
- 📊 **Automatic API documentation** (Swagger/OpenAPI)
- 📷 **Image upload** and storage
- 🗂️ **Timeline API** for image posts
- 🧠 **AI-powered image indexing** with LlamaIndex
- 🔍 **Vector embeddings** stored in PostgreSQL with pgvector
- 🤖 **Automatic caption generation** using OpenAI GPT-4o-ministAPI Full-Stack Project

A modern full-stack web application with FastAPI backend and React frontend, featuring image uploads and timeline display with Material Design and Apple Human Interface principles.

## Features

### Backend
- 🚀 **FastAPI** framework for high performance
- � **Type hints** throughout with Pydantic validation
- 🧪 **Pytest** for comprehensive testing
- 🔒 **CORS** middleware configured
- ⚙️ **Environment-based** configuration
- 📊 **Automatic API documentation** (Swagger/OpenAPI)
- 📷 **Image upload** and storage
- 🗂️ **Timeline API** for image posts

### Frontend
- ⚛️ **React 18** with TypeScript
- ⚡ **Vite** for blazing-fast development
- 🎨 **Material-UI (MUI)** components
- 🍎 **Apple Human Interface** design principles
- 📱 **Responsive** design
- 🖼️ **Image upload** with preview
- 📰 **Timeline view** with smooth animations

## Project Structure

```
helloworld_python_project/
├── src/                     # Backend Python source
│   ├── __init__.py
│   ├── main.py             # FastAPI application entry point
│   ├── config.py           # Configuration management
│   ├── models.py           # Pydantic models
│   ├── routes.py           # API route handlers (including image endpoints)
│   ├── database.py         # Database connection and session management
│   ├── db_models.py        # SQLAlchemy database models with vector support
│   └── indexing_service.py # LlamaIndex image embedding service
├── frontend/               # Frontend React application
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── ImageUpload.tsx
│   │   │   └── Timeline.tsx
│   │   ├── App.tsx         # Main app component
│   │   ├── main.tsx        # React entry point
│   │   ├── types.ts        # TypeScript types
│   │   └── index.css       # Global styles
│   ├── package.json
│   ├── vite.config.ts      # Vite configuration with proxy
│   └── tsconfig.json
├── tests/                  # Backend tests
│   ├── conftest.py
│   ├── test_config.py
│   └── test_routes.py
├── uploads/                # Uploaded images storage (created automatically)
├── .env.example            # Example environment variables
├── pyproject.toml          # Python dependencies and configuration
├── dev.sh                  # Full-stack development startup script
├── run.sh                  # Backend-only startup script
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher (for frontend)
- **Docker Desktop** (for PostgreSQL database)
- **OpenAI API Key** (for image embedding and caption generation)
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip
- npm or yarn (for frontend dependencies)

> **📦 Docker Required**: This application uses PostgreSQL running in Docker. See [DOCKER_SETUP.md](DOCKER_SETUP.md) for installation instructions.

### Installation

#### Quick Start (Full-Stack)

1. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone and navigate to the project:
   ```bash
   cd helloworld_python_project
   ```

3. Install backend dependencies:
   ```bash
   uv sync --extra dev
   ```

4. Install frontend dependencies:
   ```bash
   cd frontend && npm install && cd ..
   ```

5. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

6. Start both backend and frontend:
   ```bash
   ./dev.sh
   ```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

#### Option 1: Using uv (Recommended)

1. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Navigate to the project directory:
   ```bash
   cd helloworld_python_project
   ```

3. Sync dependencies (this creates a virtual environment and installs all dependencies):
   ```bash
   uv sync --extra dev
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

#### Option 2: Using pip

1. Navigate to the project directory:
   ```bash
   cd helloworld_python_project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

### Running the Application

#### Full-Stack Development Mode (Recommended)
```bash
./dev.sh
```

This will start both the backend (port 8000) and frontend (port 3000) concurrently.

#### Backend Only

Using uv:
```bash
uv run python -m src.main
```

Or using uvicorn directly:
```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Or with the run script:
```bash
./run.sh
```

#### Frontend Only

```bash
cd frontend && npm run dev
```

The applications will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### API Endpoints

#### Core Endpoints
- **GET** `/` - Welcome message
- **GET** `/api/v1/health` - Health check
- **GET** `/api/v1/hello` - Simple greeting

#### Image Endpoints
- **POST** `/api/v1/images` - Upload an image with optional caption
  - Accepts: `multipart/form-data`
  - Fields: `file` (image), `caption` (optional string)
  - Automatically generates embeddings and stores in PostgreSQL with pgvector
  - Auto-generates caption if none provided using GPT-4o-mini
- **GET** `/api/v1/images` - Get all uploaded images (timeline)
- **GET** `/api/v1/images/{filename}` - Serve a specific image file

## AI-Powered Features

This application uses **LlamaIndex** and **OpenAI** to provide intelligent image processing:

### Automatic Image Indexing
When you upload an image, the system:
1. 🖼️ **Analyzes the image** using GPT-4o-mini multimodal model
2. 📝 **Generates a detailed description** of the image content
3. 🔢 **Creates a 1536-dimension embedding vector** from the description
4. 💾 **Stores the embedding** in PostgreSQL using pgvector extension
5. 🤖 **Auto-generates a caption** if you don't provide one

### Vector Search Capabilities
The embeddings stored in pgvector enable:
- **Semantic image search** - Find similar images by meaning, not just metadata
- **Content-based recommendations** - Suggest related images
- **Advanced querying** - Search images by describing what you're looking for

### Technologies Used
- **LlamaIndex**: Framework for connecting LLMs with data
- **OpenAI GPT-4o-mini**: Multimodal model for image understanding
- **text-embedding-3-small**: Efficient embedding model (1536 dimensions)
- **pgvector**: PostgreSQL extension for vector similarity search

### Setup Requirements
To enable AI features, you need:
1. An OpenAI API key (get one at https://platform.openai.com/api-keys)
2. Add to your `.env` file:
   ```bash
   OPENAI_API_KEY=sk-your-api-key-here
   ```

> **Note**: If the OpenAI API key is not configured, images will still upload successfully, but embedding generation will be skipped and captions won't be auto-generated.

### Testing

#### Using uv
```bash
uv run pytest
```

Run tests with coverage:
```bash
uv run pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
uv run pytest tests/test_routes.py
```

#### Using activated virtual environment
```bash
pytest
pytest --cov=src --cov-report=html
pytest tests/test_routes.py
```

### Code Quality

#### Using uv

Linting with Ruff:
```bash
uv run ruff check .
```

Auto-fix issues:
```bash
uv run ruff check --fix .
```

Type Checking with mypy:
```bash
uv run mypy src
```

Format Code:
```bash
uv run ruff format .
```

#### Using activated virtual environment

```bash
ruff check .
ruff check --fix .
mypy src
ruff format .
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for available options:

- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `DEBUG`: Enable debug mode
- `HOST`: Server host
- `PORT`: Server port
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
- `API_V1_PREFIX`: API version prefix
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for embeddings and captions (**required**)

## Package Management with uv

This project is configured to use [uv](https://docs.astral.sh/uv/), a fast Python package installer and resolver written in Rust.

### Common uv Commands

```bash
# Sync dependencies (install/update based on uv.lock)
uv sync

# Sync with development dependencies
uv sync --extra dev

# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Remove a dependency
uv remove <package-name>

# Update dependencies
uv lock --upgrade

# Run a command in the virtual environment
uv run <command>

# Run Python scripts
uv run python script.py
```

### Benefits of uv

- ⚡ **10-100x faster** than pip
- 🔒 **Deterministic builds** with `uv.lock`
- 🎯 **Better dependency resolution**
- 🛠️ **Built-in virtual environment management**
- 📦 **Compatible with pip and PyPI**

## Development

### Adding New Endpoints

1. Define your Pydantic models in `src/models.py`
2. Create route handlers in `src/routes.py` or create a new router file
3. Register the router in `src/main.py`
4. Add tests in `tests/`

### Example: Adding a New Route

```python
# In src/routes.py
@router.get("/example", response_model=ExampleResponse)
async def example_endpoint() -> ExampleResponse:
    return ExampleResponse(data="example")
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.