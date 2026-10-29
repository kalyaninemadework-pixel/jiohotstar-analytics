-- ==============================================================================
-- DISNEY+ HOTSTAR STREAMING ANALYTICS PLATFORM
-- Relational Star Schema DDL (PostgreSQL & SQLite Compatible)
-- Author: Kalyani Gajanan Nemade (Independent Analytics Portfolio Project)
-- ==============================================================================

-- 1. DIM_CONTENT
DROP TABLE IF EXISTS dim_content;
CREATE TABLE dim_content (
    content_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'Movie' or 'TV Show'
    primary_genre VARCHAR(50) NOT NULL,
    secondary_genre VARCHAR(50),
    original_language VARCHAR(50) NOT NULL,
    runtime_minutes INTEGER NOT NULL,
    total_episodes INTEGER NOT NULL DEFAULT 1,
    release_year INTEGER NOT NULL,
    age_rating VARCHAR(20) NOT NULL,
    licensing_tier VARCHAR(50) NOT NULL,
    content_cost_usd NUMERIC(12, 2) NOT NULL,
    director VARCHAR(100),
    lead_actor VARCHAR(100)
);

-- 2. DIM_USERS
DROP TABLE IF EXISTS dim_users;
CREATE TABLE dim_users (
    user_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE NOT NULL,
    subscription_tier VARCHAR(50) NOT NULL, -- 'Free (AVOD)', 'Super', 'Premium'
    region VARCHAR(50) NOT NULL,
    primary_language VARCHAR(50) NOT NULL,
    acquisition_channel VARCHAR(100) NOT NULL,
    age_group VARCHAR(20) NOT NULL,
    is_churned INTEGER NOT NULL DEFAULT 0, -- 1 for churned, 0 for active
    churn_date DATE
);

-- 3. DIM_DATE
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY, -- Format YYYYMMDD
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend INTEGER NOT NULL DEFAULT 0,
    is_ipl_season INTEGER NOT NULL DEFAULT 0,
    is_festive_season INTEGER NOT NULL DEFAULT 0
);

-- 4. FACT_STREAMS
DROP TABLE IF EXISTS fact_streams;
CREATE TABLE fact_streams (
    stream_id VARCHAR(30) PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    content_id VARCHAR(20) NOT NULL,
    stream_date DATE NOT NULL,
    date_id INTEGER NOT NULL,
    watch_duration_minutes NUMERIC(10, 2) NOT NULL,
    completion_percentage NUMERIC(5, 2) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    network_type VARCHAR(50) NOT NULL,
    playback_quality VARCHAR(50) NOT NULL,
    user_rating NUMERIC(3, 1),
    is_repeat_stream INTEGER NOT NULL DEFAULT 0,
    is_first_stream INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    FOREIGN KEY (content_id) REFERENCES dim_content(content_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Performance Indexes for Analytical Query Acceleration
CREATE INDEX idx_streams_user_id ON fact_streams(user_id);
CREATE INDEX idx_streams_content_id ON fact_streams(content_id);
CREATE INDEX idx_streams_date_id ON fact_streams(date_id);
CREATE INDEX idx_streams_stream_date ON fact_streams(stream_date);
CREATE INDEX idx_content_genre ON dim_content(primary_genre);
CREATE INDEX idx_content_lang ON dim_content(original_language);
CREATE INDEX idx_users_tier ON dim_users(subscription_tier);
