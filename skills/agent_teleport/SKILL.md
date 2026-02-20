# Agent Teleport (Powered by TiDB Zero)

## Goal
To migrate the Agent's configuration and memory to a new machine seamlessly.

## Usage
*   **Pack (Old Machine):** `python run.py --action pack` -> Returns DSN.
*   **Restore (New Machine):** `python run.py --action restore --dsn "..."`
