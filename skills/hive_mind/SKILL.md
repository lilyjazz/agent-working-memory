# Hive Mind (Powered by TiDB Zero)

## Goal
To store user preferences and agent state in a persistent cloud database. This allows the Agent to "remember" things even after a restart or when moving to a new device.

## 📥 Installation

### 1. Add to `TOOLS.md`
```markdown
- **hive-mind**: Store/Retrieve persistent key-value preferences.
  - **Location:** `/path/to/skills/hive_mind/SKILL.md`
  - **Command:** `python /path/to/skills/hive_mind/run.py --action set --key "theme" --value "dark"`
```

### 2. Add to `AGENTS.md` (Protocol)
Copy [PROTOCOL.md](PROTOCOL.md).

## Usage
*   `--action set --key k --value v`
*   `--action get --key k`
*   `--action list`
