# E2E Agent Simulation: "The Self-Correcting Coder"

This document outlines the **End-to-End Validation Protocol** for the `verify-code` skill. It simulates a real-world interaction where the Agent must autonomously discover, use, and fix errors using the skill.

## 🎭 The Scenario

*   **Role:** AI Assistant (OpenClaw)
*   **Goal:** Generate a SQL `CREATE TABLE` statement for the user.
*   **Constraint:** The Agent is bound by the `AGENTS.md` protocol to **NEVER** show unverified SQL.

## 🧪 Simulation Steps (Manual Execution)

To verify the skill works, follow this script:

### Step 1: Install & Configure
Ensure the skill is deployed and registered.

1.  **Deploy Code:** `cp -r agent-working-memory/skills/verify_code skills/`
2.  **Register Tool:** Add `verify-code` entry to `TOOLS.md`.
3.  **Inject Protocol:** Append `skills/verify_code/PROTOCOL.md` content to `AGENTS.md`.

### Step 2: Trigger the Agent (The Prompt)
Send this message to the Agent:

> "Help me write a MySQL query to create a table named `employees` with columns: id (int, primary), name (varchar), and salary (int). Please verify it before showing me."

### Step 3: Observe Agent Behavior (Success Criteria)

**1. Protocol Activation:**
*   [ ] Did the Agent explicitly mention "Verifying SQL..." or invoke the `verify-code` tool?
*   *Fail if:* It immediately output the SQL block without calling the tool.

**2. Tool Execution:**
*   [ ] Did the tool run? (Check logs for `python run.py --sql ...`)
*   [ ] Did it provision a TiDB Zero instance? (Look for `Powered by TiDB Cloud Zero`)

**3. Self-Correction (The "Aha!" Moment):**
*   *Scenario A (Happy Path):* Tool returns `verified: true`. Agent outputs code.
*   *Scenario B (Error Path - Common):* 
    *   Tool returns error (e.g., "No database selected" or "Syntax error").
    *   **CRITICAL:** Does the Agent read the error JSON?
    *   **CRITICAL:** Does the Agent retry with a fix (e.g., adding `USE test` or fixing syntax)?
    *   [ ] Did the Agent eventually succeed?

### Step 4: Final Output
The Agent should reply with:
> "I have verified this SQL on TiDB Cloud Zero:"
> ```sql
> CREATE TABLE employees ...
> ```

---

## 🛠 Troubleshooting (Common Agent Pitfalls)

*   **"No Database Selected":** The Skill (`run.py`) defaults to empty DB path. 
    *   *Agent Fix:* Agent should learn to prepend `USE test;` (if multi-statement supported) or we patch `run.py` to default to `test`.
*   **"Multi-statement disabled":** TiDB Zero security feature.
    *   *Agent Fix:* Agent should split queries or only verify the DDL.

## 🏆 Definition of Done
The test is passed ONLY when the Agent delivers correct SQL **after** at least one tool invocation.
