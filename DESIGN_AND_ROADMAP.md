# TiDB Agent Skills: Design & Technical Roadmap

**Strategy:** Build standalone, self-contained skills.
Each skill folder (e.g., `skills/verify-code/`) is a complete micro-app with its own entry point (`run.py`), dependencies (`requirements.txt`), and documentation (`SKILL.md`).

---

## 🏗 System Architecture: The "Body-Mind-Heart" Model

To make a Skill truly useful to an autonomous Agent, it needs three parts:

| Component | Metaphor | File | Purpose |
| :--- | :--- | :--- | :--- |
| **Code** | **Hands (手)** | `run.py` | **Execution.** The Python logic that calls APIs (TiDB Zero) and runs SQL. It must be robust, self-contained, and output strict JSON. |
| **Definition** | **Brain (脑)** | `SKILL.md` | **Knowledge.** Defines *what* the tool is and *how* to call it. This goes into the Agent's `TOOLS.md`. |
| **Protocol** | **Heart (心)** | `PROTOCOL.md` | **Instinct.** Defines *when* and *why* to use it. This goes into the Agent's `AGENTS.md` (System Prompt) to trigger autonomous behavior (e.g., "Always verify SQL"). |

```mermaid
[Agent]
   |
   +-- (Heart) Instinct: "I must verify this SQL." (Reads AGENTS.md)
   |
   +-- (Brain) Knowledge: "I have a tool for that." (Reads TOOLS.md)
   |
   +-- (Hands) Action: Calls `python run.py`
         |
         +-- Provisions TiDB Zero -> Runs SQL -> Returns JSON
```

---

## 🛡️ Testing Standard (Definition of Done)

Every Skill **MUST** include:
1.  **Unit Tests:** `tests/unit/` (Mocked network).
2.  **Live Tests:** `tests/integration/` (Real TiDB connection).
3.  **Agent Simulation:** `tests/e2e_agent_simulation.md` (A script to verify the Agent *autonomously* uses the skill).

---

## 🛠 Component Design

### Level 0: The Primitives (Embedded)
Instead of shared libraries, primitive logic (provisioning via curl, SQL execution via pymysql) is embedded or vendored into each Skill's `run.py` to ensure zero external dependencies.

*   **Provisioner:** Embedded `create_temp_db()` function using `curl`.
*   **Executor:** Embedded `run_sql()` function using `pymysql`.

### Level 1: The Skills (Orchestrators)
These are the distributable units.

*   **`verify-code`**:
    *   Logic: Create DB -> Run SQL -> if error return suggestion -> else return sample data.
*   **`data-refinery`**:
    *   Logic: Create DB -> Generate CREATE TABLE from CSV header -> LOAD DATA -> Run cleaning SQL.

---

## 🛡️ Testing Standard (Definition of Done)

Every Skill **MUST** include a Live End-to-End (E2E) Test (`tests/integration/test_<skill_name>.py`) that proves the capability works in the real world.

**E2E Test Checklist:**
1.  **Real Infrastructure:** Must provision a real TiDB Zero instance (no mocks).
2.  **Real Scenario:** Must execute the core user story (e.g., "Load CSV", "Vector Search").
3.  **Self-Checking:** Must assert that the output JSON is valid and correct.

*Example flow for `data-refinery`:*
> Generate CSV -> Provision DB -> Run Skill -> Query DB to verify data is clean -> Pass.

---

## 📅 Roadmap: Delivering the 15 Superpowers

### Phase 1: The Foundation (Current Status: ✅)
*   [x] **Project Structure:** `tidb-zero-project/` created.
*   [x] **Skill 1: `verify-code`** (Standalone) ready & verified.
    *   Contains embedded provisioner and executor.

### Phase 2: The "Wow" MVP (Next Steps)
*Focus on the most impressive capabilities for Developers.*
*   [ ] **Skill 7: `sql-dojo`** (SQL Tutor)
    *   Script to pre-load a sample dataset (e.g., *Sakila* or *Northwind*) upon creation.

### Phase 3: The Data Analyst
*Focus on Business Users.*
*   [ ] **Skill 3: `data-refinery`**
    *   Build `csv_to_sql.py` loader.
*   [ ] **Skill 8: `data-diff`**
    *   Logic to compare two tables via SQL `EXCEPT`.
