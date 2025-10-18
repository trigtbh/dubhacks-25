# 🚀 Quick Start Guide

Get Unfreeze running with Oracle Cloud + Cloudflare in 10 minutes!

## Prerequisites

- Node.js (v18+)
- Python (v3.9+)
- Cloudflare account (free)
- Optional: Oracle Cloud account (for deployment)

## Step 1: Install Project Dependencies

### Automated Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## Step 2: Setup Cloudflare

### Install Wrangler CLI
```bash
npm install -g wrangler
```

### Login to Cloudflare
```bash
wrangler login
```

### Create D1 Database
```bash
cd cloudflare

# Create database
wrangler d1 create unfreeze-db
```

You'll see output like:
```
✅ Successfully created DB 'unfreeze-db'!

[[d1_databases]]
binding = "DB"
database_name = "unfreeze-db"
database_id = "xxxx-xxxx-xxxx-xxxx"  ← COPY THIS
```

### Initialize Database Schema
```bash
wrangler d1 execute unfreeze-db --file=./schema.sql
```

### Create KV Namespace
```bash
wrangler kv:namespace create "KV"
```

Output:
```
✅ Successfully created KV namespace!

[[kv_namespaces]]
binding = "KV"
id = "xxxxxxxxxxxx"  ← COPY THIS
```

### Get API Credentials

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Copy your **Account ID** (shown in the right sidebar)
3. Go to **Profile** → **API Tokens** → **Create Token**
4. Use template: **Edit Cloudflare Workers**
5. Add permissions:
   - Account > D1 > Edit
   - Account > Workers KV Storage > Edit
6. Create and copy the token

## Step 3: Configure Backend

Create `backend/.env`:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Cloudflare Configuration
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_API_TOKEN=your_api_token_here
CLOUDFLARE_D1_DATABASE_ID=your_d1_database_id_here
CLOUDFLARE_KV_NAMESPACE_ID=your_kv_namespace_id_here
```

## Step 4: Configure Frontend

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 5: Start Development Servers

### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate
python run.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

Expected output:
```
▲ Next.js 14.x.x
- Local:        http://localhost:3000
✓ Ready in 2.3s
```

## Step 6: Verify Everything Works

### Test Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "platform": {
    "hosting": "Oracle Cloud",
    "services": "Cloudflare (D1, KV)"
  },
  "services": {
    "api": "operational",
    "cloudflare_d1": "configured",
    "cloudflare_kv": "configured"
  }
}
```

### Test D1 Database
```bash
curl http://localhost:8000/cloudflare/d1/status
```

### Test KV Storage
```bash
curl http://localhost:8000/cloudflare/kv/status
```

### Visit Frontend
Open http://localhost:3000 in your browser

## What's Next?

### 1. View API Documentation
Open http://localhost:8000/docs for interactive API docs

### 2. Test Database Operations

**Insert data:**
```bash
curl -X POST http://localhost:8000/cloudflare/d1/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"INSERT INTO users (email, name) VALUES (?, ?)", "params":["test@example.com", "Test User"]}'
```

**Query data:**
```bash
curl -X POST http://localhost:8000/cloudflare/d1/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT * FROM users", "params":[]}'
```

### 3. Test KV Storage

**Store value:**
```bash
curl -X PUT http://localhost:8000/cloudflare/kv \
  -H "Content-Type: application/json" \
  -d '{"key":"greeting","value":"Hello Cloudflare!"}'
```

**Retrieve value:**
```bash
curl http://localhost:8000/cloudflare/kv/greeting
```

### 4. Customize Your App

- **Frontend**: Edit `frontend/app/page.tsx`
- **Backend**: Add routes in `backend/app/api/routes.py`
- **Database**: Modify `cloudflare/schema.sql` and re-run migrations

## Troubleshooting

### Backend won't start

**Check Python version:**
```bash
python3 --version  # Need 3.9+
```

**Activate virtual environment:**
```bash
cd backend
source venv/bin/activate
```

**Reinstall dependencies:**
```bash
pip install -r requirements.txt
```

### Cloudflare connection failed

**Verify credentials:**
```bash
# Test API token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.cloudflare.com/client/v4/user/tokens/verify
```

**Check .env file:**
- Ensure no spaces around `=`
- No quotes around values
- File is named exactly `.env`

### Frontend can't reach backend

**Check backend is running:**
```bash
curl http://localhost:8000/
```

**Verify .env.local:**
```bash
cat frontend/.env.local
# Should show: NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Check CORS settings:**
Backend should allow `http://localhost:3000` in CORS origins

### Port already in use

**Kill process on port 8000:**
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Or use different port
API_PORT=8001 python run.py
```

**Kill process on port 3000:**
```bash
# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

## Useful Commands

### Wrangler D1
```bash
# List databases
wrangler d1 list

# Execute query
wrangler d1 execute unfreeze-db --command="SELECT * FROM users"

# Run SQL file
wrangler d1 execute unfreeze-db --file=./migrations/001_add_column.sql

# Backup database
wrangler d1 export unfreeze-db --output=backup.sql
```

### Wrangler KV
```bash
# List namespaces
wrangler kv:namespace list

# Put key
wrangler kv:key put --namespace-id=YOUR_ID "mykey" "myvalue"

# Get key
wrangler kv:key get --namespace-id=YOUR_ID "mykey"

# Delete key
wrangler kv:key delete --namespace-id=YOUR_ID "mykey"

# List keys
wrangler kv:key list --namespace-id=YOUR_ID
```

### Backend
```bash
# Start server
python run.py

# With specific port
API_PORT=8001 python run.py

# Using uvicorn directly
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
# Development
npm run dev

# Build for production
npm run build

# Start production server
npm run start
```

## Next Steps

1. ✅ Verify everything is running
2. 📖 Read [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) for architecture
3. 🎨 Customize the UI and add features
4. 🚀 Deploy to production (see [README.md](./README.md))

## Resources

- [Cloudflare D1 Documentation](https://developers.cloudflare.com/d1/)
- [Cloudflare KV Documentation](https://developers.cloudflare.com/kv/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)

---

**You're all set!** 🎉

Happy coding! For deployment instructions, check [README.md](./README.md)
