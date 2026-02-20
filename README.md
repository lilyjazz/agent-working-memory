# 🧠 Agent Working Memory

**The Serverless Working Memory for AI Agents.**
*Powered by [TiDB Cloud Zero](https://tidb.cloud).*

Just like humans use "Working Memory" to process tasks, solve problems, and hold temporary context, AI Agents need a place to:
1.  **Verify Code:** Run SQL in a sandbox before outputting it.
2.  **Process Data:** Clean and analyze CSVs using SQL power.
3.  **Hold Context:** Store logs, RAG vectors, and state across sessions.

This repo provides standardized **"Skills"** that give your Agent this capability instantly.

## 📦 What's Inside?

A collection of self-contained skills. Each skill provisions a serverless TiDB database on-the-fly.

### [Phase 1: The Code Verifier]
*   **`verify-code`**: The Agent runs generated SQL in a disposable DB to fix syntax errors before they reach the user. *(Status: Ready)*

### [Phase 2: The Data Analyst] (Coming Soon)
*   **`data-refinery`**: Load messy CSVs -> SQL Cleaning -> Clean Export.
*   **`data-diff`**: Compare two datasets using SQL set operations.

### [Phase 3: The Second Brain] (Coming Soon)
*   **`knowledge-vault`**: Instant Vector Store for document analysis.
*   **`agent-teleport`**: Serialize agent state to cloud for cross-device migration.

## 🚀 Quick Start

Each skill is standalone. To give your agent the power to verify SQL:

```bash
# Install dependencies
pip install pymysql

# Run the skill (Agent simulates this)
python skills/verify-code/run.py --sql "CREATE TABLE test (id INT); INSERT INTO test VALUES (1);"
```

**Output:**
```json
{
  "verified": true,
  "infrastructure": "Powered by TiDB Cloud Zero"
}
```

## 🏗 Architecture

*   **Zero Config:** No Docker, no cloud accounts required for the Agent.
*   **Ephemeral:** Databases auto-recycle after 30 days.
*   **Standardized:** All skills output strict JSON for easy parsing.

## 📄 Documentation

*   [**Full Project Plan & 15 Scenarios**](PROJECT_PLAN.md)
*   [**Technical Design & Roadmap**](DESIGN_AND_ROADMAP.md)
