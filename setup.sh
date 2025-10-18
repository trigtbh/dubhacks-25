#!/bin/bash

# Unfreeze Project Setup Script
# This script sets up both frontend and backend for development

set -e

echo "🚀 Setting up Unfreeze project..."
echo ""

# Setup Frontend
echo "📦 Setting up Frontend..."
cd frontend
if [ ! -f ".env.local" ]; then
    cp .env.local.example .env.local 2>/dev/null || echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi
echo "✅ Frontend environment file created"

if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install
else
    echo "✅ Frontend dependencies already installed"
fi
cd ..

# Setup Backend
echo ""
echo "🐍 Setting up Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "📥 Installing backend dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || cat > .env << EOL
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOL
fi
echo "✅ Backend environment file created"

cd ..

echo ""
echo "✨ Setup complete! ✨"
echo ""
echo "To start development:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  python run.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

