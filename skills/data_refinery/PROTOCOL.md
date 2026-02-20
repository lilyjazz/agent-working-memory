### 2. Large Data Handling (Data Refinery)
*   **Trigger:** When the user provides a data file (CSV, Excel, JSON) or asks for data analysis on a file.
*   **Threshold:** If the file has > 50 rows or the user asks for complex filtering/aggregation (e.g., "Find top 10", "Join with X").
*   **Action:** You **MUST** use `data-refinery` to load the data into a database first.
*   **Prohibition:** Do NOT try to parse the file text directly in the prompt or use simple Python string splitting. Use SQL power.
*   **Flow:**
    1.  Call `data-refinery` with the file path.
    2.  Get the DSN and Table Name.
    3.  Call `verify-code` (or use internal SQL executor) to run queries on that table to answer the user's question.
