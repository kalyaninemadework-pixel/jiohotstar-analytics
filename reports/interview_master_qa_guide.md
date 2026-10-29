# JioHotstar Analytics Master Interview Preparation & Pitch Guide

**Author:** Kalyani Gajanan Nemade (Independent Analytics Portfolio Project)  
**Domain:** Post-Merger OTT Streaming (JioCinema + Disney+ Hotstar), Product Analytics, SQL & BI  

---

## 1. 10 High-Impact Resume Bullet Points

1. **Architected End-to-End Post-Merger OTT Analytics Pipeline:** Modeled 5,000 titles, 25,000 user cohorts, and 150,000 streaming events in Python and PostgreSQL to analyze catalog synergy and churn drivers for the unified **JioHotstar** platform.
2. **Engineered Content Performance Scoring (CPS):** Formulated a weighted 0–100 multi-attribute algorithm in Python combining completion rates, repeat viewership, and normalized watch hours to classify post-merger content into 5 strategic quadrants.
3. **Uncovered Post-IPL Acquisition Churn Hazard:** Analyzed customer decay curves and revealed a 54.06% 90-day churn rate in sports-acquired users, formulating a "Bridge-to-Entertainment" retention funnel to cross-sell Disney+ originals to Jio free cricket streamers.
4. **Conducted Advanced Hypothesis Testing:** Executed One-Way ANOVA ($F=238.63, p < 0.001$) and Chi-Square tests ($\chi^2=1240.98, p < 0.001$) to prove regional language stickiness and tier-based churn vulnerability.
5. **Identified 1,059 Catalog Sunsetting Candidates:** Wrote advanced SQL CTEs and window functions to pinpoint redundant licensed titles with Cost-per-Stream-Hour $> \$500$, proposing $\$3.5\text{M}–\$5\text{M}$ in post-merger catalog cost savings.
6. **Analyzed View Trap & Drop-Off Dynamics:** Flagged 1,268 deceptive titles with $>30$ stream starts but $<45\%$ completion rates, establishing an automated thumbnail/trailer audit trigger.
7. **Designed 4-Page Power BI Executive Suite:** Built interactive C-Suite dashboards tracking Content Efficiency Ratios, 90-day cohort heatmaps, and living-room device breakdowns using advanced DAX.
8. **Demonstrated Regional Cross-Consumption Trends:** Identified that 28% of South Indian cinema streams originate from non-native speakers, justifying increased pan-Indian dubbing investments.
9. **Optimized Multi-Device Experience:** Uncovered that Smart TV sessions generate 2.1x longer watch duration (118 min vs. 56 min on Mobile), guiding OEM pre-install partnerships for JioFiber / Smart TVs.
10. **Authored Executive Strategy Memo:** Delivered a comprehensive 10-point actionable memo for content commissioning, licensing renegotiation, and personalized user onboarding for JioStar leadership.

---

## 2. 2-Minute Interview Pitch (The "Elevator Hook")

> *"In my flagship independent project, I built an end-to-end OTT Content Intelligence and Post-Merger Catalog Synergy case study on **JioHotstar**—the unified entity created by the \$8.5B Reliance-Disney merger. The core business challenge was navigating the post-IPL subscriber churn cliff and eliminating redundant catalog licensing expenses.*
> 
> *Using Python and a PostgreSQL relational star schema, I analyzed 5,000 titles and 150,000 streaming sessions. I engineered an algorithmic 0–100 Content Performance Score (CPS) that balances stream volume with completion rates to uncover high-volume 'View Traps' versus high-retention 'Hidden Gems'.*
> 
> *My statistical analysis proved two critical business realities: First, free users acquired through marquee sports tournaments suffer an alarming 54% 90-day churn cliff once matches end. Second, regional South Indian content delivers a 1.35x content efficiency ratio at 35% lower cost.*
> 
> *I synthesized these insights into a 4-page Power BI dashboard and presented actionable strategies to sunset 1,059 dead catalog titles—saving up to \$5M annually—while bridging sports viewers into serialized regional entertainment."*

---

## 3. 5-Minute Detailed Technical Walkthrough

> *"When designing this Disney+ Hotstar analytics project, I approached it from the perspective of a Senior Product and BI Analyst evaluating three core levers: Acquisition, Engagement Quality, and Long-Term Retention.*
> 
> *First, I established a relational Star Schema with dim_content, dim_users, dim_date, and fact_streams. Rather than relying on simple view counts, which often reward clickbait, I engineered behavioral metrics like the Average Completion Rate and Content Re-watch Rate.*
> 
> *Second, I built an algorithmic Content Performance Score in Python and SQL using Min-Max normalization. I weighted 30% view volume, 25% completion percentage, 20% total watch hours, 15% user rating, and 10% repeat stream propensity. This segmented the catalog into 5 distinct operational quadrants: Platform Blockbusters, Hidden Gems, View Traps, and Catalog Clutter.*
> 
> *Third, I applied formal statistical hypothesis testing: A One-Way ANOVA confirmed statistically significant variance across content languages (p < 0.001), showing Tamil and Telugu content holding higher audience stickiness. A Chi-Square test confirmed that Free/AVOD users churn at 3.2x the rate of Premium subscribers.*
> 
> *Fourth, I authored 15 production-grade SQL queries utilizing window functions, dense ranking, rolling 7-day averages, and multi-month cohort retention matrices.*
> 
> *Finally, I translated these findings into a 4-page Power BI executive suite with actionable DAX measures and authored a strategic C-Suite memo detailing catalog pruning and personalized onboarding funnels."*

---

## 4. Top Technical & Business Q&A

### SQL Questions & Model Answers:
1. **Q: How did you calculate month-over-month active streamer growth in SQL?**  
   *A:* "I used the `LAG()` window function partitioned over chronological month order within a CTE aggregating distinct `user_id`s, calculating the percentage variance against the previous month while handling null denominators with `NULLIF()`."
2. **Q: How did you implement the cohort retention matrix in SQL?**  
   *A:* "I extracted the cohort signup month from `dim_users` and calculated the month offset for every stream event in `fact_streams` using date arithmetic, aggregating distinct active users across M0, M1, M2, and M3 offsets via conditional `CASE WHEN` aggregation."
3. **Q: Why use `DENSE_RANK()` instead of `ROW_NUMBER()` for ranking top titles?**  
   *A:* "`DENSE_RANK()` preserves ties in completion rate without skipping rank integers, ensuring fairness when multiple titles share identical performance benchmarks."

### Power BI & DAX Questions:
1. **Q: How did you implement dynamic Content Efficiency Ratio in DAX?**  
   *A:* "I computed the ratio of the selected genre's share of `[Total Watch Hours]` divided by its share of total catalog titles, using `ALLSELECTED(dim_content)` to maintain contextual denominator integrity under user filtering."
2. **Q: How did you optimize DAX performance across 150k rows?**  
   *A:* "I enforced a clean 1:N Star Schema, created integer surrogate date keys, avoided bi-directional cross-filtering, and used variables (`VAR`) to prevent recalculating scalar sub-expressions."

### Product & Business Strategy Questions:
1. **Q: If Disney+ Hotstar leadership asked how to cut \$5M from content licensing, what is your methodology?**  
   *A:* "I would query the 1,059 titles in our 'Catalog Clutter' quadrant having Cost-per-Stream-Hour $> \$500$ and $<15$ active streams. Sunsetting these bottom 20% titles immediately recaptures trapped capital without negatively impacting MAU or retention."
2. **Q: How would you prevent post-IPL subscriber churn?**  
   *A:* "By creating an automated bridge: 7 days prior to tournament conclusion, track each sports subscriber's demographic region and push personalized 3-episode hooks of regional serialized thrillers and comedies to build viewing habits before the sports season ends."
