# Interview Orchestrator

A FastAPI-based application for orchestrating and managing interviews.

## Project Structure

```
interviewOrchestrator/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py
│   │       └── endpoints/
│   ├── controllers/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── requirements-dev.txt
├── .env
└── .env.sample
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   # For production
   pip install -r requirements.txt
   
   # For development
   pip install -r requirements-dev.txt
   ```

3. Copy `.env.sample` to `.env` and update the values:
   ```bash
   cp .env.sample .env
   ```

4. Run the application:
   ```bash
   # Development
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Production
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Development

### Code Style

This project uses:
- Black for code formatting
- Flake8 for code linting
- MyPy for type checking
- isort for import sorting

### Running Tests

```bash
pytest
```

### API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Key environment variables:
- `ENV`: development/production
- `DEBUG`: True/False
- `SECRET_KEY`: Your secret key
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins
- `DATABASE_URL`: Database connection string
# testapp
