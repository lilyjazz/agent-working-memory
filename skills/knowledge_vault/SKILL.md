# Knowledge Vault (Powered by TiDB Zero)

## Goal
To give the Agent a "Semantic Long-term Memory".
Store text snippets as vectors and retrieve them by meaning (not just keyword match).

## 📥 Installation

### 1. Add to `TOOLS.md`
```markdown
- **knowledge-vault**: Store and retrieve knowledge using vector search.
  - **Location:** `/path/to/skills/knowledge_vault/SKILL.md`
  - **Command:** `python /path/to/skills/knowledge_vault/run.py --action search --query "<QUESTION>"`
```

### 2. Add to `AGENTS.md` (Protocol)
Copy [PROTOCOL.md](PROTOCOL.md).

## Usage
*   `--action add --content "The user loves spicy food."`
*   `--action search --query "What food does the user like?"`
