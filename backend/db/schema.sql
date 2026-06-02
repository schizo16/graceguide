-- GraceGuide User Data Schema (SQLite)

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    game TEXT NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at DATETIME,
    playtime_seconds INTEGER DEFAULT 0,
    build_snapshot TEXT
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    language TEXT,
    spoiler_level TEXT,
    tokens_used INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    game TEXT NOT NULL,
    current_area TEXT,
    last_boss_defeated TEXT,
    level INTEGER,
    runes_held INTEGER,
    defeated_bosses TEXT DEFAULT '[]',
    discovered_areas TEXT DEFAULT '[]',
    collected_items TEXT DEFAULT '[]',
    completed_quests TEXT DEFAULT '[]',
    notes TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
