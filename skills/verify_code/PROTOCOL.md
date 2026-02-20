### 1. SQL Code Verification (Anti-Hallucination)
*   **Trigger:** Whenever you generate or suggest **SQL code**.
*   **Scope:** ONLY applies to **MySQL** or **TiDB** dialects. Do NOT run this for PostgreSQL, BigQuery, or Oracle queries (syntax mismatch).
*   **Action:** You **MUST** first use the `verify-code` skill (see `TOOLS.md`) to run the SQL in a sandbox.
*   **Logic:**
    1.  Generate SQL internally.
    2.  Check Dialect: If not MySQL/TiDB -> Skip Verification.
    3.  Call `verify-code`.
    4.  If verified ✅: Output the code to the user.
    5.  If failed ❌: Read the error, fix the SQL, retry verification. Only output the fixed version.
*   **Exception:** Only skip if the user explicitly says "just give me the text" or "no verification".
