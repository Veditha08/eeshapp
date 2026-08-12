# EeshApp 🍲

**EeshApp** is a personalized hostel mess-food companion designed to help Eesha make quick, context-aware decisions about what to eat for every meal. It combines recurring weekly mess menus, personal food preferences, and past meal feedback with an LLM (Qwen/Qwen3.5-4B via Tinker) to deliver friendly, practical meal recommendations.

---

## Architecture & Tech Stack

```text
                  MESS MENU
                     ↓
               Food database
                     ↓
         ┌───────────┴───────────┐
         ↓                       ↓
     Friend's preferences      Eating history
         ↓                       ↓
         └───────────┬───────────┘
                     ↓
              Open-source LLM
              (Qwen 3.5-4B)
                     ↓
           Contextual decision
                     ↓
       ┌─────────────┼──────────────┐
       ↓             ↓              ↓
     Eat this      Skip this       Buy this
       ↓             ↓              ↓
     feedback      feedback       feedback
       └─────────────┴──────────────┘
                     ↓
               Memory updated
```

- **Frontend**: React 19, Vite, Vanilla CSS
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Database**: SQLite (`backend/eeshapp.db`)
- **AI Engine**: `Qwen/Qwen3.5-4B` via Tinker (`tinker`, `tinker_cookbook`)

---

## Food Decision & Personalization Rules

- **Ground Truth Menu**: The weekly mess menu stored in the database is the absolute source of truth. The AI never invents foods or assumes unlisted items are present.
- **Preferences**:
  - *Likes (Strong)*: Dal, Rice, Dahi
  - *Likes (Mild)*: Pickle
  - *Dislikes (Strong)*: Gatte ki sabji
- **Gentle Encouragement**: Eesha doesn't enjoy most other sabjis as much, but recommendations encourage trying a small portion rather than automatically skipping them.
- **Cafeteria Fallback**: If meal history shows repeated skips or meal avoidance, cafeteria dahi with rice is suggested as a fallback option (since mess meals do not automatically have curd/dahi).

---

## Project Structure

```text
eeshapp/
├── backend/
│   ├── database.py       # SQLite connection and query helper functions
│   ├── eeshapp.db        # SQLite database (menu, preferences, history)
│   ├── main.py           # FastAPI application and endpoints
│   ├── seed_menu.py      # Seed script for the recurring weekly mess menu
│   ├── clean_history.py  # Utility script for cleaning test history
│   ├── fix_menu.py       # Utility script for menu corrections
│   ├── test_ai.py        # Standalone test script for Tinker AI inference
│   ├── test_feedback.py  # Interactive CLI test for meal feedback
│   ├── test_menu.py      # Menu query test script
│   └── test_hf.py        # Hugging Face test script
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main dashboard component
│   │   ├── App.css       # Application styling
│   │   └── main.jsx      # Vite entry point
│   ├── package.json      # Frontend dependencies & scripts
│   └── vite.config.js    # Vite configuration
├── requirements.txt      # Python backend dependencies
└── README.md             # Project documentation
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Tinker API access configured for `Qwen/Qwen3.5-4B`

### Backend Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI backend:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```
   The backend API will be available at `http://127.0.0.1:8000`.
   Interactive OpenAPI docs are at `http://127.0.0.1:8000/docs`.

### Frontend Setup

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The dashboard will be available at `http://localhost:5173`.

3. Build for production:
   ```bash
   npm run build
   ```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check endpoint |
| `GET` | `/menu` | Returns the current meal and menu based on time of day |
| `GET` | `/preferences` | Returns Eesha's stored food preferences |
| `GET` | `/history` | Returns the last 10 meal history records |
| `POST` | `/recommend` | Generates a context-aware AI recommendation using Tinker |
| `POST` | `/feedback` | Saves user feedback (`ate`, `skipped`, `ordered_outside`) |

---

## License

MIT License. See [LICENSE](LICENSE) for details.