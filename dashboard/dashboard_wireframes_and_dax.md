# Disney+ Hotstar Analytics Power BI Dashboard Architecture & DAX Handbook

**Author:** Kalyani Gajanan Nemade (Independent Analytics Portfolio Project)  
**Target Platform:** Power BI Desktop & Service  
**Data Model:** Star Schema (`dim_content`, `dim_users`, `dim_date`, `fact_streams`)

---

## 1. Master DAX Measures Repository

### Core Volume & Consumption Measures
```dax
-- Total Streaming Sessions
Total Streams = COUNTROWS(fact_streams)

-- Total Watch Hours
Total Watch Hours = 
DIVIDE(
    SUM(fact_streams[watch_duration_minutes]),
    60,
    0
)

-- Average Completion Rate (%)
Average Completion Rate = 
AVERAGE(fact_streams[completion_percentage])

-- Active Streamers (Monthly / Period)
Active Streamers = 
DISTINCTCOUNT(fact_streams[user_id])

-- Average User Rating
Average User Rating = 
AVERAGE(fact_streams[user_rating])

-- Content Re-watch Rate (%)
Rewatch Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(fact_streams), fact_streams[is_repeat_stream] = 1),
    COUNTROWS(fact_streams),
    0
) * 100
```

### Advanced Intelligence & Growth Measures
```dax
-- Month-over-Month (MoM) Watch Hours Growth %
MoM Watch Hours Growth % = 
VAR CurrentMonthHours = [Total Watch Hours]
VAR PreviousMonthHours = 
    CALCULATE(
        [Total Watch Hours],
        DATEADD(dim_date[full_date], -1, MONTH)
    )
RETURN
DIVIDE(CurrentMonthHours - PreviousMonthHours, PreviousMonthHours, 0) * 100

-- Content Efficiency Ratio (Genre / Title)
Content Efficiency Ratio = 
VAR GenreHoursShare = 
    DIVIDE(
        [Total Watch Hours], 
        CALCULATE([Total Watch Hours], ALLSELECTED(dim_content))
    )
VAR GenreCatalogShare = 
    DIVIDE(
        DISTINCTCOUNT(dim_content[content_id]), 
        CALCULATE(DISTINCTCOUNT(dim_content[content_id]), ALLSELECTED(dim_content))
    )
RETURN
DIVIDE(GenreHoursShare, GenreCatalogShare, 0)

-- Churn Rate %
Subscriber Churn Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(dim_users), dim_users[is_churned] = 1),
    COUNTROWS(dim_users),
    0
) * 100

-- First-Stream Conversion Attribution
First Stream Conversions = 
CALCULATE(
    COUNTROWS(fact_streams),
    fact_streams[is_first_stream] = 1
)

-- Content Performance Score (CPS) Measure
CPS Score = 
VAR MaxStreams = MAXX(ALL(dim_content), [Total Streams])
VAR MinStreams = MINX(ALL(dim_content), [Total Streams])
VAR MaxHours = MAXX(ALL(dim_content), [Total Watch Hours])
VAR MinHours = MINX(ALL(dim_content), [Total Watch Hours])

VAR NormStreams = DIVIDE([Total Streams] - MinStreams, MaxStreams - MinStreams, 0) * 100
VAR NormHours = DIVIDE([Total Watch Hours] - MinHours, MaxHours - MinHours, 0) * 100
VAR NormCompletion = [Average Completion Rate]
VAR NormRating = DIVIDE([Average User Rating], 5, 0) * 100
VAR NormRewatch = [Rewatch Rate %]

RETURN
(0.30 * NormStreams) + 
(0.25 * NormCompletion) + 
(0.20 * NormHours) + 
(0.15 * NormRating) + 
(0.10 * NormRewatch)
```

---

## 2. Power BI 4-Page Wireframe & Visual Specifications

### Page 1: Executive KPI Overview (Macro Health)
* **Top KPI Banner Cards:**
  1. Total Stream Sessions: `150,000`
  2. Total Watch Hours: `379,453.6 Hrs`
  3. Avg Completion Rate: `63.1%`
  4. Active Users: `25,000`
  5. Platform Churn Rate: `31.3%`
* **Visual 1 (Area / Line Chart):** Monthly Stream Hours Trend with IPL Season Shading (`dim_date[is_ipl_season]`).
* **Visual 2 (Donut Chart):** Watch Hours Share by Subscription Tier (Free vs. Super vs. Premium).
* **Visual 3 (Clustered Bar Chart):** Genre Catalog Volume vs. Watch Hours Share (with Efficiency Ratio tooltips).
* **Visual 4 (Map / Tree-map):** Regional Consumption Heatmap across India (North, South, West, East, Metro).

### Page 2: Content Performance & CPS Leaderboard
* **Visual 1 (Quadrant Scatter Plot):**
  - X-Axis: `Total Streams` (Log scale)
  - Y-Axis: `Average Completion Rate (%)`
  - Bubble Size: `Content Performance Score (CPS)`
  - Color Legend: `Primary Genre`
  - Quadrant Lines: Median Streams & Median Completion Rate.
* **Visual 2 (Matrix / Table Visual):**
  - Columns: `Title`, `Type`, `Language`, `Genre`, `Total Streams`, `Watch Hours`, `ACR %`, `Rating`, `CPS Score`, `Content Segment`.
  - Conditional Formatting: Color scale on CPS Score and Data bars on Completion Rate.
* **Interactive Slicers:** Language, Genre, Content Type (Movie vs. TV Show), Release Year Range, Licensing Tier.

### Page 3: User Cohort & Retention Dynamics
* **Visual 1 (Cohort Matrix Heatmap):**
  - Rows: `Signup Cohort Month` (2023-01 to 2024-03)
  - Columns: `Month Offset` (M0, M1, M2, M3, M6)
  - Values: `Retention %` with conditional gradient background.
* **Visual 2 (Line Chart):** 90-Day Churn Hazard Curve by Acquisition Channel (IPL vs. Tentpole Movie vs. Telco vs. Organic).
* **Visual 3 (Stacked Bar Chart):** Device Type Breakdown by Subscription Tier (Smart TV vs. Mobile vs. Web).

### Page 4: Strategic Action & Sunsetting Hub
* **Visual 1 (Decomposition Tree):** Root: `Total Churn` $\rightarrow$ Branch 1: `Acquisition Channel` $\rightarrow$ Branch 2: `Subscription Tier` $\rightarrow$ Branch 3: `Primary Language`.
* **Visual 2 (Sunsetting Action Table):**
  - Content with Cost > \$50,000 and Cost per Stream Hour > \$500.
  - Action Tag: `Deprioritize / Non-Renewal Candidate`.
* **Visual 3 (Opportunity Card Matrix):**
  - Top 10 "Hidden Gems" ready for promotion on Homepage Carousel.
  - Top 10 "View Traps" needing thumbnail/trailer audit.
