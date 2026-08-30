# NHL Analytics Pipeline

Portfolio ELT project: NHL API → Snowflake (native ingestion) → dbt (silver/gold) → Streamlit.

## Current state

Local dev only. Ingestion runs as a Snowflake stored procedure (Python,
calling the NHL API through an External Access Integration), deployed and
run against `DEV` by hand. QAT/PRD and CI/CD come later, once this works
end to end.

Infra setup (warehouses, resource monitor, databases/schemas, RBAC roles,
network rule/external access integration, stages) lives only in Snowflake
worksheets — not in this repo.

## Setup

### 1. GitHub — create the repo

1. github.com → **New repository** → `nhl-analytics-pipeline` → Create.
2. Don't add a README/gitignore in the GitHub UI — already in this starter.

### 2. VS Code — get this code into that repo

1. Unzip this project, open the folder in VS Code (**File → Open Folder**).
2. **Source Control** panel (`Ctrl+Shift+G`) → **Initialize Repository**.
3. Stage all files, write a commit message, click the commit checkmark.
4. **Publish Branch** → sign in to GitHub if prompted → select/create the repo.
5. From then on: edit → Source Control panel → commit → **Sync Changes**.

### 3. Python environment

Terminal → New Terminal in VS Code:

```
python -m venv .venv
```

Select it as your interpreter (VS Code will usually prompt you). Then:

```
pip install -r requirements.txt
```

### 4. Credentials

1. Copy `.env.example` to `.env`.
2. Fill in `SNOWFLAKE_ACCOUNT` and `SNOWFLAKE_USER` (your own username).
   `SNOWFLAKE_ROLE` and `SNOWFLAKE_WAREHOUSE` are already set correctly.
3. No password — browser auth will pop a login window on first connect.

## Deploy and test

From `ingestion/stored_procs/`:

```
python deploy.py
```

This uploads `load_schedule_proc.py` to `DEV.RAW.INGESTION_STAGE` and
(re)creates `DEV.RAW.LOAD_SCHEDULE`. A browser window opens for SSO the
first time — log in once.

Then in a Snowflake worksheet (as `NHL_DEVELOPER`):

```sql
CALL RAW.LOAD_SCHEDULE('EDM', '20242025');
SELECT * FROM RAW.SCHEDULE;
```

You should see one row with the full season's JSON payload. Try
`raw_json:games[0]:id` to confirm you can query into it.

## Project structure

```
nhl-analytics-pipeline/
├── ingestion/
│   └── stored_procs/
│       ├── load_schedule_proc.py   # the stored proc source
│       └── deploy.py               # stages + (re)creates the proc in DEV
├── requirements.txt
├── .env.example
└── .gitignore
```

## What's next

- Loop across all 32 teams instead of one
- Bronze flatten (Stream + Task + MERGE)
- Stand up `NHL_CI_CD` (key-pair auth), then QAT/PRD deploy via GitHub Actions
- dbt project scaffold (staging + marts)
