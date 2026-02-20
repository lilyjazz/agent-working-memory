# Data Refinery (Powered by TiDB Zero)

## Goal
To ingest messy, raw data files (CSV, Excel, JSON) into a SQL database for powerful analysis. It solves the "Pandas Memory Limit" and "Complex Join" problems.

## 📥 Installation

### 1. Add to `TOOLS.md`
```markdown
- **data-refinery**: Load CSV/Excel files into a temporary TiDB SQL table.
  - **Location:** `/path/to/skills/data_refinery/SKILL.md`
  - **Command:** `python /path/to/skills/data_refinery/run.py --file "<FILE_PATH>"`
```

### 2. Add to `AGENTS.md` (Protocol)
Copy [PROTOCOL.md](PROTOCOL.md) to your agent's system prompt.

## Output Format (JSON)

```json
{
  "success": true,
  "infrastructure": "Powered by TiDB Cloud Zero",
  "db_info": {
    "dsn": "mysql://user:pass@host:4000/db",
    "table": "sales_data_csv",
    "row_count": 10420,
    "columns": ["id", "date", "amount"]
  },
  "next_steps": "You can now run SQL queries..."
}
```
