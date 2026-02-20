# TiDB Agent Skills: Design & Technical Roadmap

**Strategy:** Build standalone, self-contained skills.
Each skill folder (e.g., `skills/verify_code/`) is a complete micro-app with its own entry point (`run.py`), dependencies (`requirements.txt`), and documentation (`SKILL.md`).

---

## 📦 Skill Package Specification (SPS)

To ensure modularity and ease of use, every skill directory (`skills/<name>/`) **MUST** adhere to the following structure. We call this the **"Four Pillars"** standard.

| File | Metaphor | Audience | Purpose & Requirement |
| :--- | :--- | :--- | :--- |
| **`run.py`** | **The Hands** (手) | Runtime | **Execution Logic.** <br>• Must be a standalone Python script.<br>• Must output strict JSON to stdout.<br>• Must contain embedded provisioning logic (no external shared libs). |
| **`SKILL.md`** | **The Brain** (脑) | Agent (Tool) | **Capability Definition.** <br>• Describes *what* the tool does.<br>• Provides CLI usage examples.<br>• Content is meant to be copied into the Agent's `TOOLS.md`. |
| **`PROTOCOL.md`** | **The Heart** (心) | Agent (Prompt) | **Behavioral Trigger.** <br>• Describes *when* and *why* to use the tool.<br>• Content is meant to be injected into the Agent's `AGENTS.md` (System Prompt) to create autonomous instincts. |
| **`DESIGN.md`** | **The Soul** (魂) | Developer | **Architecture & Maintainability.** <br>• Explains internal logic, architecture diagrams, and limitations.<br>• Helps human contributors understand the code. |

### Optional Files
*   `requirements.txt`: Python dependencies (e.g., `pymysql`, `pandas`).
*   `test_*.py`: Local unit tests (if complex).

---

## 🏗 System Architecture: The "Body-Mind-Heart" Model

To make a Skill truly useful to an autonomous Agent, it needs three parts:

| Component | Metaphor | File | Purpose |
| :--- | :--- | :--- | :--- |
| **Code** | **Hands (手)** | `run.py` | **Execution.** The Python logic that calls APIs (TiDB Zero) and runs SQL. It must be robust, self-contained, and output strict JSON. |
| **Definition** | **Brain (脑)** | `SKILL.md` | **Knowledge.** Defines *what* the tool is and *how* to call it. This goes into the Agent's `TOOLS.md`. |
| **Protocol** | **Heart (心)** | `PROTOCOL.md` | **Instinct.** Defines *when* and *why* to use it. This goes into the Agent's `AGENTS.md` (System Prompt) to trigger autonomous behavior. |

---

## 🛠 Component Design

### Level 0: The Primitives (Embedded)
Primitives (provisioning, SQL execution) are embedded per skill to ensure zero external dependencies.

### Level 1: The Skills (Orchestrators)
These are the distributable units.

#### 1. `verify_code` (The Self-Correcting Coder)
*   **Hands:** Provisions DB, runs single-statement SQL, captures errors.
*   **Brain:** Tool to verify SQL correctness.
*   **Heart:** "Always verify generated SQL before showing it."

#### 2. `data_refinery` (The Data Analyst) - *New!*
*   **Hands (`run.py`):**
    *   Input: Local file path (CSV/Excel).
    *   Logic: Pandas read -> Schema Inference -> `CREATE TABLE` -> Batch `INSERT` -> Return DSN + Table Name.
*   **Brain (`SKILL.md`):** Tool to turn static files into queryable SQL tables.
*   **Heart (`PROTOCOL.md`):** "When handling data files >50 rows, ALWAYS load into DB first instead of processing in-memory."

---

## 📅 Roadmap: Delivering the 15 Superpowers

### Phase 1: The Foundation (Current Status: ✅)
*   [x] **Project Structure:** `agent-working-memory/` created.
*   [x] **Skill 1: `verify_code`** (Standalone) ready & verified.
*   [x] **Testing:** Unit + Integration + Agent Simulation.

### Phase 2: The Data Analyst (Next Steps)
*Focus on Business Users.*
*   [ ] **Skill 2: `data_refinery`**
    *   **Goal:** Upload CSV -> SQL Table.
    *   **Dependencies:** `pandas`, `openpyxl`.
    *   **Challenge:** Reliable type inference & fast insertion.

### Phase 3: The "Wow" MVP
*   [ ] **Skill 7: `sql_dojo`** (SQL Tutor)
    *   Script to pre-load a sample dataset (e.g., *Sakila* or *Northwind*) upon creation.

### Phase 4: The Cloud Native Agent
*Focus on Agent Persistence.*
*   [ ] **Skill 11: `agent_teleport`**
    *   Script to dump Workspace -> SQL Insert.
*   [ ] **Skill 13: `black_box`**
    *   Logging adapter for OpenClaw.

---

## 🛡️ Testing Standard (Definition of Done)

Every Skill **MUST** include a Live End-to-End (E2E) Test (`tests/integration/test_<skill_name>.py`) that proves the capability works in the real world.

**E2E Test Checklist:**
1.  **Real Infrastructure:** Must provision a real TiDB Zero instance (no mocks).
2.  **Real Scenario:** Must execute the core user story (e.g., "Load CSV", "Vector Search").
3.  **Self-Checking:** Must assert that the output JSON is valid and correct.
