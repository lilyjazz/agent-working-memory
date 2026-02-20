# Design: Data Refinery Skill

**Role:** "The Excel Killer" / "Data Laundromat"
**Goal:** Ingest local files (CSV/Excel) into a temporary TiDB database, enabling the Agent to use SQL for complex cleaning and analysis.

---

## 🏗 Architecture

```mermaid
[Input: file.csv] 
    |
    v
[1. Analyzer (Pandas)] --> (Infers Schema: "id:INT, name:VARCHAR")
    |
    v
[2. Provisioner] --(curl)--> [TiDB Zero API]
    |
    v
[3. Loader (SQL)] --(INSERT/LOAD)--> [Create Table & Ingest]
    |
    v
[Output: JSON] --> { "dsn": "...", "table": "file_csv", "rows": 100 }
```

### 1. The Analyzer (Brain)
*   **Library:** `pandas`
*   **Logic:**
    *   Read file (head only for large files? No, we need full ingest).
    *   Clean column names (replace spaces with `_`, lowercase).
    *   Map `dtype` to SQL Type:
        *   `int64` -> `BIGINT`
        *   `float64` -> `DOUBLE`
        *   `datetime64` -> `DATETIME`
        *   `object` -> `TEXT` (safest)

### 2. The Provisioner (Hands)
*   Reuses `tidb-zero` curl logic (embedded).

### 3. The Loader (Hands)
*   **Method:** Batch `INSERT` (Simpler than `LOAD DATA LOCAL INFILE` due to cloud restrictions/driver flags).
*   **Batch Size:** 1000 rows per chunk.

---

## ❤️ The Heart (Protocol)

> **Trigger:** When user provides a file > 50 rows or asks for complex filtering.
> **Action:** Load into DB using `data-refinery`.
> **Reasoning:** Don't use Python string processing. Use SQL.

---

## ⚠️ Limitations

1.  **File Size:** Limited by Agent memory (since Pandas reads into memory). For huge files, we'd need a streaming reader. MVP uses Pandas.
2.  **Network:** Uploading 10MB+ might be slow via single-thread INSERT.
