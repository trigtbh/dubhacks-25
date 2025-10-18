# 🚀 Quick Start Guide

Get up and running with Unfreeze in 5 minutes!

## Automated Setup (Recommended)

Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- ✅ Install all dependencies
- ✅ Create environment files
- ✅ Set up Python virtual environment

## Manual Setup

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local
```

## Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python run.py
```

✅ Backend running at: http://localhost:8000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

✅ Frontend running at: http://localhost:3000

## What's Included

### Frontend ⚛️
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Beautiful, responsive UI
- Dark mode support
- API integration ready

### Backend 🐍
- FastAPI with async support
- CORS configured
- Auto-generated API docs
- Supabase integration ready
- Type-safe with Pydantic

## Next Steps

1. **View the app**: Open http://localhost:3000
2. **Check API docs**: Visit http://localhost:8000/docs
3. **Add Supabase** (optional):
   - Create project at supabase.com
   - Add credentials to `backend/.env`
   - Test at http://localhost:8000/supabase/status

## Useful Links

- 📚 [Full Documentation](./README.md)
- 🎯 API Docs: http://localhost:8000/docs
- 🎨 Frontend: http://localhost:3000

## Troubleshooting

**Backend won't start?**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Check Python version: `python --version` (need 3.9+)

**Frontend won't start?**
- Check Node version: `node --version` (need 18+)
- Try: `rm -rf node_modules && npm install`

**API connection failed?**
- Ensure backend is running on port 8000
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`

## Happy Hacking! 🎉

