# Reddit Medication Experience Explorer

**Status:** Exploratory, non-commercial, low-volume prototype  
**Purpose:** Evaluate whether Reddit comments in health-related subreddits can provide useful aggregate insights into people’s experiences with specific medications (e.g. effectiveness, side effects, adherence issues).

---

## Overview

This repository contains a small, read-only Python prototype that uses the **Reddit Data API** to:

1. Periodically retrieve **new posts and comments** from a *small set* of health-related subreddits (e.g. condition or medication communities).
2. Store this data in an internal, private dataset.
3. Run **offline natural-language processing (NLP)** models to:
   - Identify which medications are being discussed.
   - Categorise comments into themes such as perceived effectiveness, side effects, access/affordability, etc.
4. Produce **aggregate statistics and topic summaries** (e.g. “X% of comments mentioning Drug Y also mention insomnia”) for feasibility and research purposes.

The goal of this exploratory project is to determine whether Reddit data could be a **useful signal** for understanding real-world perceptions of medicines.  
If the approach proves valuable and we decide to build a commercial product that relies on Reddit data, we understand that this would require a **separate, commercial data agreement** with Reddit.

---

## Scope and behaviour

- **Read-only:**  
  The code only reads data via the Reddit Data API. It does **not** post, comment, send messages, or perform any automated on-platform actions.

- **Limited subreddit set:**  
  Initial experiments focus on a **small pilot list** of health-related subreddits, for example:
  - `r/diabetes`
  - `r/Hypertension`
  - `r/ADHD`
  - `r/depression`
  - `r/AskDocs` (for exploratory analysis of medication-related questions)

  The list is configurable in `config.py` / environment variables.

- **Low frequency:**  
  The crawler is intended to run on a **monthly** cycle, or similarly infrequent schedule. It:
  - Fetches *new* posts since the last run (or within a recent look-back window, e.g. the last 30 days).
  - Fetches comments for a subset of those posts (e.g. posts mentioning specific medications or with sufficient engagement).

- **Aggregate analysis only:**  
  Downstream analysis is focused on **aggregate trends**, such as:
  - Commonly co-mentioned side effects.
  - Distribution of sentiment around a medication.
  - Topics that recur across subreddits.

  Individual comments are not exposed publicly; results are used internally to evaluate feasibility.

---

## Project structure

```text
reddit-medication-explorer/
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ __init__.py
│  ├─ config.py          # Configuration & environment variables
│  ├─ reddit_client.py   # OAuth client wrapper for Reddit API
│  ├─ crawler.py         # Logic to fetch new posts and comments
│  ├─ storage.py         # Simple local JSONL/CSV storage helpers
│  └─ analysis_stub.py   # Placeholder hooks for offline NLP models
└─ scripts/
   └─ run_monthly_crawl.py  # Entry point script for the monthly job
