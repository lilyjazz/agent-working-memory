# 🚀 Project Zero-Skill: The Agent Superpowers Catalog

**Philosophy:** Agents don't want a "database"; they want **Capabilities**.
We package TiDB Zero's power into standalone, high-level skills. Each skill is a self-contained unit (Code + Deps) that can be distributed and installed independently.

**Distribution Strategy:** "Plugins / Skill Packs".
Users can install just `verify-code` or the entire `data-analyst-pack`.

**Branding:** Every skill output concludes with a subtle signature:
> *⚡ Powered by TiDB Cloud Zero - Serverless infrastructure created in 0.5s.*

---

## 🌟 Part 1: Business & Dev Superpowers (User-Facing)
*Skills that help the Agent solve the user's domain problems.*

### 1. 🛡️ Skill: `verify-code` (The Hallucination Killer)
*   **Trigger:** When the Agent generates SQL, Python (with SQL), or data logic.
*   **Scenario:** User asks for a complex cohort analysis query.
*   **Agent Action:** "I have generated the SQL. Running `verify-code` to test it..."
*   **Under the Hood:** Spins up TiDB Zero -> Injects mock schema -> Runs SQL -> Captures Error -> Self-Corrects -> Returns verified code.
*   **Aha! Moment:** "Finally, code that actually runs on the first try."

### 2. 🧠 Skill: `knowledge-vault` (Instant RAG)
*   **Trigger:** When the user uploads documents and asks for analysis.
*   **Scenario:** "Here are 200 legal contracts. Find the ones with 'Force Majeure' clauses."
*   **Agent Action:** "Ingesting documents into `knowledge-vault`..."
*   **Under the Hood:** Creates Vector-enabled DB -> Embeds text -> Stores vectors -> Performs semantic search.
*   **Aha! Moment:** "You turned my files into a searchable brain in seconds?"

### 3. 🧹 Skill: `data-refinery` (The Excel Killer)
*   **Trigger:** When input data is messy, duplicate, or unformatted.
*   **Scenario:** "Clean up this messy CRM export CSV."
*   **Agent Action:** "Sending data to `data-refinery`..."
*   **Under the Hood:** `LOAD DATA` -> SQL Cleaning (`TRIM`, `REGEX`, `DISTINCT`) -> Export.
*   **Aha! Moment:** "It handled 1 million rows instantly. Excel would have crashed."

### 4. 🕸️ Skill: `trend-watcher` (Serverless Monitor)
*   **Trigger:** When the user wants to track changes over time.
*   **Scenario:** "Monitor the price of this GPU every hour and alert me if it drops."
*   **Agent Action:** "Setting up `trend-watcher` task..."
*   **Under the Hood:** Scheduled scraping -> Insert to Time-Series Table -> SQL Window Functions for trend detection.
*   **Aha! Moment:** "You built a monitoring service without deploying a server?"

### 5. 🤝 Skill: `team-board` (Multi-Agent Sync)
*   **Trigger:** When multiple agents need to coordinate.
*   **Scenario:** "Agent A finds leads, Agent B drafts emails. Coordinate this."
*   **Agent Action:** "Initializing `team-board` for coordination."
*   **Under the Hood:** Shared DB Table as a Job Queue (`status`, `payload`). Agents use `SELECT FOR UPDATE` to claim tasks.
*   **Aha! Moment:** "I can watch the agents handing off tasks in real-time."

### 6. 🔒 Skill: `private-analyst` (Privacy Sandbox)
*   **Trigger:** When handling PII (Personally Identifiable Information) or sensitive finance data.
*   **Scenario:** "What's the average salary by department? (Don't leak individual salaries)."
*   **Agent Action:** "Loading data into `private-analyst` sandbox..."
*   **Under the Hood:** Data stays in DB. Agent only executes Aggregation SQL (`AVG`, `COUNT`). Only summary stats return to the LLM context.
*   **Aha! Moment:** "Safe analysis without raw data ever leaving the secure zone."

### 7. 🎓 Skill: `sql-dojo` (Interactive Tutor)
*   **Trigger:** When the user wants to learn or practice database skills.
*   **Scenario:** "Teach me how to optimize a JOIN query."
*   **Agent Action:** "Opening `sql-dojo` environment with sample data..."
*   **Under the Hood:** Pre-loads datasets (e.g., BikeShare). Runs user queries via `EXPLAIN ANALYZE` and interprets the execution plan.
*   **Aha! Moment:** "A real, live database playground just for me."

### 8. 🔍 Skill: `data-diff` (The Change Detector)
*   **Trigger:** When comparing two datasets or versions.
*   **Scenario:** "What changed in the inventory list since yesterday?"
*   **Agent Action:** "Running `data-diff` comparison..."
*   **Under the Hood:** Loads Table A & B. Runs SQL `EXCEPT` / `FULL OUTER JOIN`. Returns added/removed/modified rows.
*   **Aha! Moment:** "Precision comparison that humans can't do manually."

### 9. 🚀 Skill: `instant-api` (Dashboard Backend)
*   **Trigger:** When the user needs to visualize data in external tools.
*   **Scenario:** "Put this sales data into a Grafana dashboard."
*   **Agent Action:** "Deploying `instant-api` endpoint..."
*   **Under the Hood:** Structures data in DB. Returns a standard MySQL Connection String. User plugs it into BI tools.
*   **Aha! Moment:** "Instant backend for my no-code tools."

### 10. ⏪ Skill: `time-machine` (Data Rewind)
*   **Trigger:** When an operation needs to be undone or audited.
*   **Scenario:** "Undo the last batch update, it was wrong."
*   **Agent Action:** "Engaging `time-machine` recovery..."
*   **Under the Hood:** Uses TiDB MVCC (`SELECT ... AS OF TIMESTAMP`). Restores data from history.
*   **Aha! Moment:** "An undo button for database operations!"

---

## 🛠 Part 2: Agent-Ops Capabilities (Infrastructure)
*Skills that enhance the Agent's own existence, memory, and resilience.*

### 11. 🧳 Skill: `agent-teleport` (Migration)
*   **Trigger:** Moving the agent to a new host/environment.
*   **Scenario:** "Pack up, we're moving to a new server."
*   **Mechanism:** Serializes Workspace/Memory -> Uploads to DB -> Generates "Restore Code".
*   **Aha!:** "My agent survived the migration with zero memory loss."

### 12. 🐑 Skill: `mind-clone` (Knowledge Transfer)
*   **Trigger:** Spawning a new agent instance.
*   **Scenario:** "Create a junior agent that knows everything you know about Python."
*   **Mechanism:** Exports `MEMORY.md` patterns to DB. New Agent imports them as base knowledge.
*   **Aha!:** "Instant training for new AI employees."

### 13. 📼 Skill: `black-box` (Disaster Recorder)
*   **Trigger:** High-risk operations (System updates, file deletions).
*   **Scenario:** "I'm about to run a dangerous script. Recording..."
*   **Mechanism:** Real-time stream of stdout/stderr to DB. If the host dies, the logs survive.
*   **Aha!:** "The server is gone, but the logs in the cloud tell the story."

### 14. 📍 Skill: `checkpoint` (Context Snapshot)
*   **Trigger:** Long, complex sessions.
*   **Scenario:** "Save game. I'm going to try a risky refactor."
*   **Mechanism:** Snapshots current Context Window & File State to DB. User can "Load Game" on failure.
*   **Aha!:** "I can experiment fearlessly."

### 15. 🧠 Skill: `hive-mind` (Cross-Device Sync)
*   **Trigger:** Using the agent on multiple devices.
*   **Scenario:** "I told you on my phone that I like dark mode."
*   **Mechanism:** A shared `user_preferences` table synced across all agent instances via DB.
*   **Aha!:** "It remembers me everywhere."
