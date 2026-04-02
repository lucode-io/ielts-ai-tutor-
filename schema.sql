-- ============================================================
-- IELTS Master Platform - Supabase Database Schema
-- Run this in your Supabase SQL Editor
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── USERS TABLE ──
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_seen TIMESTAMPTZ DEFAULT NOW(),
    baseline_band NUMERIC(3,1) DEFAULT NULL,
    target_band NUMERIC(3,1) DEFAULT 7.0,
    native_language TEXT DEFAULT 'English',
    response_language TEXT DEFAULT 'English',
    tutor_name TEXT DEFAULT 'Alex',
    accent_color TEXT DEFAULT '#F0C040',
    streak_count INTEGER DEFAULT 0,
    streak_last_date DATE DEFAULT NULL,
    challenge_started_at TIMESTAMPTZ DEFAULT NULL,
    challenge_day INTEGER DEFAULT 0,
    challenge_completed BOOLEAN DEFAULT FALSE,
    subscription_status TEXT DEFAULT 'free',
    stripe_customer_id TEXT DEFAULT NULL
);

-- ── SESSIONS TABLE ──
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    mode TEXT NOT NULL,
    topic TEXT NOT NULL,
    target_band NUMERIC(3,1),
    overall_band NUMERIC(3,1),
    duration_seconds INTEGER DEFAULT 0,
    message_count INTEGER DEFAULT 0,
    session_data JSONB DEFAULT '{}'
);

-- ── BAND SCORES TABLE ──
CREATE TABLE IF NOT EXISTS band_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    skill TEXT NOT NULL, -- speaking/writing/reading/listening/overall
    band_score NUMERIC(3,1) NOT NULL,
    fluency NUMERIC(3,1),
    lexical_resource NUMERIC(3,1),
    grammatical_range NUMERIC(3,1),
    pronunciation NUMERIC(3,1),
    task_achievement NUMERIC(3,1),
    coherence NUMERIC(3,1),
    notes TEXT
);

-- ── PRACTICE MESSAGES TABLE ──
CREATE TABLE IF NOT EXISTS practice_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    role TEXT NOT NULL, -- user/assistant
    content TEXT NOT NULL,
    audio_url TEXT DEFAULT NULL
);

-- ── RECURRING ERRORS TABLE ──
CREATE TABLE IF NOT EXISTS recurring_errors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    detected_at TIMESTAMPTZ DEFAULT NOW(),
    error_type TEXT NOT NULL,
    error_category TEXT NOT NULL, -- grammar/vocabulary/structure/pronunciation
    description TEXT NOT NULL,
    example TEXT,
    frequency INTEGER DEFAULT 1,
    last_seen TIMESTAMPTZ DEFAULT NOW()
);

-- ── CHALLENGE DAYS TABLE ──
CREATE TABLE IF NOT EXISTS challenge_days (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    day_number INTEGER NOT NULL,
    completed_at TIMESTAMPTZ DEFAULT NOW(),
    task_type TEXT NOT NULL,
    band_score NUMERIC(3,1),
    notes TEXT,
    UNIQUE(user_id, day_number)
);

-- ── DIAGNOSTIC TEST TABLE ──
CREATE TABLE IF NOT EXISTS diagnostic_tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    taken_at TIMESTAMPTZ DEFAULT NOW(),
    speaking_band NUMERIC(3,1),
    writing_band NUMERIC(3,1),
    reading_band NUMERIC(3,1),
    listening_band NUMERIC(3,1),
    overall_band NUMERIC(3,1),
    raw_results JSONB DEFAULT '{}'
);

-- ── ROW LEVEL SECURITY ──
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE band_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE practice_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE recurring_errors ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenge_days ENABLE ROW LEVEL SECURITY;
ALTER TABLE diagnostic_tests ENABLE ROW LEVEL SECURITY;

-- Users can only access their own data
CREATE POLICY "Users own data" ON users FOR ALL USING (auth.uid() = id);
CREATE POLICY "Users own sessions" ON sessions FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users own scores" ON band_scores FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users own messages" ON practice_messages FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users own errors" ON recurring_errors FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users own challenge" ON challenge_days FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users own diagnostics" ON diagnostic_tests FOR ALL USING (auth.uid() = user_id);

-- ── INDEXES ──
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_band_scores_user_id ON band_scores(user_id);
CREATE INDEX idx_band_scores_recorded_at ON band_scores(recorded_at);
CREATE INDEX idx_practice_messages_session ON practice_messages(session_id);
CREATE INDEX idx_challenge_days_user ON challenge_days(user_id);
CREATE INDEX idx_recurring_errors_user ON recurring_errors(user_id);
