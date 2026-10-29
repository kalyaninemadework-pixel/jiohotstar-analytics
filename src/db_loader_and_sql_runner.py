"""
Disney+ Hotstar Database Loader & SQL Execution Engine
Loads generated CSV datasets into SQLite, applies the star schema,
and validates all 15 business queries.

Author: Kalyani Gajanan Nemade (Independent Analytics Project)
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "data", "hotstar_analytics.db")
SQL_DIR = os.path.join(BASE_DIR, "sql")

print("Initializing SQLite Database Engine...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Load schema
schema_path = os.path.join(SQL_DIR, "01_schema.sql")
with open(schema_path, "r", encoding="utf-8") as f:
    schema_sql = f.read()

cursor.executescript(schema_sql)
print("Schema tables and indexes created successfully.")

# 2. Ingest CSVs
print("Ingesting datasets into SQLite tables...")

dim_content = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_content.csv"))
dim_users = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_users.csv"))
dim_date = pd.read_csv(os.path.join(PROCESSED_DIR, "dim_date.csv"))
fact_streams = pd.read_csv(os.path.join(PROCESSED_DIR, "fact_streams.csv"))

dim_content.to_sql("dim_content", conn, if_exists="append", index=False)
dim_users.to_sql("dim_users", conn, if_exists="append", index=False)
dim_date.to_sql("dim_date", conn, if_exists="append", index=False)
fact_streams.to_sql("fact_streams", conn, if_exists="append", index=False)

conn.commit()
print("Data ingestion complete:")
print(f" - dim_content: {len(dim_content)} rows")
print(f" - dim_users: {len(dim_users)} rows")
print(f" - dim_date: {len(dim_date)} rows")
print(f" - fact_streams: {len(fact_streams)} rows")

# 3. Test & Execute Business Queries
print("\n--- Executing Sample SQL Business Analytics Queries ---")

# Test Query 1: Genre efficiency
q1 = """
WITH genre_summary AS (
    SELECT 
        c.primary_genre,
        COUNT(DISTINCT c.content_id) AS total_titles,
        COUNT(s.stream_id) AS total_streams,
        ROUND(SUM(s.watch_duration_minutes) / 60.0, 2) AS total_watch_hours,
        ROUND(AVG(s.completion_percentage), 2) AS avg_completion_rate
    FROM dim_content c
    LEFT JOIN fact_streams s ON c.content_id = s.content_id
    GROUP BY c.primary_genre
),
catalog_totals AS (
    SELECT 
        SUM(total_titles) AS grand_total_titles,
        SUM(total_watch_hours) AS grand_total_watch_hours
    FROM genre_summary
)
SELECT 
    g.primary_genre,
    g.total_titles,
    ROUND((g.total_titles * 100.0 / t.grand_total_titles), 2) AS pct_catalog,
    g.total_streams,
    g.total_watch_hours,
    ROUND((g.total_watch_hours * 100.0 / t.grand_total_watch_hours), 2) AS pct_hours,
    ROUND((g.total_watch_hours * 100.0 / t.grand_total_watch_hours) / (g.total_titles * 100.0 / t.grand_total_titles), 2) AS efficiency_ratio,
    g.avg_completion_rate
FROM genre_summary g
CROSS JOIN catalog_totals t
ORDER BY g.total_watch_hours DESC;
"""
res_q1 = pd.read_sql_query(q1, conn)
print("\n[Query 1: Genre Efficiency Leaderboard]")
print(res_q1.to_string(index=False))

# Test Query 6: Content Performance Scoring
q6 = """
WITH raw_content_stats AS (
    SELECT 
        c.content_id,
        c.title,
        c.type,
        c.original_language,
        c.primary_genre,
        c.licensing_tier,
        COUNT(s.stream_id) AS total_streams,
        COALESCE(SUM(s.watch_duration_minutes) / 60.0, 0) AS total_watch_hours,
        COALESCE(AVG(s.completion_percentage), 0) AS avg_completion_pct,
        COALESCE(AVG(s.user_rating), 3.0) AS avg_rating,
        COALESCE(SUM(s.is_repeat_stream) * 100.0 / NULLIF(COUNT(s.stream_id), 0), 0) AS rewatch_rate
    FROM dim_content c
    LEFT JOIN fact_streams s ON c.content_id = s.content_id
    GROUP BY c.content_id, c.title, c.type, c.original_language, c.primary_genre, c.licensing_tier
),
min_max_bounds AS (
    SELECT 
        MIN(total_streams) AS min_streams,
        MAX(total_streams) AS max_streams,
        MIN(total_watch_hours) AS min_hours,
        MAX(total_watch_hours) AS max_hours
    FROM raw_content_stats
),
normalized_scores AS (
    SELECT 
        r.*,
        ((r.total_streams - b.min_streams) * 100.0 / NULLIF(b.max_streams - b.min_streams, 0)) AS norm_streams,
        ((r.total_watch_hours - b.min_hours) * 100.0 / NULLIF(b.max_hours - b.min_hours, 0)) AS norm_hours,
        r.avg_completion_pct AS norm_completion,
        (r.avg_rating / 5.0 * 100.0) AS norm_rating,
        r.rewatch_rate AS norm_rewatch
    FROM raw_content_stats r
    CROSS JOIN min_max_bounds b
)
SELECT 
    content_id,
    title,
    original_language,
    primary_genre,
    total_streams,
    ROUND(total_watch_hours, 1) AS total_hours,
    ROUND(avg_completion_pct, 1) AS comp_pct,
    ROUND(avg_rating, 2) AS rating,
    ROUND(
        (0.30 * norm_streams) + 
        (0.25 * norm_completion) + 
        (0.20 * norm_hours) + 
        (0.15 * norm_rating) + 
        (0.10 * norm_rewatch), 2
    ) AS cps_score
FROM normalized_scores
ORDER BY cps_score DESC
LIMIT 10;
"""
res_q6 = pd.read_sql_query(q6, conn)
print("\n[Query 6: Top 10 Content Performance Score (CPS)]")
print(res_q6.to_string(index=False))

# Test Query 13: Churn Risk by Acquisition Channel
q13 = """
SELECT 
    acquisition_channel,
    subscription_tier,
    COUNT(user_id) AS total_users,
    SUM(is_churned) AS churned_users,
    ROUND(SUM(is_churned) * 100.0 / COUNT(user_id), 2) AS churn_rate_pct
FROM dim_users
GROUP BY acquisition_channel, subscription_tier
ORDER BY acquisition_channel, churn_rate_pct DESC;
"""
res_q13 = pd.read_sql_query(q13, conn)
print("\n[Query 13: Churn Rate by Acquisition Channel & Tier]")
print(res_q13.to_string(index=False))

conn.close()
print("\nSQLite Database hotstar_analytics.db successfully validated and indexed!")
