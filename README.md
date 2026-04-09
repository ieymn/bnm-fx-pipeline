
[README (1).md](https://github.com/user-attachments/files/26347869/README.1.md)
# BNM Data Pipeline

A data engineering portfolio project that extracts financial and economic data from Bank Negara Malaysia's (BNM) public OpenAPI, transforms it using Python and pandas, and loads it into a local SQLite database for SQL analysis.

---

## Architecture

![Architecture](![Architecture](docs/bnm-fx%20architecture.png)

```
BNM OpenAPI → extractor.py → transformer.py → loader.py → SQLite → analysis.sql
```

All steps are orchestrated by `main.py` and scheduled to run daily via cron.

---

## Why this project

I am self-teaching data engineering with the goal of transitioning into a junior DE role. I have a personal interest in forex, stocks, and crypto — so I gravitated toward financial data for this project. BNM publishes free, reliable, well-documented public data that is real and relevant to the Malaysian market, which made it a better learning experience than working with a static toy dataset.

---

## Data sources

All data is pulled from the **BNM OpenAPI** — free, no authentication required.

Base URL: `https://apikijangportal.bnm.gov.my`

| Endpoint | Data | Updates |
|---|---|---|
| `/exchange-rate` | Daily interbank exchange rates (USD, EUR, GBP, SGD, etc.) | Daily |
| `/interest-rate` | OPR, base rates, BLR | On change |
| `/opr` |Official Overnight Policy Rate (Monetary Policy) | On change |
| `/interbank-swap` | Interbank swap volume and rates | Daily |
| `kijang-emas` | Buying and selling prices for gold bullion coins | daily |


---

## Tech stack

| Tool | Purpose | Why |
|---|---|---|
| Python 3.10+ | Pipeline language | Industry standard for data engineering |
| `requests` | Call the BNM API | Simple, reliable HTTP library |
| `pandas` | Clean and transform data | Core DE skill for tabular data |
| `sqlite3` | Local database storage | Built into Python, zero setup, full SQL |
| `cron` | Daily scheduling | Lightweight scheduler for local pipelines |
| Git | Version control | Every project needs this |

---

## Project structure

```
bnm-fx-pipeline/
├── src/
│   ├── extractor.py       # Fetches data from all BNM endpoints
│   ├── transformer.py     # Cleans and validates with pandas
│   └── loader.py          # Writes clean data to SQLite
│   └── backfill.py        # Feteches 1year historical data
├── data/
│   └── bnm.db             # SQLite database (auto-created on first run)
├── analysis/
│   └── analysis.sql       # Business questions answered in SQL
├── docs/
│   └── architecture.png   # Pipeline architecture diagram
├── main.py                # Entry point — runs the full pipeline
├── requirements.txt       # Python dependencies
└── README.md
```

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/ieymn/bnm-fx-pipeline.git
cd bnm-fx-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
python main.py
```

## 4.How to run backfill

To load historical data (run once only):

```bash
cd src
python backfill.py
```

### 5. Schedule daily runs (Linux / macOS)

```bash
crontab -e
# Add this line to run at 9am every day:
0 9 * * * /usr/bin/python3 /path/to/main.py
```

---

## Analysis questions

These are SQL questions I want to explore using this data. Some came from my own curiosity about the Malaysian market, others from researching what kinds of questions financial analysts typically ask of this type of data.

**Interbank swap**

-Which tenure has the highest average transaction volume?
-How has the overnight swap volume trended month by month?

**Interest rate**

-What has the overnight interest rate been over the past year?
-Which months had the highest overnight rate in 2025?

**OPR**

-How many times did the OPR change in 2025?
-What is the trend of OPR levels from 2025 to 2026?

**Kijang Emas**

-What was the highest gold buying price for 1oz in the past year?
-Which gold weight has the highest average profit margin?

---

## Design decisions

**Why BNM and not a global API?**
BNM is a free, stable, public API that requires no authentication. It covers real Malaysian financial data across multiple domains — rates, banking, alerts — which means the pipeline has to handle different data shapes and update frequencies, making it a more realistic learning exercise.

**Why multiple endpoints?**
Real pipelines pull from multiple sources. Using five BNM endpoints means the extractor needs to handle different response structures and the loader needs to write to different tables — closer to what a real DE job involves.

**Why SQLite?**
Zero setup, built into Python, and handles this data volume comfortably. The loader is abstracted so upgrading to PostgreSQL later requires changing one connection string.

**Why separate extract, transform, load scripts?**
Each script has one job. If the transformer breaks, the extractor still works. This modularity makes the pipeline easier to debug, test, and extend.

---

## Roadmap

- [✔] Add historical backfill on first run
- [ ] Add data quality checks (null values, out-of-range rates)
- [ ] Build a simple dashboard from the stored data
- [ ] Migrate to PostgreSQL
- [ ] Replace cron with Apache Airflow DAG
- [ ] Add dbt for transformation layer

---

## Learning context

This project is part of a self-directed data engineering learning path, built for my portfolio

Skills practised: Python, REST APIs, pandas, SQLite, SQL, Git, pipeline design, ETL architecture.

---

## License

MIT
