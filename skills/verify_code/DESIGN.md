# Design: Verify Code Skill

**Role:** The "Self-Correcting Coder"
**Goal:** Provide a safe sandbox for Agents to execute and validate generated SQL before showing it to users.

---

## 🏗 Architecture (Internal)

This skill is a self-contained micro-app (`run.py`) comprising three logical components:

```mermaid
[Input: SQL] 
    |
    v
[1. Provisioner] --(curl)--> [TiDB Zero API]
    |                           |
    | (Returns DSN)             v
    |                    [Ephemeral DB]
    v
[2. Executor] --(pymysql)--> [Connect & Run]
    |                           |
    | (Returns Result/Error)    v
    |                    [Raw Output]
    v
[3. Analyzer]
    |
    +-- Success? -> Format JSON Result
    |
    +-- Failure? -> Parse Error Code -> Generate Suggestion
    |
    v
[Output: JSON]
```

### 1. The Provisioner (Hands)
*   **Mechanism:** Uses system `curl` to call TiDB Zero's unauthenticated API.
*   **Why Curl?** To minimize Python dependencies. We only need standard library `subprocess`.
*   **Fallback:** If provisioning fails, it returns a hard "Infrastructure Error" JSON.

### 2. The Executor (Hands)
*   **Driver:** `pymysql` (Pure Python, easy to install).
*   **Connection Logic:**
    *   Parses standard DSN `mysql://...`.
    *   **Hotfix:** Defaults database to `test` if path is empty (TiDB Zero quirk).
    *   **Security:** Enforces `ssl={"check_hostname": False}` for cloud connections.
*   **Execution:**
    *   Runs raw SQL via `cursor.execute()`.
    *   Auto-commits transactions.

### 3. The Analyzer (Brain)
*   **Responsibility:** Translate raw exceptions into "Agent-Actionable" advice.
*   **Heuristics:**
    *   `Error 1064` (Syntax) -> Suggest: "Check SQL syntax correctness."
    *   `Error 1046` (No DB) -> Suggest: "Try adding 'USE test;'." (Though Executor now handles this).
    *   `Error 8130` (Multi-statement) -> Suggest: "Split queries."

---

## ❤️ The Heart (Protocol)

This skill is useless if the Agent doesn't use it. The `PROTOCOL.md` defines the instinct:

> **Trigger:** Whenever generating SQL (MySQL dialect).
> **Action:** MUST call `verify-code`.
> **Exception:** Skip if user asks for non-MySQL dialects (PG/Oracle).

---

## ⚠️ Limitations & Known Issues

1.  **Single Statement Only:**
    *   TiDB Serverless disables `CLIENT_MULTI_STATEMENTS` by default for security.
    *   *Workaround:* Agent must send DDL (Create) and DML (Insert) in separate calls, or verify logic in blocks.
2.  **Ephemeral Data:**
    *   Data is lost immediately after the script ends (unless DSN is reused, but this script creates a FRESH db every run by default).
    *   *Future:* Add `--keep-alive` flag to output DSN for reuse.

## 🔄 Future Roadmap

*   [ ] **Reuse DSN:** Allow passing an existing DSN (`--dsn`) to verify SQL on a stateful DB.
*   [ ] **Dialect Check:** Regex check input SQL to warn if it looks like PostgreSQL/T-SQL.
