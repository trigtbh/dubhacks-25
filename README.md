# Unfreeze

A modern full-stack application built with Next.js (TypeScript) and FastAPI (Python), running on Oracle Cloud with Cloudflare services (D1 database and KV storage).

## 🏗️ Architecture

- **Frontend**: Next.js 14 with TypeScript (deployable to Cloudflare Pages)
- **Backend**: FastAPI running on Oracle Cloud
- **Database**: Cloudflare D1 (SQLite-compatible)
- **Storage**: Cloudflare KV (Key-Value store)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Configure Cloudflare

Follow the [Cloudflare Setup Guide](./cloudflare/README.md) to:
- Create D1 database
- Create KV namespace
- Get API credentials

Then update `backend/.env`:
```env
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_D1_DATABASE_ID=your_database_id
CLOUDFLARE_KV_NAMESPACE_ID=your_namespace_id
```

### 3. Start Development

**Terminal 1 - Backend (Oracle Cloud compatible)**
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
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📚 Documentation

- **[START_HERE.md](./START_HERE.md)** - Quick start guide
- **[QUICKSTART.md](./QUICKSTART.md)** - Detailed setup
- **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** - Architecture details
- **[cloudflare/README.md](./cloudflare/README.md)** - Cloudflare setup
- **[backend/README.md](./backend/README.md)** - Backend docs
- **[frontend/README.md](./frontend/README.md)** - Frontend docs

## 🔧 Key Features

### Backend (FastAPI on Oracle Cloud)
- ⚡ Fast async Python API
- 🗄️ Cloudflare D1 database integration
- 💾 Cloudflare KV storage
- 📝 Auto-generated API docs
- 🔒 CORS configured

### Frontend (Next.js)
- ⚛️ React 18 with TypeScript
- 💅 Tailwind CSS styling
- 🌓 Dark mode support
- 📱 Responsive design
- ☁️ Cloudflare Pages ready

### Cloudflare Services
- 🗄️ D1: SQLite-compatible database
- 💾 KV: Fast key-value storage
- 🌍 Global edge network
- 🚀 Serverless architecture

## 📖 API Endpoints

### Core
- `GET /` - Health check
- `GET /health` - Detailed status
- `POST /unfreeze` - Main endpoint

### Cloudflare D1
- `GET /cloudflare/d1/status` - Database status
- `POST /cloudflare/d1/query` - Execute SQL query
- `POST /cloudflare/d1/batch` - Batch queries

### Cloudflare KV
- `GET /cloudflare/kv/status` - KV status
- `GET /cloudflare/kv/{key}` - Get value
- `PUT /cloudflare/kv` - Store value
- `DELETE /cloudflare/kv/{key}` - Delete value

## 🚀 Deployment

### Backend on Oracle Cloud

1. **Create Oracle Cloud Compute Instance**
   - Choose Ubuntu/AlmaLinux
   - Open ports 80, 443, 8000

2. **Deploy Backend**
```bash
# On Oracle Cloud instance
git clone your-repo
cd dubhacks-25/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Add .env with Cloudflare credentials
python run.py
```

3. **Setup Nginx (optional)**
```bash
sudo apt install nginx
# Configure reverse proxy for production
```

### Frontend on Cloudflare Pages

1. Push code to GitHub
2. Go to Cloudflare Pages
3. Connect repository
4. Set build settings:
   - Build command: `cd frontend && npm install && npm run build`
   - Build output: `frontend/.next`
   - Root directory: `/`
5. Add environment variable:
   - `NEXT_PUBLIC_API_URL`: Your Oracle Cloud backend URL
6. Deploy!

## 🗄️ Database Setup

Initialize your D1 database:

```bash
cd cloudflare
wrangler d1 create unfreeze-db
wrangler d1 execute unfreeze-db --file=./schema.sql
```

## 💡 Development Tips

1. **Test Cloudflare locally**: Use Wrangler CLI
2. **Monitor Oracle Cloud**: Set up logging and monitoring
3. **Secure your API**: Add authentication middleware
4. **Use environment variables**: Never commit secrets

## 📝 License

MIT License - feel free to use this project!

---

Built with ❤️ for DubHacks 2025

**Stack**: Next.js + FastAPI + Oracle Cloud + Cloudflare
