# 🎯 Unfreeze - Project Overview

## What is Unfreeze?

Unfreeze is a modern full-stack application template built for DubHacks 2025, featuring:
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Python
- **Database Ready**: Pre-configured Supabase integration

## 📁 Project Structure

```
dubhacks-25/
├── frontend/                    # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx          # Root layout with metadata
│   │   ├── page.tsx            # Main page with interactive UI
│   │   └── globals.css         # Global styles with Tailwind
│   ├── package.json            # Node dependencies
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tailwind.config.ts      # Tailwind CSS config
│   ├── next.config.mjs         # Next.js configuration
│   └── postcss.config.mjs      # PostCSS configuration
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── config.py           # Environment configuration
│   │   ├── api/
│   │   │   ├── routes.py       # Main API endpoints
│   │   │   └── supabase_routes.py  # Supabase endpoints
│   │   └── services/
│   │       └── supabase_client.py  # Supabase integration
│   ├── requirements.txt        # Python dependencies
│   └── run.py                  # Development server script
│
├── README.md                    # Main documentation
├── QUICKSTART.md               # Quick start guide
├── setup.sh                    # Automated setup script
└── .gitignore                  # Git ignore rules
```

## 🎨 Frontend Features

### Technology Stack
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client for API calls

### UI Components
- Beautiful gradient backgrounds
- Dark mode support (system preference)
- Responsive design for all screen sizes
- Interactive form with real-time API integration
- Status indicators and loading states
- Modern card-based layout

### Key Files

**`app/page.tsx`**
- Main application page
- API integration example
- Form handling with state management
- Error handling and loading states

**`app/layout.tsx`**
- Root layout component
- Metadata configuration
- Global font settings

**`app/globals.css`**
- Tailwind directives
- CSS variables for theming
- Dark mode support

## 🐍 Backend Features

### Technology Stack
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Supabase**: PostgreSQL database client

### API Endpoints

#### Core Endpoints
- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /status` - API operational status

#### Application Endpoints
- `POST /unfreeze` - Main processing endpoint
  - Request: `{ "text": "string" }`
  - Response: `{ "message": "string", "input": "string", "timestamp": "string" }`

#### Supabase Endpoints
- `GET /supabase/status` - Check Supabase configuration

### Key Files

**`app/main.py`**
- FastAPI application initialization
- CORS middleware configuration
- Route registration
- Health check endpoints

**`app/config.py`**
- Environment variable management
- Settings validation with Pydantic
- Configuration defaults

**`app/api/routes.py`**
- Main API route definitions
- Request/response models
- Business logic

**`app/services/supabase_client.py`**
- Supabase client singleton
- Helper methods for database operations
- Configuration validation

## 🗄️ Supabase Integration

### Setup Process

1. **Create Supabase Project**
   - Visit [supabase.com](https://supabase.com)
   - Create new project
   - Note your project URL and anon key

2. **Configure Backend**
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   ```

3. **Test Connection**
   ```bash
   curl http://localhost:8000/supabase/status
   ```

### Using Supabase

```python
from app.services.supabase_client import get_supabase_client

# Get client
supabase = get_supabase_client()

# Query data
response = supabase.table('users').select("*").execute()

# Insert data
supabase.table('users').insert({"name": "John"}).execute()

# Update data
supabase.table('users').update({"name": "Jane"}).eq('id', 1).execute()

# Delete data
supabase.table('users').delete().eq('id', 1).execute()
```

## 🔧 Configuration

### Environment Variables

**Frontend (`.env.local`)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (`.env`)**
```env
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
```

## 🚀 Development Workflow

### Setup (First Time)
```bash
# Automated
./setup.sh

# Or manual - see QUICKSTART.md
```

### Daily Development

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

### Making Changes

1. **Add New API Endpoint**
   - Add route in `backend/app/api/routes.py`
   - Define Pydantic models
   - Update frontend to call new endpoint

2. **Add New Frontend Page**
   - Create new file in `frontend/app/`
   - Add route automatically (App Router)
   - Link from existing pages

3. **Add Supabase Table**
   - Create table in Supabase dashboard
   - Add types/models
   - Create API endpoints
   - Update frontend to use new data

## 📚 API Documentation

Once backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These are automatically generated from your FastAPI code!

## 🎯 Next Steps

### Immediate Tasks
1. Run the setup script
2. Start both servers
3. Test the application
4. Customize the UI and add your features

### Features to Add
- User authentication
- Database models and tables
- Business logic in API routes
- Additional frontend pages
- File uploads
- Real-time features
- Email notifications

### Deployment Considerations
- Set production environment variables
- Update CORS origins
- Configure database connection pooling
- Set up CI/CD pipeline
- Enable HTTPS
- Add monitoring and logging

## 🛠️ Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend Framework | Next.js 14 | React framework with SSR |
| Frontend Language | TypeScript | Type-safe JavaScript |
| Styling | Tailwind CSS | Utility-first CSS |
| Backend Framework | FastAPI | Modern Python API framework |
| API Validation | Pydantic | Data validation |
| Database | Supabase | PostgreSQL with REST API |
| HTTP Client | Axios | Promise-based requests |
| Server | Uvicorn | ASGI server |

## 📖 Learning Resources

- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Supabase Guides](https://supabase.com/docs/guides)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 💡 Tips

1. **Use TypeScript**: Catch errors before runtime
2. **Follow RESTful conventions**: Keep APIs predictable
3. **Handle errors gracefully**: Always validate input
4. **Keep secrets safe**: Never commit .env files
5. **Write tests**: Add pytest for backend, Jest for frontend
6. **Document code**: Use docstrings and comments
7. **Use version control**: Commit often with clear messages

## 🤝 Contributing

This is your hackathon project! Feel free to:
- Modify any code
- Add new features
- Refactor architecture
- Experiment and learn

## 📝 License

MIT License - Use this however you want!

---

**Good luck at DubHacks 2025!** 🚀

If you have questions, check the documentation or API docs at http://localhost:8000/docs

