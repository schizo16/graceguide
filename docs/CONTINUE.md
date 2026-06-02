# Hướng dẫn tiếp tục phát triển GraceGuide

> File này dành cho bạn — solo dev — khi quay lại dự án sau 1 tuần, 1 tháng, hoặc lâu hơn.
> Mục tiêu: đọc xong là biết ngay đang làm gì, đang ở đâu, làm tiếp như thế nào.

---

## 1. TỔNG QUAN TRẠNG THÁI DỰ ÁN

### ✅ Đã làm được (MVP "Ember" — v0.1)

| Tính năng | Trạng thái |
|---|---|
| Tauri 2.0 overlay window (always-on-top, transparent, click-through) | ✅ Hoàn thành |
| Python sidecar (FastAPI, localhost:3721) | ✅ Hoàn thành |
| Global hotkey Ctrl+Alt+G (toggle overlay) | ✅ Hoàn thành |
| Game detection (phát hiện eldenring.exe qua psutil) | ✅ Hoàn thành |
| Xbox controller support (XInput, LB+RB+Start chord) | ✅ Hoàn thành |
| Chat UI (React + TailwindCSS + TypeScript) | ✅ Hoàn thành |
| Build recommender (3 câu hỏi → gợi ý build) | ✅ Hoàn thành |
| RAG pipeline (ChromaDB + all-MiniLM-L6-v2 + Ollama) | ✅ Hoàn thành |
| Elden Ring dataset (25 bosses + 20 weapons + 20 areas) | ✅ Hoàn thành |
| Onboarding flow (first-launch build selection) | ✅ Hoàn thành |
| i18n English + Vietnamese | ✅ Hoàn thành |
| System tray + quit menu | ✅ Hoàn thành |
| Controller mode UI (5 quick action buttons) | ✅ Hoàn thành |
| Linux build (.deb, .rpm, binary) | ✅ Hoàn thành |

### ❌ Chưa làm (cần cho Phase 2)

| Tính năng | Ưu tiên |
|---|---|
| **No-spoiler mode** (3 level: none/hint/full) | 🔴 Cao |
| **Windows build & test** (NSIS installer) | 🔴 Cao |
| **Multi-game support** (Dark Souls, Bloodborne) | 🔴 Cao |
| **Progress tracking** (auto save file parsing) | 🟡 Trung bình |
| **Lore companion** (RAG mở rộng với lore data) | 🟡 Trung bình |
| Voice input (Windows Speech API) | 🟢 Thấp |
| TTS (text-to-speech) | 🟢 Thấp |
| Esports games (Valorant, LoL) | 🟢 Thấp (sau) |

### ⚠️ Rủi ro kỹ thuật cần xử lý

1. **Overlay trên Windows DirectX fullscreen** — Cần test WebView2 transparent window có hoạt động trên Elden Ring fullscreen không. Nếu không, fallback về borderless window mode.
2. **Ollama distribution** — User cần tự cài Ollama + pull model (~4-8GB). Có thể bundle model nhỏ hơn (Phi-3, ~2GB) cho lần đầu.
3. **Antivirus** — Trên Windows, Electron/Tauri app có thể bị Windows Defender chặn. Cần sign code (self-sign tạm thời).

---

## 2. CẤU TRÚC DỰ ÁN

```
graceguide/
│
├── src/                           # 🔵 FRONTEND (React + TypeScript)
│   ├── main.tsx                   # Entry point
│   ├── App.tsx                    # Root component (rẽ nhánh onboarding/chat)
│   ├── components/
│   │   ├── ChatWindow.tsx         # Khung chat chính
│   │   ├── ChatInput.tsx          # Input + quick suggestion chips
│   │   ├── ChatMessage.tsx        # Message bubble (user/AI)
│   │   ├── BuildCard.tsx          # Build card với stat bars
│   │   ├── ControllerMode.tsx     # 5 button quick action (controller)
│   │   ├── OnboardingFlow.tsx     # 3 câu hỏi onboarding
│   │   └── Settings.tsx           # (chưa implement)
│   ├── hooks/
│   │   └── useOverlay.ts          # IPC bridge + game detection polling
│   ├── i18n/
│   │   ├── index.ts               # i18next setup
│   │   ├── en.json                # ~40 UI strings
│   │   └── vi.json                # ~40 UI strings
│   ├── types/
│   │   └── index.ts               # Message, BuildStats, BuildTemplate types
│   └── styles/
│       └── index.css              # TailwindCSS + scrollbar styling
│
├── src-tauri/                     # 🔴 CORE (Rust)
│   ├── src/
│   │   ├── main.rs                # Windows subsystem entry
│   │   ├── lib.rs                 # App setup, commands, plugin registration
│   │   ├── overlay.rs             # Window management (show/hide/click-through)
│   │   ├── tray.rs                # System tray icon + menu
│   │   └── ipc.rs                 # Python sidecar lifecycle
│   ├── Cargo.toml                 # Rust dependencies
│   ├── tauri.conf.json            # Window config, bundle, plugins
│   └── icons/                     # App icons (PNG)
│
├── backend/                       # 🟢 BACKEND (Python)
│   ├── main.py                    # FastAPI server (uvicorn, port 3721)
│   ├── requirements.txt           # Python dependencies
│   ├── chat/
│   │   ├── router.py              # POST /chat endpoint
│   │   ├── service.py             # RAG + Ollama call logic
│   │   └── prompts.py             # System prompts (EN + VI)
│   ├── rag/
│   │   ├── vector_store.py        # ChromaDB wrapper (get/create collection)
│   │   ├── embeddings.py          # SentenceTransformer lazy-loader
│   │   └── retriever.py           # Query → embed → search → return chunks
│   ├── game_data/
│   │   ├── loader.py              # CSV → ChromaDB indexing
│   │   └── elden_ring/
│   │       ├── bosses.csv         # 25 bosses
│   │       ├── weapons.csv        # 20 weapons
│   │       ├── areas.csv          # 20 areas
│   │       └── builds.json        # 5 build templates
│   ├── game_detection/
│   │   └── monitor.py             # psutil process check
│   ├── controller/
│   │   └── xinput.py              # XInput via ctypes (Windows only)
│   ├── db/
│   │   ├── schema.sql             # SQLite tables
│   │   └── user_store.py          # CRUD operations
│   ├── i18n/
│   │   └── translator.py          # Language detection heuristic
│   └── onboarding/
│       └── recommender.py         # Build decision tree
│
├── scripts/
│   └── scrape_elden_ring.py       # One-time scraper
│
├── docs/
│   ├── PRD.md                     # Product Requirements Document
│   ├── CONTINUE.md                # THIS FILE
│   └── superpowers/plans/
│       └── 2026-06-02-graceguide-mvp.md  # Implementation plan
│
├── .venv/                         # Python virtual environment (gitignored)
├── node_modules/                  # JS dependencies (gitignored)
├── package.json                   # Node.js deps + scripts
├── vite.config.ts                 # Vite build config
├── tsconfig.json                  # TypeScript config
├── tailwind.config.js             # TailwindCSS config
├── postcss.config.js              # PostCSS config
└── README.md                      # GitHub README
```

### Luồng dữ liệu chính

```
User gõ câu hỏi trong overlay
  → React UI gửi lệnh invoke('chat', { message })
  → Tauri Rust command gọi HTTP POST đến Python backend (localhost:3721/chat)
  → Python chat service:
      1. Embed query (all-MiniLM-L6-v2)
      2. Search ChromaDB (cosine similarity, top 5)
      3. Build prompt (system + context + query)
      4. Gọi Ollama (llama3.1:8b)
      5. Return response text
  → Rust trả JSON về cho React frontend
  → React hiển thị response trong ChatMessage
```

---

## 3. CÁCH CHẠY

### Lần đầu tiên

```bash
# 1. Clone
git clone https://github.com/schizo16/graceguide.git
cd graceguide

# 2. Frontend
npm install

# 3. Python backend
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows
pip install -r backend/requirements.txt

# 4. Cài Ollama + pull model
# Tải từ https://ollama.com
ollama pull llama3.1:8b      # GPU: 6GB+ VRAM, ~4.5GB
# hoặc
ollama pull llama3.2:3b      # CPU: ít RAM hơn, ~2GB

# 5. Index game data vào ChromaDB
PYTHONPATH=backend .venv/bin/python -c \
  "from game_data.loader import load_items_to_chroma; load_items_to_chroma()"
```

### Chạy development

```bash
# Terminal 1: Backend
source .venv/bin/activate
python backend/main.py
# → http://127.0.0.1:3721

# Terminal 2: Frontend + Tauri
npm run tauri dev
# → Cửa sổ Tauri + Vite dev server (http://localhost:1420)
```

### Build release

```bash
npm run tauri build
# → src-tauri/target/release/bundle/
#   ├── deb/GraceGuide_0.1.0_amd64.deb
#   ├── rpm/GraceGuide-0.1.0-1.x86_64.rpm
#   └── appimage/ (nếu FUSE available)
```

### API endpoints (để test không cần UI)

```bash
# Health
curl http://127.0.0.1:3721/health

# Game detection
curl http://127.0.0.1:3721/game/current

# Controller status (Windows only)
curl http://127.0.0.1:3721/controller/status

# Build recommender
curl -X POST http://127.0.0.1:3721/onboarding/recommend \
  -H "Content-Type: application/json" \
  -d '{"playstyle":"strength","difficulty":"easy"}'

# Chat (cần Ollama đang chạy)
curl -X POST http://127.0.0.1:3721/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"How to beat Margit?","language":"en"}'
```

---

## 4. CÁCH THÊM GAME MỚI (VD: Dark Souls 3)

Đây là pattern để support game mới. Mỗi game là một module riêng.

### Bước 1: Thêm dataset

Tạo file CSV trong `backend/game_data/darksouls3/`:
```
backend/game_data/darksouls3/
├── bosses.csv        # Boss data
├── weapons.csv       # Weapon data
├── areas.csv         # Area data
├── items.csv         # Key items
├── npcs.csv          # Characters, quests
└── builds.json       # Build templates
```

Format CSV giống Elden Ring. Copy `loader.py` logic để index vào ChromaDB với collection name `darksouls3`.

### Bước 2: Thêm game detection

Sửa `backend/game_detection/monitor.py`:

```python
GAME_PROCESSES = {
    "eldenring.exe": "eldenring",
    "darksouls3.exe": "darksouls3",
    "darksouls2.exe": "darksouls2",
    # ...thêm game mới ở đây
}
```

### Bước 3: Thêm collection vào RAG

Sửa `backend/rag/retriever.py` để chọn collection dựa trên game đang chạy.

### Bước 4: Frontend

- Thêm game name vào `ChatWindow.tsx` (hardcode tạm, sau này dynamic)
- Add quick actions mới nếu cần

Template cho game mới chỉ tốn **2-3 ngày** nếu đã có data.

---

## 5. CÁCH THÊM TÍNH NĂNG MỚI

### Thêm API endpoint mới

1. Tạo router file trong `backend/` (VD: `backend/lore/router.py`)
2. Định nghĩa endpoint trong router
3. Import + include router trong `backend/main.py`

### Thêm React component mới

1. Tạo file trong `src/components/`
2. Import vào `ChatWindow.tsx` hoặc component cha phù hợp
3. Nếu cần gọi backend, dùng `invoke()` từ `@tauri-apps/api/core` hoặc gọi thẳng HTTP đến localhost:3721

### Thêm hotkey mới

Sửa `src-tauri/src/lib.rs` — thêm `.with_shortcut("Ctrl+Alt+X")` trong plugin builder. Handler có sẵn xử lý tất cả shortcuts qua `with_handler`.

### Thêm ngôn ngữ mới (VD: Japanese)

1. Copy `src/i18n/en.json` → `src/i18n/ja.json`
2. Translate các string
3. Thêm vào `src/i18n/index.ts`:
   ```typescript
   import ja from './ja.json';
   resources: { en, vi, ja }
   ```

---

## 6. KIẾN TRÚC QUAN TRỌNG CẦN NHỚ

### Tại sao Tauri + Python (không phải Electron)?

| Quyết định | Lý do |
|---|---|
| **Tauri** thay vì Electron | RAM ~20-40MB thay vì 120-200MB. Game thủ ghét app ngốn RAM. |
| **Python sidecar** thay vì Rust AI | Python có ecosystem AI tốt nhất (Ollama, ChromaDB, sentence-transformers). Rust không có. |
| **Local LLM** thay vì Cloud | Zero budget, privacy, offline. Chấp nhận quality thấp hơn GPT. |
| **ChromaDB** thay vì Pinecone | Local-first, free, không cần server. |
| **CSV dataset** thay vì scraping runtime | Dễ edit, version control, reproducible build. |
| **FastAPI** thay vì Flask | Async, type checking, tự động docs. |

### Tại sao localhost:3721 (không phải Unix socket)?

- Windows compatible
- Dễ debug (curl, browser)
- Không cần permission đặc biệt
- Port 3721 không conflict với app thông dụng

### State management

MVP dùng React local state (`useState` trong `useOverlay.ts`). Khi app lớn hơn:
- Nếu chỉ cần global state đơn giản → **Zustand** (đã có trong package.json)
- Nếu cần persistence → **localStorage** hoặc **SQLite** qua Tauri store plugin

---

## 7. WINDOWS BUILD

### Cài đặt

```bash
# Trên Windows, cần:
# 1. Rust toolchain (https://rustup.rs)
# 2. Visual Studio Build Tools (C++ workload)
# 3. WebView2 runtime (có sẵn trên Windows 10/11)
# 4. Python 3.11+
# 5. Node.js 20+
```

### Cross-compile từ Linux (chưa test)

Có thể dùng `cross` (https://github.com/cross-rs/cross) để build Windows target từ Linux, nhưng phức tạp. Khuyên dùng máy Windows thật.

### NSIS Installer

Tauri tự động tạo NSIS installer cho Windows. Config trong `tauri.conf.json`:
```json
"bundle": {
  "windows": {
    "nsis": {
      "installMode": "currentUser"
    }
  }
}
```

### Code signing

- Để tránh Windows Defender/SmartScreen, cần sign code
- Self-sign: tạm được cho dev, nhưng người dùng sẽ thấy cảnh báo
- EV Code Signing cert: ~$200-300/năm — mua khi có revenue

---

## 8. TESTING

### Backend (Python)

```bash
cd backend
PYTHONPATH=. python -m pytest tests/  # (khi có tests)
```

Hiện tại chưa có test. Nên viết test cho:
- `chat/service.py` — mock Ollama
- `rag/retriever.py` — test query → expected results
- `onboarding/recommender.py` — test decision tree

### Frontend (React)

Chưa có test framework. Nên thêm:
- Vitest cho unit test component
- Playwright cho E2E (có sẵn tool)

### Rust

```bash
cd src-tauri
cargo test
```

---

## 9. COMMON ISSUES & SOLUTIONS

| Vấn đề | Nguyên nhân | Giải pháp |
|---|---|---|
| `Ollama connection refused` | Ollama chưa chạy | `ollama serve` |
| `Model not found` | Chưa pull model | `ollama pull llama3.1:8b` |
| `ChromaDB collection empty` | Chưa index data | Chạy loader.py |
| `Overlay không hiện trên game` | Game dùng exclusive fullscreen | Chuyển game sang borderless window |
| `Hotkey không hoạt động` | Tauri plugin lỗi | Kiểm tra console log, thử Ctrl+Alt+G |
| `Python module not found` | Sai PYTHONPATH | Chạy với `PYTHONPATH=backend` |
| `Tauri build lỗi` | Thiếu system dep | Cài `libwebkit2gtk-4.1-dev` (Linux) |
| `Controller không detect` | Không phải Windows | XInput chỉ hoạt động trên Windows |

---

## 10. NEXT STEPS (NGAY KHI QUAY LẠI)

1. **Kiểm tra repo còn chạy không:**
   ```bash
   git status
   git log --oneline -5
   ```

2. **Backend còn chạy không:**
   ```bash
   source .venv/bin/activate
   python backend/main.py &
   curl http://127.0.0.1:3721/health
   ```

3. **Ollama còn model không:**
   ```bash
   ollama list
   ```

4. **Frontend còn build không:**
   ```bash
   npx tsc --noEmit
   ```

5. **Test chat end-to-end:**
   ```bash
   curl -X POST http://127.0.0.1:3721/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"test","language":"en"}'
   ```

6. **Chọn tính năng tiếp theo từ danh sách Phase 2 ở trên.**

---

## 11. LIÊN HỆ & TÀI LIỆU

- **GitHub:** https://github.com/schizo16/graceguide
- **PRD:** `docs/PRD.md`
- **Implementation Plan:** `docs/superpowers/plans/2026-06-02-graceguide-mvp.md`
- **Tauri 2.0 Docs:** https://v2.tauri.app
- **Ollama Docs:** https://github.com/ollama/ollama
- **ChromaDB Docs:** https://docs.trychroma.com

---

*File này được viết ngày 2026-06-02, sau khi hoàn thành MVP 30 ngày.*
*Nếu đã lâu bạn chưa động vào dự án, hãy đọc từ đầu đến cuối trước khi code.*
