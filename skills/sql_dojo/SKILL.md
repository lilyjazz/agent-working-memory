# SQL Dojo (Powered by TiDB Zero)

## Goal
To provide a sandbox database pre-loaded with classic datasets (like Sakila) for users to practice SQL or for the Agent to demonstrate queries.

## 📥 Installation

### 1. Add to `TOOLS.md`
```markdown
- **sql-dojo**: Provision a practice database with sample data.
  - **Location:** `/path/to/skills/sql_dojo/SKILL.md`
  - **Command:** `python /path/to/skills/sql_dojo/run.py --dataset mini_sakila`
```

### 2. Add to `AGENTS.md` (Protocol)
Copy [PROTOCOL.md](PROTOCOL.md) to your agent's system prompt.

## Output Format
Returns a JSON with `dsn` and schema info.
