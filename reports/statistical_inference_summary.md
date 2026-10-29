# Disney+ Hotstar Statistical Inference & Hypothesis Testing Report
**Project Lead:** Kalyani Gajanan Nemade (Independent Analytics Portfolio Project)

## Executive Statistical Summary

| Test # | Hypothesis Question | Statistical Test Applied | Test Statistic | p-value | Decision ($\\alpha = 0.05$) | Business Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Does viewer completion rate differ across content languages? | One-Way ANOVA | $F = 238.6259$ | $2.0493e-154$ | Reject $H_0$ | Significant language variance; South Indian regional content demonstrates higher stickiness. |
| **2** | Does watch duration per session differ between Movies and TV Shows? | Welch's Two-Sample T-Test | $t = -341.8694$ | $0.0000e+00$ | Reject $H_0$ | TV shows drive extended multi-episode sessions, making them prime vehicles for ad-insertion. |
| **3** | Is subscriber churn dependent on subscription tier? | Chi-Square ($\\chi^2$) Independence | $\\chi^2 = 1240.9807$ | $3.3455e-270$ | Reject $H_0$ | Free tier exhibits 3.2x higher churn vulnerability than Premium tier. |
| **4** | Is higher completion rate correlated with user satisfaction ratings? | Pearson & Spearman Correlation | $r = 0.6946$ | $0.0000e+00$ | Statistically Significant | Strong positive correlation indicates completion rate is a valid proxy for content quality. |

---

## 5-Tier Content Portfolio Segmentation

| Segment Name | Definition | Catalog Share | Actionable Business Strategy |
| :--- | :--- | :--- | :--- |
| **Platform Blockbusters** | High Views & High Completion | ~25% | Core anchors; renew licenses immediately and leverage for top-of-funnel marketing. |
| **Hidden Gems / Sleeper Hits** | Low Views & High Completion | ~25% | High satisfaction but low discovery; feature prominently in recommendation carousels. |
| **View Traps (Early Drop-off)**| High Views & Low Completion | ~25% | High initial clicks but poor retention; investigate misleading thumbnails or poor pacing. |
| **Catalog Clutter** | Low Views & Low Completion | ~25% | Deprioritize, renegotiate licensing fees down, or sunset to save hosting costs. |
