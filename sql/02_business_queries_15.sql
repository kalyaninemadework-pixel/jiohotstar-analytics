-- ==============================================================================
-- DISNEY+ HOTSTAR STREAMING ANALYTICS PLATFORM
-- 15 Production-Grade Business & Product Analytics SQL Queries
-- Author: Kalyani Gajanan Nemade (Independent Analytics Portfolio Project)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Genre Performance & Content Efficiency Ratio
-- Business Value: Identifies which genres generate outsized watch time relative to catalog volume.
-- ------------------------------------------------------------------------------
WITH genre_summary AS (
    SELECT 
        c.primary_genre,
        COUNT(DISTINCT c.content_id) AS total_titles,
        COUNT(s.stream_id) AS total_streams,
        ROUND(SUM(s.watch_duration_minutes) / 60.0, 2) AS total_watch_hours,
        ROUND(AVG(s.completion_percentage), 2) AS avg_completion_rate,
        ROUND(AVG(s.user_rating), 2) AS avg_user_rating
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
    ROUND((g.total_titles * 100.0 / t.grand_total_titles), 2) AS pct_catalog_share,
    g.total_streams,
    g.total_watch_hours,
    ROUND((g.total_watch_hours * 100.0 / t.grand_total_watch_hours), 2) AS pct_watch_hours_share,
    -- Efficiency Ratio > 1.0 indicates outperforming catalog allocation
    ROUND((g.total_watch_hours * 100.0 / t.grand_total_watch_hours) / (g.total_titles * 100.0 / t.grand_total_titles), 2) AS efficiency_ratio,
    g.avg_completion_rate,
    g.avg_user_rating
FROM genre_summary g
CROSS JOIN catalog_totals t
ORDER BY g.total_watch_hours DESC;


-- ------------------------------------------------------------------------------
-- QUERY 2: Top 3 Titles in Each Genre by Completion Rate (Window Function)
-- Business Value: Highlights flagship benchmark content within every vertical.
-- ------------------------------------------------------------------------------
WITH content_stats AS (
    SELECT 
        c.primary_genre,
        c.content_id,
        c.title,
        c.original_language,
        c.type,
        COUNT(s.stream_id) AS stream_count,
        ROUND(AVG(s.completion_percentage), 2) AS avg_completion_pct,
        ROUND(SUM(s.watch_duration_minutes) / 60.0, 2) AS total_watch_hours
    FROM dim_content c
    JOIN fact_streams s ON c.content_id = s.content_id
    GROUP BY c.primary_genre, c.content_id, c.title, c.original_language, c.type
    HAVING COUNT(s.stream_id) >= 15 -- Minimum volume threshold for statistical validity
),
ranked_content AS (
    SELECT 
        primary_genre,
        title,
        original_language,
        type,
        stream_count,
        avg_completion_pct,
        total_watch_hours,
        DENSE_RANK() OVER (
            PARTITION BY primary_genre 
            ORDER BY avg_completion_pct DESC, total_watch_hours DESC
        ) AS genre_rank
    FROM content_stats
)
SELECT 
    primary_genre,
    genre_rank,
    title,
    original_language,
    type,
    stream_count,
    avg_completion_pct,
    total_watch_hours
FROM ranked_content
WHERE genre_rank <= 3
ORDER BY primary_genre, genre_rank;


-- ------------------------------------------------------------------------------
-- QUERY 3: Monthly Active Streamers (MAS) & MoM Growth Dynamics
-- Business Value: Tracks platform engagement growth and seasonal peaks (e.g. IPL).
-- ------------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        d.year,
        d.month,
        d.month_name,
        COUNT(DISTINCT s.user_id) AS monthly_active_streamers,
        COUNT(s.stream_id) AS total_streams,
        ROUND(SUM(s.watch_duration_minutes) / 60.0, 2) AS total_watch_hours
    FROM fact_streams s
    JOIN dim_date d ON s.date_id = d.date_id
    GROUP BY d.year, d.month, d.month_name
)
SELECT 
    year,
    month,
    month_name,
    monthly_active_streamers,
    LAG(monthly_active_streamers, 1) OVER (ORDER BY year, month) AS prev_month_mas,
    ROUND(
        ((monthly_active_streamers - LAG(monthly_active_streamers, 1) OVER (ORDER BY year, month)) * 100.0) /
        NULLIF(LAG(monthly_active_streamers, 1) OVER (ORDER BY year, month), 0), 2
    ) AS mom_mas_growth_pct,
    total_watch_hours,
    ROUND(
        ((total_watch_hours - LAG(total_watch_hours, 1) OVER (ORDER BY year, month)) * 100.0) /
        NULLIF(LAG(total_watch_hours, 1) OVER (ORDER BY year, month), 0), 2
    ) AS mom_watch_hours_growth_pct
FROM monthly_metrics
ORDER BY year, month;


-- ------------------------------------------------------------------------------
-- QUERY 4: 90-Day User Cohort Retention Matrix
-- Business Value: Measures customer decay across monthly signup cohorts.
-- ------------------------------------------------------------------------------
WITH user_cohorts AS (
    SELECT 
        user_id,
        strftime('%Y-%m', signup_date) AS cohort_month,
        subscription_tier
    FROM dim_users
),
user_activities AS (
    SELECT 
        s.user_id,
        strftime('%Y-%m', s.stream_date) AS activity_month,
        -- Calculate month offset from signup
        (CAST(strftime('%Y', s.stream_date) AS INT) - CAST(strftime('%Y', u.signup_date) AS INT)) * 12 +
        (CAST(strftime('%m', s.stream_date) AS INT) - CAST(strftime('%m', u.signup_date) AS INT)) AS month_offset
    FROM fact_streams s
    JOIN dim_users u ON s.user_id = u.user_id
)
SELECT 
    c.cohort_month,
    COUNT(DISTINCT c.user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN a.month_offset = 0 THEN a.user_id END) AS m0_active,
    ROUND(COUNT(DISTINCT CASE WHEN a.month_offset = 0 THEN a.user_id END) * 100.0 / COUNT(DISTINCT c.user_id), 1) AS m0_retention_pct,
    COUNT(DISTINCT CASE WHEN a.month_offset = 1 THEN a.user_id END) AS m1_active,
    ROUND(COUNT(DISTINCT CASE WHEN a.month_offset = 1 THEN a.user_id END) * 100.0 / COUNT(DISTINCT c.user_id), 1) AS m1_retention_pct,
    COUNT(DISTINCT CASE WHEN a.month_offset = 2 THEN a.user_id END) AS m2_active,
    ROUND(COUNT(DISTINCT CASE WHEN a.month_offset = 2 THEN a.user_id END) * 100.0 / COUNT(DISTINCT c.user_id), 1) AS m2_retention_pct,
    COUNT(DISTINCT CASE WHEN a.month_offset = 3 THEN a.user_id END) AS m3_active,
    ROUND(COUNT(DISTINCT CASE WHEN a.month_offset = 3 THEN a.user_id END) * 100.0 / COUNT(DISTINCT c.user_id), 1) AS m3_retention_pct
FROM user_cohorts c
LEFT JOIN user_activities a ON c.user_id = a.user_id
WHERE c.cohort_month BETWEEN '2023-01' AND '2024-03'
GROUP BY c.cohort_month
ORDER BY c.cohort_month;


-- ------------------------------------------------------------------------------
-- QUERY 5: Pareto Principle (80/20 Rule) Watch Time Distribution
-- Business Value: Shows catalog concentration risk: what % of titles drive 80% of watch hours.
-- ------------------------------------------------------------------------------
WITH title_watch_hours AS (
    SELECT 
        c.content_id,
        c.title,
        c.original_language,
        c.primary_genre,
        SUM(s.watch_duration_minutes) / 60.0 AS title_hours
    FROM dim_content c
    JOIN fact_streams s ON c.content_id = s.content_id
    GROUP BY c.content_id, c.title, c.original_language, c.primary_genre
),
ranked_titles AS (
    SELECT 
        content_id,
        title,
        original_language,
        primary_genre,
        title_hours,
        ROW_NUMBER() OVER (ORDER BY title_hours DESC) AS title_rank,
        COUNT(*) OVER () AS total_titles_count,
        SUM(title_hours) OVER () AS platform_total_hours,
        SUM(title_hours) OVER (ORDER BY title_hours DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_cumulative_hours
    FROM title_watch_hours
)
SELECT 
    title_rank,
    title,
    original_language,
    primary_genre,
    ROUND(title_hours, 2) AS title_watch_hours,
    ROUND((title_rank * 100.0 / total_titles_count), 2) AS cumulative_catalog_pct,
    ROUND((running_cumulative_hours * 100.0 / platform_total_hours), 2) AS cumulative_watch_hours_pct
FROM ranked_titles
WHERE title_rank IN (1, 10, 50, 100, 250, 500, 1000, 2000, 3000)
ORDER BY title_rank;


-- ------------------------------------------------------------------------------
-- QUERY 6: Content Performance Score (CPS) Engine in SQL
-- Business Value: Transparent algorithmic scoring on 0-100 scale for catalog decisions.
-- ------------------------------------------------------------------------------
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
        -- Min-Max Normalization to 0-100
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
    type,
    original_language,
    primary_genre,
    licensing_tier,
    total_streams,
    ROUND(total_watch_hours, 1) AS total_watch_hours,
    ROUND(avg_completion_pct, 1) AS avg_completion_pct,
    ROUND(avg_rating, 2) AS avg_rating,
    ROUND(
        (0.30 * norm_streams) + 
        (0.25 * norm_completion) + 
        (0.20 * norm_hours) + 
        (0.15 * norm_rating) + 
        (0.10 * norm_rewatch), 2
    ) AS content_performance_score
FROM normalized_scores
ORDER BY content_performance_score DESC
LIMIT 20;


-- ------------------------------------------------------------------------------
-- QUERY 7: Regional Language Efficiency & Cross-Consumption
-- Business Value: Shows how regional titles expand beyond their native speaker base.
-- ------------------------------------------------------------------------------
SELECT 
    c.original_language AS content_language,
    COUNT(DISTINCT c.content_id) AS title_count,
    COUNT(s.stream_id) AS total_streams,
    ROUND(SUM(s.watch_duration_minutes) / 60.0, 2) AS total_watch_hours,
    ROUND(AVG(s.completion_percentage), 2) AS avg_completion_pct,
    -- Non-native consumption percentage
    ROUND(
        COUNT(CASE WHEN u.primary_language != c.original_language THEN 1 END) * 100.0 / 
        NULLIF(COUNT(s.stream_id), 0), 2
    ) AS cross_language_viewing_pct
FROM dim_content c
JOIN fact_streams s ON c.content_id = s.content_id
JOIN dim_users u ON s.user_id = u.user_id
GROUP BY c.original_language
ORDER BY total_watch_hours DESC;


-- ------------------------------------------------------------------------------
-- QUERY 8: First-Touch Content Acquisition Attribution
-- Business Value: Identifies the 'Gateway Titles' that attract brand new subscribers.
-- ------------------------------------------------------------------------------
WITH first_streams AS (
    SELECT 
        s.content_id,
        s.user_id,
        u.subscription_tier,
        u.acquisition_channel
    FROM fact_streams s
    JOIN dim_users u ON s.user_id = u.user_id
    WHERE s.is_first_stream = 1
)
SELECT 
    c.content_id,
    c.title,
    c.original_language,
    c.primary_genre,
    c.type,
    COUNT(fs.user_id) AS first_stream_conversions,
    COUNT(CASE WHEN fs.subscription_tier = 'Premium' THEN 1 END) AS premium_tier_conversions,
    COUNT(CASE WHEN fs.subscription_tier = 'Super' THEN 1 END) AS super_tier_conversions,
    COUNT(CASE WHEN fs.subscription_tier = 'Free (AVOD)' THEN 1 END) AS free_tier_conversions
FROM first_streams fs
JOIN dim_content c ON fs.content_id = c.content_id
GROUP BY c.content_id, c.title, c.original_language, c.primary_genre, c.type
ORDER BY first_stream_conversions DESC
LIMIT 15;


-- ------------------------------------------------------------------------------
-- QUERY 9: Drop-off Hazard Analysis ("View Traps")
-- Business Value: High start volume but poor completion indicates deceptive trailers or poor narrative pacing.
-- ------------------------------------------------------------------------------
SELECT 
    c.content_id,
    c.title,
    c.original_language,
    c.primary_genre,
    c.type,
    c.licensing_tier,
    COUNT(s.stream_id) AS total_starts,
    ROUND(AVG(s.completion_percentage), 2) AS avg_completion_pct,
    COUNT(CASE WHEN s.completion_percentage < 30.0 THEN 1 END) AS early_dropoff_streams,
    ROUND(COUNT(CASE WHEN s.completion_percentage < 30.0 THEN 1 END) * 100.0 / COUNT(s.stream_id), 2) AS early_dropoff_rate_pct
FROM dim_content c
JOIN fact_streams s ON c.content_id = s.content_id
GROUP BY c.content_id, c.title, c.original_language, c.primary_genre, c.type, c.licensing_tier
HAVING COUNT(s.stream_id) >= 30 AND AVG(s.completion_percentage) < 45.0
ORDER BY total_starts DESC
LIMIT 15;


-- ------------------------------------------------------------------------------
-- QUERY 10: Device Preference & Viewing Hours Matrix
-- Business Value: Guides bitrate encoding and UI placement (Living room TV vs. Personal Mobile).
-- ------------------------------------------------------------------------------
SELECT 
    s.device_type,
    u.subscription_tier,
    COUNT(s.stream_id) AS total_streams,
    ROUND(SUM(s.watch_duration_minutes) / 60.0, 2) AS total_watch_hours,
    ROUND(AVG(s.watch_duration_minutes), 2) AS avg_session_duration_minutes,
    ROUND(AVG(s.completion_percentage), 2) AS avg_completion_pct,
    ROUND(COUNT(CASE WHEN s.playback_quality = '4K Ultra HD' THEN 1 END) * 100.0 / COUNT(s.stream_id), 2) AS pct_4k_streams
FROM fact_streams s
JOIN dim_users u ON s.user_id = u.user_id
GROUP BY s.device_type, u.subscription_tier
ORDER BY s.device_type, total_watch_hours DESC;


-- ------------------------------------------------------------------------------
-- QUERY 11: Power User Segmentation (Percentile Distribution via NTILE)
-- Business Value: Identifies the top 5% VIP streamers for loyalty perks and churn defense.
-- ------------------------------------------------------------------------------
WITH user_watch_totals AS (
    SELECT 
        u.user_id,
        u.subscription_tier,
        u.region,
        u.primary_language,
        COUNT(s.stream_id) AS total_stream_sessions,
        SUM(s.watch_duration_minutes) / 60.0 AS total_hours_streamed
    FROM dim_users u
    JOIN fact_streams s ON u.user_id = s.user_id
    GROUP BY u.user_id, u.subscription_tier, u.region, u.primary_language
),
user_percentiles AS (
    SELECT 
        *,
        NTILE(20) OVER (ORDER BY total_hours_streamed DESC) AS ventile_rank -- Top 1 = Top 5%
    FROM user_watch_totals
)
SELECT 
    CASE WHEN ventile_rank = 1 THEN 'Top 5% Power Users'
         WHEN ventile_rank BETWEEN 2 AND 4 THEN 'Top 6-20% Core Users'
         WHEN ventile_rank BETWEEN 5 AND 10 THEN 'Moderate Streamers (21-50%)'
         ELSE 'Casual Streamers (Bottom 50%)' END AS user_segment,
    COUNT(user_id) AS user_count,
    ROUND(AVG(total_hours_streamed), 2) AS avg_hours_per_user,
    ROUND(SUM(total_hours_streamed), 2) AS total_segment_hours,
    ROUND(SUM(total_hours_streamed) * 100.0 / (SELECT SUM(total_hours_streamed) FROM user_percentiles), 2) AS pct_of_platform_watch_hours
FROM user_percentiles
GROUP BY 1
ORDER BY avg_hours_per_user DESC;


-- ------------------------------------------------------------------------------
-- QUERY 12: Content Sunsetting Candidates (Cost Rationalization)
-- Business Value: Pinpoints underperforming licensed content to deprioritize/sunset, saving licensing fees.
-- ------------------------------------------------------------------------------
SELECT 
    c.content_id,
    c.title,
    c.licensing_tier,
    c.content_cost_usd,
    COUNT(s.stream_id) AS total_streams,
    COALESCE(ROUND(SUM(s.watch_duration_minutes) / 60.0, 2), 0) AS total_watch_hours,
    COALESCE(ROUND(AVG(s.completion_percentage), 2), 0) AS avg_completion_pct,
    -- Cost per Stream Hour (High cost + low hours = Immediate Candidate for Sunsetting)
    ROUND(c.content_cost_usd / NULLIF(SUM(s.watch_duration_minutes) / 60.0, 0), 2) AS cost_per_stream_hour_usd
FROM dim_content c
LEFT JOIN fact_streams s ON c.content_id = s.content_id
WHERE c.licensing_tier IN ('Medium', 'High')
GROUP BY c.content_id, c.title, c.licensing_tier, c.content_cost_usd
HAVING COUNT(s.stream_id) < 15 OR (c.content_cost_usd / NULLIF(SUM(s.watch_duration_minutes) / 60.0, 0)) > 500.0
ORDER BY cost_per_stream_hour_usd DESC
LIMIT 20;


-- ------------------------------------------------------------------------------
-- QUERY 13: Churn Risk by Acquisition Channel & Tier
-- Business Value: Informs marketing budget allocation toward channels delivering high-LTV users.
-- ------------------------------------------------------------------------------
SELECT 
    acquisition_channel,
    subscription_tier,
    COUNT(user_id) AS total_acquired_users,
    SUM(is_churned) AS total_churned_users,
    ROUND(SUM(is_churned) * 100.0 / COUNT(user_id), 2) AS churn_rate_pct,
    ROUND((COUNT(user_id) - SUM(is_churned)) * 100.0 / COUNT(user_id), 2) AS retention_rate_pct
FROM dim_users
GROUP BY acquisition_channel, subscription_tier
ORDER BY acquisition_channel, churn_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 14: Rolling 7-Day Moving Average of Watch Hours
-- Business Value: Smooths day-to-day noise to expose true consumption trends by tier.
-- ------------------------------------------------------------------------------
WITH daily_tier_hours AS (
    SELECT 
        s.stream_date,
        u.subscription_tier,
        SUM(s.watch_duration_minutes) / 60.0 AS daily_watch_hours
    FROM fact_streams s
    JOIN dim_users u ON s.user_id = u.user_id
    GROUP BY s.stream_date, u.subscription_tier
)
SELECT 
    stream_date,
    subscription_tier,
    ROUND(daily_watch_hours, 2) AS daily_hours,
    ROUND(
        AVG(daily_watch_hours) OVER (
            PARTITION BY subscription_tier 
            ORDER BY stream_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_7day_avg_hours
FROM daily_tier_hours
ORDER BY stream_date DESC, subscription_tier;


-- ------------------------------------------------------------------------------
-- QUERY 15: Evergreen Content Identification (Sustained Long-Tail Consumption)
-- Business Value: Finds titles released > 2 years ago that still drive top 10% viewership.
-- ------------------------------------------------------------------------------
SELECT 
    c.content_id,
    c.title,
    c.release_year,
    c.primary_genre,
    c.original_language,
    COUNT(s.stream_id) AS total_streams_2023_2024,
    ROUND(SUM(s.watch_duration_minutes) / 60.0, 2) AS total_watch_hours,
    ROUND(AVG(s.completion_percentage), 2) AS avg_completion_pct,
    ROUND(SUM(s.is_repeat_stream) * 100.0 / COUNT(s.stream_id), 2) AS repeat_stream_pct
FROM dim_content c
JOIN fact_streams s ON c.content_id = s.content_id
WHERE c.release_year <= 2020
GROUP BY c.content_id, c.title, c.release_year, c.primary_genre, c.original_language
HAVING COUNT(s.stream_id) >= 40
ORDER BY repeat_stream_pct DESC, total_watch_hours DESC
LIMIT 15;
