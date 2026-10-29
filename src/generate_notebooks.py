"""
Notebook Generator for Disney+ Hotstar Analytics Project
Creates 3 fully documented Jupyter Notebooks (.ipynb) in the notebooks/ folder.

Author: Kalyani Gajanan Nemade (Independent Analytics Project)
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(BASE_DIR, "notebooks")
os.makedirs(NB_DIR, exist_ok=True)

def create_notebook(cells, filepath):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Created notebook: {filepath}")

def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [text]}

def code_cell(code):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [code]}

# ------------------------------------------------------------------------------
# Notebook 1: Data Cleaning & Profiling
# ------------------------------------------------------------------------------
nb1_cells = [
    md_cell("# Disney+ Hotstar Analytics: Module 1 - Data Profiling, Cleaning & Star Schema Ingestion\n**Author:** Kalyani Gajanan Nemade (Independent Analytics Project)"),
    md_cell("### 1. Ingestion & Library Setup"),
    code_cell("import os\nimport pandas as pd\nimport numpy as np\n\ndata_dir = '../data/processed'\ndim_content = pd.read_csv(os.path.join(data_dir, 'dim_content.csv'))\ndim_users = pd.read_csv(os.path.join(data_dir, 'dim_users.csv'))\ndim_date = pd.read_csv(os.path.join(data_dir, 'dim_date.csv'))\nfact_streams = pd.read_csv(os.path.join(data_dir, 'fact_streams.csv'))\n\nprint(f'Content: {dim_content.shape}')\nprint(f'Users: {dim_users.shape}')\nprint(f'Date: {dim_date.shape}')\nprint(f'Streams: {fact_streams.shape}')"),
    md_cell("### 2. Missing Value & Cardinality Profiling"),
    code_cell("print('--- Missing Values in Streams ---')\nprint(fact_streams.isnull().sum())\n\nprint('\\n--- Unique User Regions ---')\nprint(dim_users['region'].value_counts())\n\nprint('\\n--- Content by Primary Genre ---')\nprint(dim_content['primary_genre'].value_counts())"),
    md_cell("### 3. Data Integrity & Type Validation"),
    code_cell("fact_streams['stream_date'] = pd.to_datetime(fact_streams['stream_date'])\ndim_users['signup_date'] = pd.to_datetime(dim_users['signup_date'])\n\nassert (fact_streams['completion_percentage'] <= 100).all(), 'Completion rate exceeds 100%!'\nassert (fact_streams['completion_percentage'] >= 0).all(), 'Negative completion rate!'\nprint('Data integrity assertions passed successfully!')")
]
create_notebook(nb1_cells, os.path.join(NB_DIR, "01_data_cleaning_and_profiling.ipynb"))

# ------------------------------------------------------------------------------
# Notebook 2: Exploratory Data Analysis
# ------------------------------------------------------------------------------
nb2_cells = [
    md_cell("# Disney+ Hotstar Analytics: Module 2 - Exploratory Data Analysis & Consumption Dynamics\n**Author:** Kalyani Gajanan Nemade (Independent Analytics Project)"),
    md_cell("### 1. Genre Efficiency Analysis"),
    code_cell("import os\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\ndata_dir = '../data/processed'\ndim_content = pd.read_csv(os.path.join(data_dir, 'dim_content.csv'))\nfact_streams = pd.read_csv(os.path.join(data_dir, 'fact_streams.csv'))\n\nmerged = fact_streams.merge(dim_content, on='content_id')\ngenre_perf = merged.groupby('primary_genre').agg(\n    total_streams=('stream_id', 'count'),\n    total_hours=('watch_duration_minutes', lambda x: x.sum()/60.0),\n    avg_comp=('completion_percentage', 'mean')\n).reset_index()\n\ngenre_perf.sort_values(by='total_hours', ascending=False)"),
    md_cell("### 2. Language Consumption & South Indian Regional Stickiness"),
    code_cell("lang_perf = merged.groupby('original_language').agg(\n    titles=('content_id', 'nunique'),\n    total_hours=('watch_duration_minutes', lambda x: x.sum()/60.0),\n    avg_comp=('completion_percentage', 'mean')\n).reset_index().sort_values(by='total_hours', ascending=False)\n\nprint(lang_perf)")
]
create_notebook(nb2_cells, os.path.join(NB_DIR, "02_eda_and_insights.ipynb"))

# ------------------------------------------------------------------------------
# Notebook 3: Advanced Analytics & Scoring
# ------------------------------------------------------------------------------
nb3_cells = [
    md_cell("# Disney+ Hotstar Analytics: Module 3 - Content Scoring (CPS), Segmentation & Statistical Tests\n**Author:** Kalyani Gajanan Nemade (Independent Analytics Project)"),
    md_cell("### 1. Statistical Hypothesis Testing (ANOVA & Chi-Square)"),
    code_cell("from scipy import stats\n\n# Chi-Square Test on Churn vs Tier\ndim_users = pd.read_csv(os.path.join('../data/processed', 'dim_users.csv'))\nct = pd.crosstab(dim_users['subscription_tier'], dim_users['is_churned'])\nchi2, p, dof, ex = stats.chi2_contingency(ct)\nprint(f'Chi2: {chi2:.4f}, p-value: {p:.4e}')\nprint(ct)"),
    md_cell("### 2. 5-Tier Content Portfolio Segmentation Matrix"),
    code_cell("scored_content = pd.read_csv(os.path.join('../data/processed', 'dim_content_scored.csv'))\nprint(scored_content['content_segment'].value_counts())\nprint(scored_content.groupby('content_segment')['cps_score'].mean())")
]
create_notebook(nb3_cells, os.path.join(NB_DIR, "03_advanced_analytics_and_scoring.ipynb"))

print("All notebooks created successfully!")
