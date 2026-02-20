---
name: tidb-sql
description: "Execute SQL on TiDB. Use this skill when you need to: 1) Verify generated SQL code correctness. 2) Analyze structured data using SQL power. 3) Persist state/logs. 4) Perform vector search on text embeddings."
---

# TiDB SQL Executor

## When to Use (Agent Guide)
- **Self-Correction:** Always validate your generated SQL code by running it here before showing it to the user.
- **Data Analysis:** Load user CSVs into a table and use SQL `GROUP BY`/`JOIN` for insights.
- **RAG:** Use `VEC_COSINE_DISTANCE()` for vector search.

## Usage

```bash
python sql_runner.py --dsn "mysql://user:pass@host:4000/db" --sql "SELECT * FROM users LIMIT 5"
```

## Output Format
```json
{
  "status": "success",
  "data": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "row_count": 2
}
```
