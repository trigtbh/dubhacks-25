# Unfreeze Backend

FastAPI backend designed to run on Oracle Cloud with Cloudflare D1 database and KV storage.

## Architecture

- **Runtime**: Python 3.9+ on Oracle Cloud
- **Framework**: FastAPI (async)
- **Database**: Cloudflare D1 (SQLite-compatible)
- **Cache/Storage**: Cloudflare KV
- **API Style**: RESTful with auto-docs

## Getting Started

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Cloudflare

See [../cloudflare/README.md](../cloudflare/README.md) for detailed setup.

Quick setup:
```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create D1 database
wrangler d1 create unfreeze-db

# Create KV namespace
wrangler kv:namespace create "KV"
```

### 3. Environment Variables

Copy `.env.example` to `.env` and fill in your Cloudflare credentials:

```env
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_D1_DATABASE_ID=your_database_id
CLOUDFLARE_KV_NAMESPACE_ID=your_kv_namespace_id
```

### 4. Start Server

```bash
python run.py
```

API available at: http://localhost:8000
Docs available at: http://localhost:8000/docs

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Environment config
│   ├── api/
│   │   ├── routes.py        # Main routes
│   │   └── cloudflare_routes.py  # Cloudflare endpoints
│   └── services/
│       └── cloudflare_client.py  # D1 & KV client
├── requirements.txt
└── run.py
```

## Using Cloudflare Services

### D1 Database

```python
from app.services.cloudflare_client import get_d1_client

d1 = get_d1_client()

# Query with parameters
result = await d1.query(
    "SELECT * FROM users WHERE id = ?",
    [user_id]
)

# Batch queries
results = await d1.batch([
    ("INSERT INTO users (name) VALUES (?)", ["John"]),
    ("SELECT * FROM users", [])
])
```

### KV Storage

```python
from app.services.cloudflare_client import get_kv_client

kv = get_kv_client()

# Store value
await kv.put("user:123", "John Doe", expiration_ttl=3600)

# Get value
value = await kv.get("user:123")

# Delete value
await kv.delete("user:123")

# List keys
keys = await kv.list_keys(prefix="user:", limit=100)
```

## API Endpoints

### Health & Status
- `GET /` - Health check
- `GET /health` - Detailed health status

### Application
- `POST /unfreeze` - Main application endpoint
- `GET /status` - Application status

### Cloudflare D1
- `GET /cloudflare/d1/status` - Check D1 connection
- `POST /cloudflare/d1/query` - Execute SQL query
- `POST /cloudflare/d1/batch` - Execute batch queries

### Cloudflare KV
- `GET /cloudflare/kv/status` - Check KV status
- `GET /cloudflare/kv/{key}` - Get value by key
- `PUT /cloudflare/kv` - Store key-value pair
- `DELETE /cloudflare/kv/{key}` - Delete key
- `GET /cloudflare/kv/list/keys` - List keys

### Info
- `GET /cloudflare/info` - Cloudflare services info

## Deployment on Oracle Cloud

### Option 1: Direct Deployment

```bash
# On Oracle Cloud instance
git clone your-repo
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add environment variables
nano .env

# Run with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Option 2: With Systemd (Production)

Create `/etc/systemd/system/unfreeze-api.service`:

```ini
[Unit]
Description=Unfreeze FastAPI
After=network.target

[Service]
User=opc
WorkingDirectory=/home/opc/backend
Environment="PATH=/home/opc/backend/venv/bin"
ExecStart=/home/opc/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable unfreeze-api
sudo systemctl start unfreeze-api
sudo systemctl status unfreeze-api
```

### Option 3: With Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_HOST` | No | Host to bind (default: 0.0.0.0) |
| `API_PORT` | No | Port to bind (default: 8000) |
| `ENVIRONMENT` | No | development/production |
| `ALLOWED_ORIGINS` | No | CORS origins |
| `CLOUDFLARE_ACCOUNT_ID` | Yes* | Your Cloudflare account ID |
| `CLOUDFLARE_API_TOKEN` | Yes* | API token with D1/KV permissions |
| `CLOUDFLARE_D1_DATABASE_ID` | Yes* | D1 database ID |
| `CLOUDFLARE_KV_NAMESPACE_ID` | No | KV namespace ID |

*Required for Cloudflare features

## Development

```bash
# Start dev server with auto-reload
python run.py

# Or use uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Cloudflare D1 Docs](https://developers.cloudflare.com/d1/)
- [Cloudflare KV Docs](https://developers.cloudflare.com/kv/)
- [Oracle Cloud Docs](https://docs.oracle.com/en-us/iaas/Content/home.htm)
