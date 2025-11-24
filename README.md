# 📦 Job Scraper Pipeline

**A modular, scalable ETL system for job scraping across Middle East job boards.**
Designed for Data Engineering & Python practice using real-world scraping and pipeline architecture.

---

<p align="center">

  <!-- Build badges -->

  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/Scraping-Polite%20%26%20Modular-green" />
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey" />
  <img src="https://img.shields.io/badge/ETL-Pipeline-orange" />
  <img src="https://img.shields.io/badge/Status-Under%20Active%20Development-yellow" />

</p>

---

# 🚀 Overview

This project is a **production-ready job scraping pipeline** organized into a clean ETL architecture:

**Extract → Transform → Load → Automate**

You can scrape multiple job boards (Wuzzuf, GulfTalent, Bayt, etc.), clean and normalize the data, extract metadata (tags, salary, seniority), dedupe jobs, load into SQLite/CSV, and schedule daily runs.

The entire pipeline is fully modular, configurable, and extendable — every site scraper lives in its own file.

---

# 📂 Project Structure

```
job-scraper/
├── README.md
├── requirements.txt
├── Makefile
├── cli.py
│
├── extract/
│   ├── base_scraper.py
│   ├── wuzzuf.py
│   ├── gulftalent.py
│   ├── naukrigulf.py
│   ├── tanqeeb.py
│   ├── drjobs.py
│   ├── bayt.py
│   ├── laimoon.py
│   ├── akhtaboot.py
│   ├── example_site.py
│   └── utils/
│       ├── fetch.py
│       ├── rate_limit.py
│       ├── parse.py
│       └── logger.py
│
├── transform/
│   ├── normalize.py
│   ├── clean_text.py
│   ├── extract_metadata.py
│   ├── dedupe.py
│   └── text_normalization/
│       ├── arabic.py
│       ├── english.py
│       ├── html.py
│       └── unicode.py
│
├── load/
│   ├── to_csv.py
│   ├── to_sqlite.py
│   ├── to_parquet.py
│   ├── merge.py
│   └── schema.py
│
├── pipeline/
│   ├── runner.py
│   ├── scheduler.py
│   └── validation.py
│
├── core/
│   ├── models.py
│   ├── helpers.py
│   └── exceptions.py
│
├── configs/
│   ├── sites.yml
│   └── rules/
│       ├── salary.yml
│       ├── seniority.yml
│       └── tags.yml
│
├── data/
│   ├── raw/
│   ├── intermediate/
│   ├── processed/
│   └── logs/
│
├── metadata/
│   ├── run_history.json
│   ├── cache/
│   └── mapping/
│
└── scripts/
    └── run_pipeline.sh
```

---

# 🛠 Installation

## 1️⃣ Clone the repo

```bash
git clone https://github.com/husseini2000/job-scraper.git
cd job-scraper
```

## 2️⃣ Create a virtual environment

```bash
python -m venv env
source env/bin/activate        # Mac/Linux
env\Scripts\activate           # Windows
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Or if you're using Poetry:

```bash
poetry install
```

---

# ▶️ Quick Start

### **Run entire ETL pipeline**

```bash
python cli.py run-all
```

### **Run per-stage**

```bash
python cli.py extract
python cli.py transform
python cli.py load
```

### **Scrape one site**

```bash
python cli.py extract --site wuzzuf
```

---

# 🧪 Testing

```bash
pytest -q
```

---

# 🎯 Features

### ✅ Modular scrapers

Each job site has its own Python scraper.

### ✅ Config-driven

Enable/disable sites or adjust rate limits in:

```
configs/sites.yml
```

### ✅ Strong Transform Layer

* HTML & emoji cleaning
* Arabic + English normalization
* Salary extraction
* Seniority detection
* Skill tag extraction (Python, SQL, AWS, Airflow, etc.)
* Duplicate job removal

### ✅ Multiple Load Targets

* CSV
* SQLite
* Parquet

### ✅ Pipeline Automation

Use `pipeline/runner.py` or run via cron using:

```
scripts/run_pipeline.sh
```

---

# 🧭 Roadmap

This project is divided into phases to help build a strong, production-worthy pipeline.

---

## 🧱 **PHASE 0 — Foundation & Environment (1 day)**

**Goal:** Prepare the project structure and development environment.

### Tasks

* Initialise Git repo
* Create the directory structure
* Add `.gitignore`, `requirements.txt`, `pyproject.toml` (optional)
* Setup virtualenv
* Add preliminary `README.md`
* Create `Makefile`

**Output:** Skeleton project.

---

## 🐣 **PHASE 1 — Core Engine & Utilities (2–3 days)**

**Goal:** Create the shared engine for all scrapers.

### Tasks

* Implement utils (fetcher, rate limiter, logger)
* Implement core models and helpers
* Create `configs/sites.yml`

**Output:** Full scraper engine foundation.

---

## 🌐 **PHASE 2 — First Scraper (Wuzzuf) + BaseScraper (3–4 days)**

Build BaseScraper and implement Wuzzuf as the first complete scraper.

**Output:** Working Wuzzuf scraper.

---

## 🧹 **PHASE 3 — Transform Layer (4–5 days)**

Clean, normalize, extract metadata, dedupe.

**Output:** Standardized job objects.

---

## 🛢 **PHASE 4 — Load Layer (2–3 days)**

CSV, SQLite, Parquet, merging, schema.

**Output:** jobs_raw.csv, jobs_clean.csv, jobs.db

---

## 🌍 **PHASE 5 — Additional Scrapers (5–12 days)**

GulfTalent, Tanqeeb, DrJobs, Bayt, NaukriGulf, Laimoon, Akhtaboot.

---

## 🔁 **PHASE 6 — CLI + Pipeline Runner (2–3 days)**

One-command ETL workflow.

---

## 📊 **PHASE 7 — Validation, Logging, Monitoring (1–2 days)**

Add run history, validation, and clear error reporting.

---

## 🚀 **PHASE 8 — Automation & Deployment (1 day)**

Cron job automation + final polish.

---

# ❤️ Contributing

Pull requests are welcome.
If you're scrapers for additional job sites, follow the `example_site.py` template.

---

# 📜 License

MIT License.

---
