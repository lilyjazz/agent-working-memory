---
name: verify-code
description: "Safely execute and validate SQL code in a disposable TiDB Zero sandbox. Returns execution result or syntax error details. Use this BEFORE showing SQL to users."
---

# Verify SQL Code (Powered by TiDB Zero)

## Goal
To prevent "hallucinated SQL". This skill provisions a temporary database, runs your SQL, and returns the result or error.

## 📥 Installation

### 1. Add to `TOOLS.md`
Add the following block to your agent's tool definitions:

```markdown
- **verify-code**: Verify SQL correctness using TiDB Zero.
  - **Location:** `/path/to/skills/verify_code/SKILL.md`
  - **Command:** `python /path/to/skills/verify_code/run.py --sql "<QUERY>"`
```

### 2. Add to `AGENTS.md` (Mandatory Protocol)
Copy the content of [PROTOCOL.md](PROTOCOL.md) into your agent's system prompt or operational protocols section. This ensures the agent *automatically* uses this skill.

## Usage (Standalone)

```bash
# Set env var if needed (optional)
export TIDB0_INVITATION_CODE="xxx" 

# Run verification
python run.py --sql "CREATE TABLE test (id INT); INSERT INTO test VALUES (1);"
```

## Output Format (JSON)

**Success:**
```json
{
  "verified": true,
  "result": { ...rows... },
  "infrastructure": "TiDB Cloud Zero"
}
```

**Failure:**
```json
{
  "verified": false,
  "error": "Error 1064: You have an error in your SQL syntax...",
  "fix_suggestion": "Check line 1 near...",
  "infrastructure": "TiDB Cloud Zero"
}
```
