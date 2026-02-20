# TiDB Agent Skills: Design & Technical Roadmap

**Strategy:** Build standalone, self-contained skills.
Each skill folder (e.g., `skills/verify-code/`) is a complete micro-app with its own entry point (`run.py`), dependencies (`requirements.txt`), and documentation (`SKILL.md`).

---

## 🏗 System Architecture (Standalone Model)

```text
tidb-zero-project/
├── skills/
│   ├── verify-code/      # [Standalone Unit]
│   │   ├── SKILL.md      # User Manual
│   │   ├── run.py        # Logic (Provisions + Executes)
│   │   └── requirements.txt
│   │
│   ├── data-refinery/    # [Standalone Unit]
│   │   ├── SKILL.md
│   │   ├── run.py
│   │   └── requirements.txt
│   │
│   └── ...
```

This architecture allows:
1.  **Independent Distribution:** Users can grab just one folder.
2.  **Zero Coupling:** Changes in `verify-code` don't break `data-refinery`.
3.  **Simple Integration:** Agent just needs to run `python skills/<name>/run.py`.

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
