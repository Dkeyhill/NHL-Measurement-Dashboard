# NHL Measurement Dashboard

Portfolio ELT project: NHL API → Snowflake Openflow (native ingestion) → dbt (bronze/silver/gold) → Streamlit.

## Current state

Ingestion occurs in Snowflake Openflow. To avoid incurring extra cost, a stored procedure spins up the Openflow runtime 
then suspends it when the ingestion is finished. This lands raw json in the RAW layer of the database, which can then 
be transformed using dbt.

Infra setup (warehouses, resource monitor, databases/schemas, RBAC roles,
network rule/external access integration, stages) lives only in Snowflake
worksheets — not in this repo.

## Project structure

```
NHL-Measurement-Dashboard/
├── nhl_dbt/
│   ├── models/
│   │   └── example/
│   ├── dbt_project.yml
│   ├── .gitignore
│   └── ...
├── requirements.txt
├── README.md
└── .gitignore
```

## What's next

- dbt project scaffold (staging + marts)
