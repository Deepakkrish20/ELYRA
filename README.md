# InsightAI - Content Intelligence Platform

InsightAI is an AI-powered Content Intelligence Platform designed to analyze textual content using Natural Language Processing (NLP) and Machine Learning techniques. The platform aims to provide actionable insights for various media types, including spam filtering, sentiment and moral analysis of poetry, and deep content breakdown for movies.

---

## Tech Stack

### Frontend
- **React.js** - Single page application library
- **Vite** - Modern front-end build tool
- **Tailwind CSS** - Utility-first styling framework
- **React Router DOM** - Client-side routing
- **Axios** - Promise-based HTTP client for the browser and Node.js
- **ESLint & Prettier** - Code quality and formatting tools

### Backend
- **Python 3.12+**
- **FastAPI** - High-performance modern web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server implementation
- **Pydantic** - Data validation and settings management using Python type annotations
- **Pytest** - Robust test framework

### DevOps
- **Git** - Version control
- **Docker & Docker Compose** - Containerization and orchestration
- **GitHub Actions** - Continuous Integration (CI) workflows

---

## Planned Features

1. **Spam Detection**
   - Classify text messages, emails, and comments as spam or ham.
   - Real-time prediction endpoint.
2. **Poem Emotion and Moral Analysis**
   - Evaluate poetry lines for emotional tones (joy, sadness, anger, etc.).
   - Extract underlying moral suggestions and themes.
3. **Movie Content Analysis**
   - Analyze movie synopses or scripts for genre classification.
   - Highlight key plot themes and content advisories.

---

## Project Structure

```text
insight-ai/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow
├── backend/
│   ├── app/
│   │   ├── api/               # Router endpoints (spam, poem, movie)
│   │   ├── core/              # Config, security, constants
│   │   ├── models/            # Database models (future)
│   │   ├── schemas/           # Pydantic validation schemas
│   │   ├── services/          # Business logic and ML inference
│   │   ├── utils/             # Helper functions
│   │   └── main.py            # FastAPI Entry point
│   ├── tests/                 # Unit and integration tests
│   ├── .env.example           # Example backend env settings
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
├── docs/                      # Architectural docs and diagrams
├── frontend/
│   ├── src/
│   │   ├── assets/            # Static assets (images, fonts)
│   │   ├── components/        # Reusable UI components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── layouts/           # Page structures (Navbar, Footer, Sidebar)
│   │   ├── pages/             # Route-level components (Home, Analyzers)
│   │   ├── routes/            # Route configurations
│   │   ├── services/          # API services (Axios client, endpoints)
│   │   ├── utils/             # Helper functions
│   │   ├── App.jsx            # React root component
│   │   ├── index.css          # CSS styles (Tailwind imports)
│   │   └── main.jsx           # Vite application entry
│   ├── .env.example           # Example frontend env settings
│   ├── eslint.config.js       # ESLint configurations
│   ├── tailwind.config.js     # Tailwind CSS settings
│   └── vite.config.js         # Vite configuration
├── docker-compose.yml         # Local Docker Orchestration
├── LICENSE                    # License information
└── README.md                  # Main project guide
```

---

## Local Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Copy the example environment variables:
   ```bash
   cp .env.example .env
   ```
3. Install the node dependencies:
   ```bash
   npm install
   ```
4. Run the frontend in development mode:
   ```bash
   npm run dev
   ```
   The application will be accessible at `http://localhost:5173`.

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Copy the example environment variables:
   ```bash
   cp .env.example .env
   ```
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API documentation will be available at `http://localhost:8000/docs`.

---

## Docker Instructions

To spin up the entire application stack including the React frontend and FastAPI backend inside Docker:

1. Ensure Docker and Docker Compose are installed on your machine.
2. From the root directory (`insight-ai`), run:
   ```bash
   docker compose up --build
   ```
3. Once running, visit:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`

---

## Future Enhancements
- Integration of state-of-the-art NLP models (Hugging Face Transformers / LangChain).
- User authentication and persistent query history.
- Real-time visualization dashboards for bulk uploads.
- Full production CI/CD deployments to cloud providers.
