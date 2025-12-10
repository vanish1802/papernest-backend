# 📚 PaperNest

A modern research paper management system with AI-powered summarization and intelligent chat capabilities.

## ✨ Features

- **User Authentication**: Secure registration and login with session-based authentication
- **Paper Management**: Upload PDFs or manually add research papers with metadata
- **AI Summarization**: Generate concise summaries using Groq's LLM API
- **Intelligent Chat**: Ask questions about your papers using RAG (Retrieval-Augmented Generation)
- **Organization**: Filter papers by status (To Read, Reading, Completed) and priority levels
- **Modern UI**: Clean, responsive interface built with Streamlit

## 🏗️ Architecture

### Backend (FastAPI)
- **API Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Session-based auth with SHA256-hashed passwords (Bcrypt)
- **AI Integration**: Groq API for LLM capabilities
- **RAG System**: Sentence-Transformers for semantic search

### Frontend (Streamlit)
- **UI Framework**: Streamlit for rapid prototyping
- **State Management**: Session-based state handling
- **Real-time Updates**: Dynamic content rendering

### Deployment
- **Platform**: Render (Free Tier)
- **Containerization**: Docker
- **Infrastructure as Code**: `render.yaml` Blueprint

## 🛠️ Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Groq API
- Sentence-Transformers
- PyTorch

**Frontend:**
- Streamlit
- Requests

**DevOps:**
- Docker
- Render
- GitHub Actions (CI/CD ready)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL
- Groq API Key ([Get one here](https://console.groq.com))

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/vanish1802/papernest-backend.git
cd papernest-backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials:
# DATABASE_URL=postgresql://user:pass@localhost:5432/papernest_db
# SECRET_KEY=your-secret-key
# GROQ_API_KEY=your-groq-api-key
```

4. **Run the backend**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Run the frontend** (in a separate terminal)
```bash
export API_URL=http://localhost:8000
streamlit run streamlit_app.py --server.port 8501
```

6. **Access the application**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🌐 Deployment (Render)

### One-Click Deployment

1. Fork this repository
2. Sign up for [Render](https://render.com)
3. Create a new Blueprint
4. Connect your GitHub repository
5. Set the `GROQ_API_KEY` environment variable
6. Click "Apply"

Render will automatically:
- Create a PostgreSQL database
- Deploy the backend service
- Deploy the frontend service
- Link all services together

### Manual Deployment

See the [Migration Guide](docs/migration_guide.md) for detailed instructions.

## 📖 API Documentation

Once the backend is running, visit `/docs` for interactive API documentation (Swagger UI).

### Key Endpoints

**Authentication:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get session ID

**Papers:**
- `GET /papers/` - List all papers
- `POST /papers/` - Create new paper
- `POST /papers/upload` - Upload PDF
- `POST /papers/{id}/summarize` - Generate AI summary
- `POST /papers/{id}/chat` - Chat with paper

**Health:**
- `GET /health` - Check service health and database connection

## 🔒 Security Features

- **Password Hashing**: SHA256 pre-hashing + Bcrypt for secure password storage
- **Session Management**: Secure session-based authentication
- **CORS Protection**: Configurable CORS middleware
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries

## 🎯 Performance Optimizations

- **Lazy Loading**: ML models load on-demand to reduce startup time
- **Caching**: LRU cache for embeddings to speed up multi-turn conversations
- **Async Operations**: FastAPI async endpoints for better concurrency

## 📁 Project Structure

```
papernest-backend/
├── app/
│   ├── api/           # API route handlers
│   ├── core/          # Core utilities (auth, security, RAG)
│   ├── db/            # Database configuration
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   └── main.py        # FastAPI application
├── streamlit_app.py   # Frontend application
├── Dockerfile         # Container configuration
├── render.yaml        # Render Blueprint
├── requirements.txt   # Python dependencies
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for blazing-fast LLM inference
- [Render](https://render.com) for free hosting
- [Streamlit](https://streamlit.io) for rapid UI development
- [FastAPI](https://fastapi.tiangolo.com) for modern API framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for researchers and students**
