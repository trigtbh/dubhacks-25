# 👋 Welcome to Unfreeze!

A full-stack app running on **Oracle Cloud** with **Cloudflare** services (D1 database & KV storage).

## 🎯 What You Have

✅ **Frontend**: Next.js 14 with TypeScript + Tailwind CSS  
✅ **Backend**: FastAPI (Python) for Oracle Cloud  
✅ **Database**: Cloudflare D1 (SQLite-compatible)  
✅ **Storage**: Cloudflare KV (Key-Value)  
✅ **Documentation**: Complete setup guides  

## 🏗️ Architecture

```
┌─────────────────┐
│  Cloudflare     │
│  Pages          │  ← Frontend (Next.js)
│  (Frontend)     │
└────────┬────────┘
         │
         │ API Calls
         ↓
┌─────────────────┐     ┌──────────────────┐
│  Oracle Cloud   │────→│  Cloudflare      │
│  Compute        │     │  - D1 Database   │
│  (FastAPI)      │←────│  - KV Storage    │
└─────────────────┘     └──────────────────┘
```

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Dependencies

```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Setup Cloudflare Services

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create D1 database
cd cloudflare
wrangler d1 create unfreeze-db

# Initialize schema
wrangler d1 execute unfreeze-db --file=./schema.sql

# Create KV namespace
wrangler kv:namespace create "KV"
```

**Copy the IDs** and add to `backend/.env`:
```env
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_D1_DATABASE_ID=from_wrangler_output
CLOUDFLARE_KV_NAMESPACE_ID=from_wrangler_output
```

### Step 3: Start Development

**Terminal 1 - Backend**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend**
```bash
cd frontend
npm run dev
```

Visit:
- 🎨 Frontend: http://localhost:3000
- 🔌 API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## 📚 Full Documentation

- **[README.md](./README.md)** - Complete overview
- **[QUICKSTART.md](./QUICKSTART.md)** - Detailed setup
- **[cloudflare/README.md](./cloudflare/README.md)** - Cloudflare guide
- **[backend/README.md](./backend/README.md)** - Backend docs
- **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** - Architecture

## 🧪 Test Your Setup

### Test Backend
```bash
curl http://localhost:8000/health
```

### Test Cloudflare D1
```bash
curl http://localhost:8000/cloudflare/d1/status
```

### Test Cloudflare KV
```bash
curl http://localhost:8000/cloudflare/kv/status
```

## 🗄️ Database Operations

### Query D1 Database
```bash
# Via Wrangler
wrangler d1 execute unfreeze-db --command="SELECT * FROM users"

# Via API
curl -X POST http://localhost:8000/cloudflare/d1/query \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT * FROM users","params":[]}'
```

### Use KV Storage
```bash
# Store value
curl -X PUT http://localhost:8000/cloudflare/kv \
  -H "Content-Type: application/json" \
  -d '{"key":"test","value":"Hello World"}'

# Get value
curl http://localhost:8000/cloudflare/kv/test
```

## 🚀 Deployment

### Backend → Oracle Cloud

1. Create Oracle Cloud Compute instance
2. SSH into instance
3. Clone repo and install dependencies
4. Add `.env` with Cloudflare credentials
5. Run with systemd or PM2

See [backend/README.md](./backend/README.md) for details.

### Frontend → Cloudflare Pages

1. Push to GitHub
2. Connect to Cloudflare Pages
3. Set build command: `cd frontend && npm run build`
4. Add `NEXT_PUBLIC_API_URL` environment variable
5. Deploy!

## 🔧 Common Commands

```bash
# Backend
cd backend
source venv/bin/activate
python run.py

# Frontend
cd frontend
npm run dev

# Cloudflare D1
wrangler d1 list
wrangler d1 execute unfreeze-db --command="SQL HERE"

# Cloudflare KV
wrangler kv:key put --namespace-id=YOUR_ID "key" "value"
wrangler kv:key get --namespace-id=YOUR_ID "key"
```

## ❓ Troubleshooting

**Cloudflare credentials not working?**
- Double-check Account ID in dashboard
- Ensure API token has D1 and KV permissions
- Verify database and namespace IDs

**Backend can't connect to Cloudflare?**
```bash
# Test manually with curl
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/d1/database
```

**Frontend can't reach backend?**
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/config.py`

## 💡 Quick Tips

1. **Cloudflare is free tier friendly** - D1 and KV have generous limits
2. **Oracle Cloud has free tier** - Perfect for hosting the backend
3. **Use Wrangler for DB management** - Easier than API calls
4. **Check API docs** at http://localhost:8000/docs - Interactive!
5. **D1 is SQLite** - Use standard SQLite syntax

## 🎯 Next Steps

1. ✅ Get everything running locally
2. 📝 Customize the database schema in `cloudflare/schema.sql`
3. 🎨 Build your UI in `frontend/app/page.tsx`
4. 🔌 Add API endpoints in `backend/app/api/routes.py`
5. 🚀 Deploy to production!

## 📖 Resources

- [Cloudflare D1 Docs](https://developers.cloudflare.com/d1/)
- [Cloudflare KV Docs](https://developers.cloudflare.com/kv/)
- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)

---

**Happy Hacking!** 🎉

For questions, check the documentation or API docs at http://localhost:8000/docs
