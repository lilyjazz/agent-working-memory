# Design: SQL Dojo Skill

**Role:** "The Interactive Tutor"
**Goal:** Provision a database and hydrate it with seed data instantly.

## 🏗 Architecture

```mermaid
[Input: --dataset sakila] 
    |
    v
[1. Provisioner] --(curl)--> [TiDB Zero API]
    |
    v
[2. Hydrator] --(pymysql)--> [Read .sql file] -> [Split Statements] -> [Execute]
    |
    v
[Output: JSON] --> { "dsn": "...", "tables": ["actor", "film"] }
```

## ⚠️ Limitations
*   **Split Logic:** Currently splits by `;` which is fragile if data contains semicolons. Future version needs a proper SQL parser.
*   **Data Size:** Large dumps (100MB+) should use `LOAD DATA` or `mytidumper` instead of `INSERT`.
