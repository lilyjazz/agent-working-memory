---
name: verify-code
description: "Safely execute and validate SQL code in a disposable TiDB Zero sandbox. Returns execution result or syntax error details. Use this BEFORE showing SQL to users."
---

# Verify SQL Code (Powered by TiDB Zero)

## Goal
To prevent "hallucinated SQL". This skill provisions a temporary database, runs your SQL, and returns the result or error.

## When to use
*   **Always** after generating a complex SQL query.
*   **Always** when the user asks "Test this SQL for me".

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
