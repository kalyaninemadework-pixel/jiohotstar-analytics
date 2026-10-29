"""
Disney+ Hotstar Simulated Data Engine
Generates an enterprise-grade, realistic relational dataset simulating Disney+ Hotstar's
catalog, user demographics, streaming telemetry, and viewing behaviors.

Author: Kalyani Gajanan Nemade (Independent Analytics Project)
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set deterministic random seed for reproducibility
np.random.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

print("Starting Disney+ Hotstar Data Engine generation...")

# ==============================================================================
# 1. GENERATE DIM_CONTENT (5,000 Catalog Titles)
# ==============================================================================
NUM_CONTENT = 5000

languages = ["Hindi", "Tamil", "Telugu", "Malayalam", "English", "Bengali", "Marathi", "Kannada"]
lang_weights = [0.40, 0.16, 0.14, 0.08, 0.12, 0.04, 0.04, 0.02]

genres = ["Drama", "Action", "Romance", "Comedy", "Thriller", "Sci-Fi", "Crime", "Animation", "Documentary", "Horror", "Sports"]
genre_weights = [0.25, 0.20, 0.15, 0.12, 0.10, 0.05, 0.05, 0.03, 0.02, 0.02, 0.01]

content_types = ["Movie", "TV Show"]
type_weights = [0.65, 0.35]

age_ratings = ["U", "U/A 7+", "U/A 13+", "U/A 16+", "A"]
age_weights = [0.15, 0.20, 0.35, 0.20, 0.10]

licensing_tiers = ["Low", "Medium", "High", "Hotstar Specials / Original"]
tier_weights = [0.45, 0.30, 0.15, 0.10]

directors_pool = [
    "Anurag Kashyap", "Rajkumar Hirani", "Mani Ratnam", "S. S. Rajamouli", "Sukumar",
    "Lokesh Kanagaraj", "Zoya Akhtar", "Neeraj Pandey", "Jeethu Joseph", "Shoojit Sircar",
    "Christopher Nolan", "Jon Favreau", "James Cameron", "Taika Waititi", "Kabir Khan",
    "Vetrimaaran", "Pa. Ranjith", "Ayan Mukerji", "Sanjay Leela Bhansali", "Priyadarshan"
]

actors_pool = [
    "Shah Rukh Khan", "Deepika Padukone", "Ranbir Kapoor", "Alia Bhatt", "Manoj Bajpayee",
    "Vijay Sethupathi", "Samantha Ruth Prabhu", "Allu Arjun", "Kamal Haasan", "Fahadh Faasil",
    "Mohanlal", "Dulquer Salmaan", "Nawazuddin Siddiqui", "Kay Kay Menon", "Pankaj Tripathi",
    "Robert Downey Jr.", "Scarlett Johansson", "Benedict Cumberbatch", "Tom Hiddleston", "Pedro Pascal"
]

title_adjectives = ["The Secret", "Unbroken", "Silent", "Lost", "Infinite", "Midnight", "Golden", "Shadow", "Sacred", "Fierce", "Eternal", "Rogue", "Crimson", "Royal", "Dark", "Hidden"]
title_nouns = ["Empire", "Echo", "Warrior", "Legacy", "Chronicles", "Vengeance", "Lies", "Destiny", "Frontier", "Heist", "Paradox", "Journey", "Conspiracy", "Saga", "Storm", "Night"]

content_data = []
for i in range(1, NUM_CONTENT + 1):
    c_id = f"CONT_{i:05d}"
    c_type = np.random.choice(content_types, p=type_weights)
    c_lang = np.random.choice(languages, p=lang_weights)
    c_genre1 = np.random.choice(genres, p=genre_weights)
    remaining_genres = [g for g in genres if g != c_genre1]
    c_genre2 = random.choice(remaining_genres) if random.random() > 0.3 else None
    
    adj = random.choice(title_adjectives)
    noun = random.choice(title_nouns)
    title = f"{adj} {noun} ({c_lang})" if random.random() > 0.6 else f"{c_lang} {noun}: Chapter {i % 10 + 1}"
    
    if c_type == "Movie":
        runtime = int(np.clip(np.random.normal(125, 20), 75, 210))
        episodes = 1
    else:
        episodes = int(np.clip(np.random.poisson(12), 4, 45))
        runtime = episodes * int(np.clip(np.random.normal(40, 8), 25, 60))
        
    rel_year = int(np.random.choice(
        range(2012, 2025),
        p=[0.03, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.13, 0.10, 0.10]
    ))
    
    age_rat = np.random.choice(age_ratings, p=age_weights)
    lic_tier = np.random.choice(licensing_tiers, p=tier_weights)
    
    # Cost modeling
    if lic_tier == "Low":
        cost = round(np.random.uniform(10000, 50000), 2)
    elif lic_tier == "Medium":
        cost = round(np.random.uniform(50000, 200000), 2)
    elif lic_tier == "High":
        cost = round(np.random.uniform(200000, 800000), 2)
    else: # Originals
        cost = round(np.random.uniform(800000, 2500000), 2)
        
    director = random.choice(directors_pool)
    lead_actor = random.choice(actors_pool)
    
    content_data.append({
        "content_id": c_id,
        "title": title,
        "type": c_type,
        "primary_genre": c_genre1,
        "secondary_genre": c_genre2,
        "original_language": c_lang,
        "runtime_minutes": runtime,
        "total_episodes": episodes,
        "release_year": rel_year,
        "age_rating": age_rat,
        "licensing_tier": lic_tier,
        "content_cost_usd": cost,
        "director": director,
        "lead_actor": lead_actor
    })

df_content = pd.DataFrame(content_data)
print(f"Generated {len(df_content)} content titles in dim_content.")

# ==============================================================================
# 2. GENERATE DIM_USERS (25,000 Users)
# ==============================================================================
NUM_USERS = 25000

sub_tiers = ["Free (AVOD)", "Super", "Premium"]
sub_weights = [0.45, 0.35, 0.20]

regions = ["North India", "South India", "West India", "East India", "Metro Central"]
region_weights = [0.30, 0.35, 0.20, 0.08, 0.07]

acq_channels = ["IPL Cricket Campaign", "Tentpole Movie Release", "Digital Performance Ads", "Telco Partnership (Jio/Airtel)", "Organic / Word of Mouth"]
acq_weights = [0.35, 0.25, 0.15, 0.15, 0.10]

age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
age_group_weights = [0.35, 0.40, 0.15, 0.07, 0.03]

start_signup = datetime(2023, 1, 1)
end_signup = datetime(2024, 6, 30)
days_range = (end_signup - start_signup).days

user_data = []
for u in range(1, NUM_USERS + 1):
    u_id = f"USR_{u:06d}"
    tier = np.random.choice(sub_tiers, p=sub_weights)
    region = np.random.choice(regions, p=region_weights)
    
    # Language preference correlated with region
    if region == "South India":
        pref_lang = np.random.choice(["Tamil", "Telugu", "Malayalam", "Kannada", "Hindi", "English"], p=[0.35, 0.30, 0.15, 0.08, 0.07, 0.05])
    elif region == "North India":
        pref_lang = np.random.choice(["Hindi", "English", "Punjabi"], p=[0.80, 0.15, 0.05])
    elif region == "West India":
        pref_lang = np.random.choice(["Hindi", "Marathi", "Gujarati", "English"], p=[0.55, 0.25, 0.10, 0.10])
    elif region == "East India":
        pref_lang = np.random.choice(["Hindi", "Bengali", "English"], p=[0.50, 0.40, 0.10])
    else:
        pref_lang = np.random.choice(["English", "Hindi"], p=[0.50, 0.50])
        
    acq_channel = np.random.choice(acq_channels, p=acq_weights)
    age_grp = np.random.choice(age_groups, p=age_group_weights)
    
    signup_dt = start_signup + timedelta(days=int(np.random.uniform(0, days_range)))
    
    # Churn probability higher for IPL campaign and Free tier
    base_churn = 0.20
    if acq_channel == "IPL Cricket Campaign":
        base_churn += 0.20
    if tier == "Free (AVOD)":
        base_churn += 0.15
    elif tier == "Premium":
        base_churn -= 0.12
        
    is_churned = 1 if random.random() < max(0.05, min(0.75, base_churn)) else 0
    churn_date = signup_dt + timedelta(days=int(np.random.exponential(45) + 15)) if is_churned else None
    if churn_date and churn_date > datetime(2024, 12, 31):
        is_churned = 0
        churn_date = None
        
    user_data.append({
        "user_id": u_id,
        "signup_date": signup_dt.strftime("%Y-%m-%d"),
        "subscription_tier": tier,
        "region": region,
        "primary_language": pref_lang,
        "acquisition_channel": acq_channel,
        "age_group": age_grp,
        "is_churned": is_churned,
        "churn_date": churn_date.strftime("%Y-%m-%d") if churn_date else None
    })

df_users = pd.DataFrame(user_data)
print(f"Generated {len(df_users)} user profiles in dim_users.")

# ==============================================================================
# 3. GENERATE DIM_DATE (2023-01-01 to 2024-12-31)
# ==============================================================================
date_range = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
date_data = []

# IPL windows: March-May 2023, March-May 2024
for dt in date_range:
    d_id = int(dt.strftime("%Y%m%d"))
    yr = dt.year
    qtr = f"Q{dt.quarter}"
    mo = dt.month
    mo_name = dt.strftime("%B")
    dow = dt.dayofweek
    dow_name = dt.strftime("%A")
    is_weekend = 1 if dow in [5, 6] else 0
    
    # IPL Season Flag
    is_ipl = 1 if ((yr == 2023 and mo in [3, 4, 5]) or (yr == 2024 and mo in [3, 4, 5])) else 0
    
    # Major festive holiday season (Diwali / World Cup / Year-end)
    is_festive = 1 if (mo in [10, 11, 12] or dt.strftime("%m-%d") in ["01-26", "08-15", "10-02"]) else 0
    
    date_data.append({
        "date_id": d_id,
        "full_date": dt.strftime("%Y-%m-%d"),
        "year": yr,
        "quarter": qtr,
        "month": mo,
        "month_name": mo_name,
        "day_of_week": dow + 1,
        "day_name": dow_name,
        "is_weekend": is_weekend,
        "is_ipl_season": is_ipl,
        "is_festive_season": is_festive
    })

df_date = pd.DataFrame(date_data)
print(f"Generated {len(df_date)} date records in dim_date.")

# ==============================================================================
# 4. GENERATE FACT_STREAMS (150,000 Streaming Events)
# ==============================================================================
NUM_STREAMS = 150000

devices = ["Mobile Phone", "Smart TV", "Web / Laptop", "Tablet"]
device_weights = [0.55, 0.28, 0.12, 0.05]

networks = ["Jio 5G / 4G", "Airtel 5G / 4G", "Home Broadband Wi-Fi", "Other Mobile Data"]
network_weights = [0.42, 0.33, 0.20, 0.05]

qualities = ["SD (480p)", "HD (1080p)", "4K Ultra HD"]

# Popularity skew in content (Power Law / Pareto)
content_popularity = np.random.pareto(a=1.8, size=NUM_CONTENT)
content_probs = content_popularity / np.sum(content_popularity)
content_ids = df_content["content_id"].values
content_runtime_map = dict(zip(df_content["content_id"], df_content["runtime_minutes"]))
content_lang_map = dict(zip(df_content["content_id"], df_content["original_language"]))
content_type_map = dict(zip(df_content["content_id"], df_content["type"]))

user_ids = df_users["user_id"].values
user_signup_map = dict(zip(df_users["user_id"], pd.to_datetime(df_users["signup_date"])))
user_churn_map = dict(zip(df_users["user_id"], pd.to_datetime(df_users["churn_date"])))
user_tier_map = dict(zip(df_users["user_id"], df_users["subscription_tier"]))
user_lang_map = dict(zip(df_users["user_id"], df_users["primary_language"]))

# User activity weight (Active users stream more)
user_stream_capacity = np.random.poisson(lam=6, size=NUM_USERS) + 1
user_stream_probs = user_stream_capacity / np.sum(user_stream_capacity)

stream_records = []
print("Simulating streaming sessions with realistic behavioral distributions...")

# Pre-sample users and content
sampled_users = np.random.choice(user_ids, size=NUM_STREAMS, p=user_stream_probs)
sampled_content = np.random.choice(content_ids, size=NUM_STREAMS, p=content_probs)

for s in range(NUM_STREAMS):
    u_id = sampled_users[s]
    c_id = sampled_content[s]
    
    u_signup = user_signup_map[u_id]
    u_churn = user_churn_map[u_id]
    u_tier = user_tier_map[u_id]
    u_lang = user_lang_map[u_id]
    
    # Determine stream timestamp between signup and churn/end-of-period
    end_bound = u_churn if pd.notnull(u_churn) else datetime(2024, 12, 31)
    if end_bound < u_signup:
        end_bound = u_signup + timedelta(days=30)
        
    delta_days = (end_bound - u_signup).days
    stream_dt = u_signup + timedelta(days=int(np.random.exponential(delta_days * 0.4) % max(1, delta_days)))
    
    runtime = content_runtime_map[c_id]
    c_lang = content_lang_map[c_id]
    c_type = content_type_map[c_id]
    
    # Language match affinity boost
    lang_affinity = 1.2 if c_lang == u_lang else 0.85
    
    # Completion rate modeled with Beta distribution
    # Beta(a, b): Highly engaging content has higher alpha
    if c_type == "TV Show":
        # Bingeable TV Shows tend to have bi-modal: drop early or finish episode
        alpha = 3.5 * lang_affinity
        beta = 1.8
    else:
        # Movies have smoother drop-off
        alpha = 4.0 * lang_affinity
        beta = 2.2
        
    comp_pct = round(float(np.clip(np.random.beta(alpha, beta) * 100, 5.0, 100.0)), 2)
    watch_mins = round((comp_pct / 100.0) * runtime, 2)
    
    device = np.random.choice(devices, p=device_weights)
    network = np.random.choice(networks, p=network_weights)
    
    # Quality depends on tier and device
    if u_tier == "Premium" and device in ["Smart TV", "Web / Laptop"]:
        quality = np.random.choice(qualities, p=[0.05, 0.45, 0.50])
    elif u_tier == "Super":
        quality = np.random.choice(qualities, p=[0.10, 0.85, 0.05])
    else:
        quality = "SD (480p)" if device == "Mobile Phone" else "HD (1080p)"
        
    # Rating given only by some users (e.g. 25% rating propensity)
    if random.random() < 0.25:
        # High completion implies higher satisfaction
        base_rat = 2.5 + (comp_pct / 100.0) * 2.5
        rating = round(float(np.clip(np.random.normal(base_rat, 0.5), 1.0, 5.0)), 1)
    else:
        rating = None
        
    is_repeat = 1 if (comp_pct > 80.0 and random.random() < 0.18) else 0
    is_first_stream = 1 if (stream_dt - u_signup).days <= 2 else 0
    
    stream_records.append({
        "stream_id": f"STR_{s+1:07d}",
        "user_id": u_id,
        "content_id": c_id,
        "stream_date": stream_dt.strftime("%Y-%m-%d"),
        "date_id": int(stream_dt.strftime("%Y%m%d")),
        "watch_duration_minutes": watch_mins,
        "completion_percentage": comp_pct,
        "device_type": device,
        "network_type": network,
        "playback_quality": quality,
        "user_rating": rating,
        "is_repeat_stream": is_repeat,
        "is_first_stream": is_first_stream
    })

df_streams = pd.DataFrame(stream_records)
print(f"Generated {len(df_streams)} streaming events in fact_streams.")

# ==============================================================================
# 5. SAVE CSV DATASETS
# ==============================================================================
# Save raw/catalog files
df_content.to_csv(os.path.join(RAW_DATA_DIR, "hotstar_content_catalog_raw.csv"), index=False)
df_users.to_csv(os.path.join(RAW_DATA_DIR, "hotstar_users_raw.csv"), index=False)
df_streams.to_csv(os.path.join(RAW_DATA_DIR, "hotstar_streaming_events_raw.csv"), index=False)

# Save processed dimensional star schema files
df_content.to_csv(os.path.join(PROCESSED_DATA_DIR, "dim_content.csv"), index=False)
df_users.to_csv(os.path.join(PROCESSED_DATA_DIR, "dim_users.csv"), index=False)
df_date.to_csv(os.path.join(PROCESSED_DATA_DIR, "dim_date.csv"), index=False)
df_streams.to_csv(os.path.join(PROCESSED_DATA_DIR, "fact_streams.csv"), index=False)

print("\nAll datasets generated and saved successfully!")
print(f"Files saved in {PROCESSED_DATA_DIR}:")
print("1. dim_content.csv")
print("2. dim_users.csv")
print("3. dim_date.csv")
print("4. fact_streams.csv")
