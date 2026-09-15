# NHL Measurement Dashboard

Hockey is a fantastic sport. But, true hockey nerds know that there is a statistics problem. Traditional stats like assists, plus/minus, etc can't tell the full story of a game. Well, I don't intend to solve that problem.

What I do intend with this project is to connect this data with completely unrelated statistical data. You may know how many "miles per hour" Connor McDavid skates, but what about "lengths of a Honda Civic per hour"? How many "goals per shark attack" has Ovechkin scored in his career? Which player has the largest prime number of assists?

This project won't solve hockey's data problem, but it will show how technical data skills combined with bad questions can give useless - albeit entertaining - results.

## Stack

Portfolio ELT project: NHL API → Snowflake Openflow (native ingestion) → dbt (bronze/silver/gold) → Streamlit.

## Current state

Ingestion occurs in Snowflake Openflow. This lands raw json in the RAW layer of the database, which can then 
be transformed using dbt. The dbt jobs live in the Git repo. Snowflake has a native dbt object which references the repo for the source-of-truth.

This allows the scheduling of ingestion and transformation (Openflow/dbt) to happen in a single orchestration stored procedure, called by a single task. 
This is a simple and scalable solution as the project grows.

Infra setup (warehouses, resource monitor, databases/schemas, RBAC roles,network rule/external access integration, stages) lives only in Snowflake
worksheets — not in this repo.

CI/CD for dbt is handled via Github workflows. This allows for version control and test builds prior to production deployments. 

## Project structure

```
NHL-Measurement-Dashboard/          ← repo root
├── .github/
│   └── workflows/
│       ├── deploy_qat.yml
│       └── deploy_prd.yml
├── nhl_dbt/
│   ├── models/
│   ├── dbt_project.yml
│   └── ...
├── README.md
└── .gitignore
```

## What's next

Snowflake/dbt
- continued build out of the raw layer (player, team, boxscore)
- additional dbt models to transform the raw data
- metric labeling (distance, time, unit)
- addition of non-hockey statistics

Streamlit
- provide an interface for users to view the data
- hosting
