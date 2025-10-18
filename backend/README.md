# Unfreeze Backend

FastAPI backend with Supabase integration support.

## Getting Started

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Start the server:
```bash
python run.py
```

The API will be available at [http://localhost:8000](http://localhost:8000)

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Required:
- `API_HOST` - Host to bind to (default: 0.0.0.0)
- `API_PORT` - Port to bind to (default: 8000)
- `ALLOWED_ORIGINS` - CORS allowed origins

Optional (for Supabase):
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration
│   ├── api/
│   │   ├── routes.py     # Main API routes
│   │   └── supabase_routes.py  # Supabase endpoints
│   └── services/
│       └── supabase_client.py  # Supabase integration
├── requirements.txt
└── run.py               # Development server
```

## Supabase Integration

1. Create a project at [supabase.com](https://supabase.com)
2. Add your credentials to `.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

3. Use the client in your code:
```python
from app.services.supabase_client import get_supabase_client

supabase = get_supabase_client()
if supabase:
    response = supabase.table('table_name').select("*").execute()
```

## Features

- ⚡ FastAPI with async support
- 🔒 CORS configured
- 📝 Auto-generated docs
- 🗄️ Supabase ready
- ⚙️ Environment config
- 🎯 Type hints with Pydantic

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)

