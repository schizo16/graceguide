# 🎮 GraceGuide — AI Game Companion

> No alt-tab. No cheat. Just a friend who knows everything about the game.

GraceGuide is an AI game companion that lives inside your game. It provides real-time coaching, build guides, lore explanations, and boss strategies — all through an in-game overlay. No alt-tabbing to a wiki. No Discord switching. Just you and your AI companion.

## ✨ Features

- **🎮 In-Game Overlay** — Always-on-top, transparent, click-through. Appears when you need it, disappears when you don't.
- **🎮 Controller Native** — LB+RB+Start to toggle. D-pad to navigate quick actions. Built for Souls players.
- **⌨️ Hotkeys** — Ctrl+Alt+G to toggle overlay. Esc to hide.
- **💬 AI Chat** — Ask about builds, bosses, items, or lore. AI responds with context from the game database.
- **📦 Build Recommender** — Answer 3 questions, get a personalized build with stat priorities and weapon recommendations.
- **🌐 Multi-language** — English + Vietnamese supported.
- **🔒 100% Local** — Everything runs on your machine. No data sent to the cloud. No internet required (after setup).
- **🧠 RAG-Powered** — Retrieval-Augmented Generation with Elden Ring knowledge base for accurate, contextual answers.

## 🚀 Quick Start

### Prerequisites

1. **Ollama** — Download from [ollama.com](https://ollama.com)
2. **Pull a model:**
   ```bash
   ollama pull llama3.1:8b
   ```
3. **Python 3.11+** with pip

### Installation

```bash
# Clone the repo
git clone https://github.com/schizo16/graceguide.git
cd graceguide

# Frontend dependencies
npm install

# Python backend
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r backend/requirements.txt

# Index game data
PYTHONPATH=backend .venv/bin/python -c "from game_data.loader import load_items_to_chroma; load_items_to_chroma()"
```

### Run

```bash
# Terminal 1: Start Python backend
.venv/bin/python backend/main.py

# Terminal 2: Start Tauri app
npm run tauri dev
```

## 🎮 Usage

| Input | Action |
|---|---|
| `Ctrl+Alt+G` | Toggle overlay on/off |
| `Esc` | Hide overlay |
| `Enter` | Send chat message |
| `Shift+Enter` | New line in chat |
| `LB+RB+Start` | Toggle overlay (controller) |
| D-pad + A | Navigate quick actions (controller) |

### Quick Prompts (Controller Mode)
- **🔄 Hint me** — Get a hint for where to go next
- **🗺️ This area?** — Learn about your current location
- **⚔️ My build** — View your current build
- **📖 Lore check** — Understand the lore around you
- **🆕 What now?** — Get direction on what to do next

## 🗺️ Roadmap

### v0.1 "Ember" (Current — 30 days)
- ✅ Tauri 2.0 overlay window
- ✅ Python sidecar (FastAPI)
- ✅ Global hotkey + game detection
- ✅ Controller chord support
- ✅ AI Chat (RAG + Local LLM)
- ✅ Build recommender
- ✅ Elden Ring dataset (25 bosses, 20 weapons, 20 areas)
- ✅ i18n EN + VI
- ⏳ Ollama LLM integration

### v0.2 "Souls" (90 days)
- Dark Souls 1/2/3 + Bloodborne support
- No-spoiler mode (3 levels)
- Progress tracking (auto-detect via save file)
- Lore companion (RAG expanded)
- Voice input (Windows Speech API)
- Discord community

### v0.3 "Lord" (180 days)
- Esports games (Valorant, League of Legends)
- Premium subscription ($4.99/month)
- Cloud LLM option (GPT-4o mini)
- TTS + voice chat
- Plugin SDK for community game support

## 🧠 Architecture

```
┌─────────────────────────────┐
│ Tauri 2.0 (Rust)            │
│  ├─ Overlay (WebView2)      │
│  ├─ React + TypeScript UI   │
│  ├─ Global hotkey           │
│  └─ System tray             │
└──────────┬──────────────────┘
           │ HTTP (localhost:3721)
┌──────────▼──────────────────┐
│ Python Sidecar (FastAPI)     │
│  ├─ Chat: RAG + Ollama       │
│  ├─ ChromaDB vector store    │
│  ├─ Game detection (psutil)  │
│  └─ Controller (XInput)      │
└─────────────────────────────┘
```

## 💻 Tech Stack

| Layer | Technology |
|---|---|
| Desktop Framework | Tauri 2.0 |
| Frontend | React 18 + TypeScript + TailwindCSS |
| Backend | Python 3.11+ / FastAPI |
| LLM | Ollama (llama3.1:8b or 3.2:3b) |
| Vector DB | ChromaDB |
| Embeddings | all-MiniLM-L6-v2 (sentence-transformers) |
| Game Detection | psutil |
| Controller | XInput (via ctypes) |
| Data | CSV → ChromaDB indexing |

## 🏗️ Project Structure

```
graceguide/
├── src/                  # React frontend
│   ├── components/       # UI components
│   ├── hooks/           # Custom hooks (useOverlay)
│   ├── i18n/            # Internationalization
│   ├── types/           # TypeScript types
│   └── styles/          # CSS/Tailwind
├── src-tauri/           # Rust backend
│   └── src/             # overlay, tray, ipc modules
├── backend/             # Python sidecar
│   ├── chat/            # Chat API + LLM service
│   ├── rag/             # RAG pipeline (embed, store, retrieve)
│   ├── game_data/       # Elden Ring dataset
│   ├── game_detection/  # Process monitoring
│   ├── controller/      # XInput wrapper
│   ├── db/              # SQLite user store
│   ├── i18n/            # Translation service
│   └── onboarding/      # Build recommender
├── scripts/             # Utility scripts
└── docs/                # Design docs
```

## 🤝 Contributing

This is a solo project, but contributions are welcome! Open an issue or PR for:
- Data corrections (Elden Ring stats, boss weaknesses)
- New game support (Dark Souls, Bloodborne)
- Bug fixes and improvements
- Translations

## 📜 License

MIT
