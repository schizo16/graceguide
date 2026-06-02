# GraceGuide — PRD (Product Requirements Document)

> **Trạng thái:** Draft v1.0
> **Ngày:** 2026-06-02
> **Tác giả:** Solo dev
> **Repository:** `graceguide/graceguide`

---

## 1. TỔNG QUAN

### 1.1 Vision

Một AI game companion sống trong game của bạn — không cần alt-tab, không cheat, không popup quảng cáo. Chỉ đơn giản là có một người bạn cực kỳ hiểu game đó đi cùng bạn trong suốt hành trình.

### 1.2 Mission

Xây dựng desktop overlay ứng dụng AI local-first giúp game thủ:
- Tra build, item, boss ngay trong lúc chơi (không alt-tab)
- Nhận hint vừa đủ, không spoil
- Hiểu lore game mà không cần đọc wiki 3 tiếng
- Track progress và tối ưu trải nghiệm chơi

### 1.3 Target Audience (Primary)

- **Game thủ FromSoftware:** Elden Ring, Dark Souls 1/2/3, Bloodborne
- **Platform:** Windows 10/11
- **Input:** Xbox controller (primary), Keyboard + Mouse (secondary)
- **Demographic:** 18-35 tuổi, chơi game 5-20h/tuần, biết tiếng Anh hoặc Việt
- **Pain point:** Mệt mỏi vì phải alt-tab tra wiki giữa trận đánh boss, không biết build nào phù hợp, lore quá khó hiểu

### 1.4 Product Principles

1. **Local-first, privacy-first** — mọi thứ chạy trên máy người dùng, không gửi data đi đâu
2. **Zero interference với game** — không inject, không read memory, không hook DirectX
3. **Controller-native** — 90% Souls player dùng tay cầm, UX phải flow trên controller
4. **No over-engineering** — mỗi dòng code phải giải quyết một vấn đề thật sự
5. **Game-specific** — không làm general assistant, mỗi game được support là một dataset riêng

---

## 2. MVP — v0.1 "Ember" (30 ngày)

### 2.1 Scope

| Tính năng | Priority | Ghi chú |
|---|---|---|
| Overlay window (always-on-top, transparent) | P0 | Tauri 2.0 WebView2 |
| Game detection (process name) | P0 | psutil → phát hiện eldenring.exe |
| AI Chat (RAG + Local LLM) | P0 | Hỏi build, item, boss |
| Controller chord toggle (LB+RB+Start) | P0 | Quick action buttons |
| Build Recommender (3 câu hỏi onboarding) | P1 | Flow chọn playstyle |
| i18n EN + VI | P1 | ~50 UI strings |
| Elden Ring dataset (~15K items) | P0 | Scrape + index ChromaDB |
| Keyboard hotkey (Ctrl+Alt+G) | P0 | Fallback cho người dùng bàn phím |

### 2.2 Non-Goals (cố tình không làm)

- Multi-game support (chỉ Elden Ring)
- Progress tracking tự động
- No-spoiler mode nâng cao (chỉ hardcode hint level basic)
- Voice input / TTS
- Cloud sync
- Screen capture / CV
- Esports games

### 2.3 Elden Ring Dataset

| Entity | Số lượng | Nguồn |
|---|---|---|
| Weapons | ~1,500 | FextraLife, Wikidot |
| Armor | ~700 | FextraLife, Wikidot |
| Talismans | ~100 | FextraLife, Wikidot |
| Spells / Incantations | ~200 | FextraLife, Wikidot |
| Bosses | ~200 | FextraLife, Wikidot |
| Areas / Locations | ~100 | FextraLife, Wikidot |
| NPCs | ~80 | FextraLife, Wikidot |
| Build templates | 50 | Pre-built by dev |

### 2.4 User Data Storage (Local SQLite)

- `settings` — language, spoiler level, overlay opacity, hotkey config
- `sessions` — mỗi phiên chơi game
- `chat_messages` — lịch sử chat (để context window)
- `progress` — current area, boss đã đánh, build hiện tại

### 2.5 AI Stack

| Component | Công nghệ | Lý do |
|---|---|---|
| LLM | Llama 3.1 8B Q4_K_M (GPU) / 3.2 3B Q4 (CPU) | Local, multi-language, free |
| Embedding | all-MiniLM-L6-v2 (384 dim) | 100MB, CPU, đủ tốt |
| Vector DB | ChromaDB | Local, zero setup |
| Reranker | ms-marco-MiniLM-L-6-v2 | Tăng accuracy ~15% |
| LLM Runner | Ollama | Standard, REST API, auto hardware detection |

---

## 3. TECH STACK

### 3.1 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   WINDOWS MÁY NGƯỜI DÙNG                    │
│                                                             │
│  ┌──────────────────┐   IPC (stdio JSON-RPC)  ┌──────────┐ │
│  │ Tauri 2.0 (Rust) │ ◄────────────────────► │ Python   │ │
│  │  ├─ Overlay win  │     localhost:3721       │ Sidecar   │ │
│  │  │  (WebView2)   │                          │ ├─FastAPI │ │
│  │  ├─ React UI     │                          │ ├─Ollama  │ │
│  │  ├─ Hotkey mgmt  │                          │ ├─ChromaDB│ │
│  │  ├─ Controller   │                          │ ├─SQLite  │ │
│  │  └─ Game detect  │                          │ └─Dataset │ │
│  └──────────────────┘                          └──────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Frontend

| Layer | Công nghệ |
|---|---|
| Framework | Tauri 2.0 |
| UI | React 18 + TypeScript + Vite |
| Styling | TailwindCSS (custom dark theme) |
| i18n | i18next |
| State | Zustand (nhẹ, đơn giản) |

### 3.3 Backend

| Layer | Công nghệ |
|---|---|
| Language | Python 3.11+ |
| API Server | FastAPI (port 3721, localhost only) |
| LLM Client | Ollama Python library |
| Vector DB | ChromaDB |
| Embedding | sentence-transformers (all-MiniLM-L6-v2) |
| Reranker | sentence-transformers (cross-encoder) |
| User DB | SQLite (sqlite3) |
| Game Detection | psutil |
| Controller Detection | XInput (via ctypes) |

### 3.4 Overlay

| Property | Value |
|---|---|
| always-on-top | true |
| transparent | true |
| decorations | false |
| skip-taskbar | true |
| default width | 420px |
| default position | bottom-right + 20px margin |
| states | HIDDEN (click-through), SHOWN (focus), PEEK (20% opacity) |

### 3.5 Controller Support

| Mechanism | Detail |
|---|---|
| Detection | XInputGetState poll every 200ms |
| Toggle | LB + RB + Start (>500ms) |
| Quick Actions | D-pad navigation + A to select |
| Mini mode | Width 200px, larger font, hide keyboard input |
| Fallback | Nếu không detect controller → keyboard mode |

---

## 4. UX & UI

### 4.1 Overlay Layout

```
┌─────────────────────────────────────────────┐
│ [≡] GraceGuide          [⚙] [EN▼] [－][✕]  │ ← Header (auto-hide)
├─────────────────────────────────────────────┤
│ 🎮 Detected: Elden Ring                     │ ← Game chip
├─────────────────────────────────────────────┤
│ 💬 User message                             │
│ ◂ AI response with build cards              │
│ 📦 BUILD CARD (collapsible)                 │
├─────────────────────────────────────────────┤
│ [Type a message...]                [Send]   │ ← Chat input
│                                             │
│ "Best early weapons"  "How to beat..."     │ ← Quick suggestions
└─────────────────────────────────────────────┘
```

### 4.2 Controller Mode

```
┌────────────────────┐
│ 🎮 Controller Mode  │
│                     │
│ [🔄] Hint me        │ ← Large buttons
│ [🗺️] This area?     │    D-pad navigate
│ [⚔️] My build       │    A = select
│ [📖] Lore check     │
│ [🆕] What now?      │
│                     │
│ ◂ ...AI response... │
└────────────────────┘
```

### 4.3 Hotkeys

| Hotkey | Action | Mode |
|---|---|---|
| Ctrl+Alt+G | Toggle overlay | Keyboard |
| Esc | Hide overlay | Both |
| Enter | Send message | Keyboard |
| Ctrl+Enter | New line | Keyboard |
| LB+RB+Start (>500ms) | Toggle overlay | Controller |
| D-pad Up/Down/Left/Right | Navigate quick actions | Controller |
| A | Select quick action | Controller |

### 4.4 States

- **HIDDEN:** 0 opacity, click-through, game nhận click bình thường
- **SHOWN:** Full opacity, focusable, có thể chat
- **PEEK:** 20% opacity, hover để SHOWN, auto-hide sau 5s
- **NOTIFICATION:** 60% opacity top-right, thông báo ngắn (8s)

### 4.5 Build Recommender Flow

```
First Launch ──► "Bạn mới chơi Elden Ring?"
                    │
                    ├── Mới → 3 câu hỏi:
                    │   1. Lối đánh: Mạnh/Nhanh/Phép/Thiêng/Máu/Không biết
                    │   2. Độ khó: Dễ/Cân bằng/Hardcore
                    │   3. Vũ khí: Kiếm lớn/Nhỏ/Búa/Thương/Cung/Không biết
                    │   → Gợi ý build + stat priority
                    │
                    └── Veteran → Chọn thẳng build type
                         [STR] [DEX] [INT] [FAI] [ARC] [Custom]
```

---

## 5. ROADMAP

### Phase 1: MVP "Ember" (30 ngày)

| Tuần | Deliverable |
|---|---|
| W1 | Tauri skeleton + overlay window + Python sidecar IPC + controller chord |
| W2 | Scrape dataset + ChromaDB indexing + Ollama integration |
| W3 | Chat UI (React) + streaming + build card + game detection |
| W4 | i18n EN+VI + NSIS installer + GitHub release + Reddit launch |

### Phase 2: Growth "Souls" (30-90 ngày)

- Dark Souls 1/2/3 + Bloodborne dataset
- No-spoiler mode đầy đủ (3 level)
- Progress tracking (manual + auto save parser)
- Lore companion (RAG mở rộng)
- Voice input (Windows Speech API)
- Discord server + community feedback

### Phase 3: Scale "Lord" (90-180 ngày)

- Valorant / League of Legends (esports cautious)
- Premium subscription ($4.99/tháng)
- Cloud LLM option (GPT-4o mini cho premium user)
- TTS + voice chat
- Radial menu controller
- Plugin SDK (cộng đồng tự thêm game)

---

## 6. MONETIZATION

| Giai đoạn | Model | Price |
|---|---|---|
| 0-6 tháng | Free (build user base) | $0 |
| 6-12 tháng | Freemium: Free unlimited messages + 1 game | $0 |
| | Premium: multi-game, cloud LLM, progress auto, voice | $4.99/tháng |
| 12+ tháng | Premium Guides (per game) | $2.99 |
| | Marketplace (30% cut) | TBD |
| | API for streamers | $9.99/tháng |
| | GraceGuide Pro | $9.99/tháng |

---

## 7. METRICS & SUCCESS CRITERIA

### MVP Success (30 ngày)

- [ ] 100 users active (Reddit launch + GitHub organic)
- [ ] 50 GitHub stars
- [ ] Discord 50 members
- [ ] Overlay ổn định, không crash trên máy dev
- [ ] AI trả lời đúng >70% câu hỏi về Elden Ring (manual test)

### Phase 2 (90 ngày)

- [ ] 500-1000 users active
- [ ] 4.0+ rating trên Reddit/Discord feedback
- [ ] < 10% user churn trong tháng đầu
- [ ] Support ít nhất 3 games

### Phase 3 (180 ngày)

- [ ] Go/No-go decision dựa trên user growth
- [ ] Nếu < 200 users → pivot hoặc stop
- [ ] Nếu 500-2000 → premium monetization
- [ ] Nếu 2000+ → full-time

---

## 8. RISK & MITIGATION

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Không ai tải app | Medium | Critical | Marketing từ ngày 1 (Reddit, GitHub) |
| LLM chất lượng kém | High | High | RAG cẩn thận + reranker + prompt engineering |
| Overlay không hiện trên game | Medium | High | Fallback always-on-top + test với nhiều game mode |
| Anti-virus false positive | Low | Medium | Tauri native + sign code + open source |
| Tauri 2.0 bug | Medium | Medium | Monitoring Tauri releases + có plan B Electron |
| User churn vì local LLM chậm | Medium | Medium | Auto-detect hardware, suggest phù hợp |
| Overwolf ra mắt sản phẩm tương tự | Medium | High | Speed execution + community lock-in |

---

## 9. OPEN QUESTIONS (CHO MVP)

- [ ] Cần test overlay trên Elden Ring thật (fullscreen borderless vs exclusive)
- [ ] Cần test controller XInput trên Windows 10 vs 11
- [ ] Cần kiểm tra Ollama installation flow có mượt không
- [ ] Cần quyết định: bundle model với installer hay user tự pull?
- [ ] Cần kiểm tra legal: scraping wiki data có vấn đề gì không?

---

## 10. APPENDIX

### A. Elden Ring Dataset Sources

- https://eldenring.wiki.fextralife.com
- https://eldenring.wikidot.com
- License: Fan data, fair use

### B. Competitor Reference

- **AIgator** (GitHub) — general AI overlay, không game-specific
- **Souma** (CalHacks) — LoL coach, CV-based, không maintain
- **dota2-coach** (GitHub) — Dota overlay, rất mới
- **Overwolf** — platform, không phải AI companion

### C. Glossary

| Term | Definition |
|---|---|
| Overlay | Cửa sổ luôn nằm trên game, không ảnh hưởng game |
| Click-through | Mouse event xuyên qua overlay xuống game |
| Chord | Tổ hợp phím giữ đồng thời (LB+RB+Start) |
| RAG | Retrieval-Augmented Generation — search knowledge base trước khi generate |
| Sidecar | Process con chạy cùng app chính, giao tiếp qua IPC |
| Q4_K_M | Quantization level 4-bit, cân bằng quality vs speed |
