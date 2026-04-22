# Project Structure & Operations

## Directory Hierarchy (Runtime)

Under a Claude Code + Marketplace installation, there are at least 4 conceptual layers:

1. `WORKSPACE_ROOT` (Claude workspace root, typically `${CLAUDE_PROJECT_DIR}`)
2. `WORKSPACE_ROOT/.claude/` (workspace-level pointer and configuration)
3. `PROJECT_ROOT` (the actual novel project root, created by `/webnovel-init` under the book title)
4. `CLAUDE_PLUGIN_ROOT` (plugin cache directory, not inside the project)

### A) Workspace Directory (including `.claude`)

```text
workspace-root/
├── .claude/
│   ├── .webnovel-current-project   # Points to the current novel project root
│   └── settings.json
├── NovelA/
├── NovelB/
└── ...
```

### B) Novel Project Directory (`PROJECT_ROOT`)

```text
project-root/
├── .webnovel/            # Runtime data (state/index/vectors/summaries)
├── Chapters/             # Main body chapters
├── Outline/              # Outline (general and volume-level)
└── Settings/             # Settings (worldview, characters, power system)
```

## Plugin Directory (Marketplace Installation)

The plugin does not reside inside the novel project directory; it lives in the Claude plugin cache directory. At runtime, it is consistently referenced as `CLAUDE_PLUGIN_ROOT`:

```text
${CLAUDE_PLUGIN_ROOT}/
├── skills/
├── agents/
├── scripts/
└── references/
```

### C) User-Level Global Mapping (Fallback)

When no usable pointer exists in the workspace, the user-level registry is used for `workspace -> current_project_root` mapping:

```text
${CLAUDE_HOME:-~/.claude}/wordsmith/workspaces.json
```

## Simulated Directory Test (2026-03-03)

Based on actual results from `D:\wk\novel skill\plugin-sim-20260303-012048`:

- `WORKSPACE_ROOT`: `D:\wk\novel skill\plugin-sim-20260303-012048`
- Pointer file: `D:\wk\novel skill\plugin-sim-20260303-012048\.claude\.webnovel-current-project`
- Pointer content: `D:\wk\novel skill\plugin-sim-20260303-012048\MortalityCapitalism-SecondTest`
- Example created projects: `MortalityCapitalism/`, `MortalityCapitalism-SecondTest/`

## Common Operations Commands

Unified preamble (manual CLI scenario):

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"
export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

### Index Rebuild

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index process-chapter --chapter 1
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index stats
```

### Health Report

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" status -- --focus all
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" status -- --focus urgency
```

### Vector Rebuild

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" rag index-chapter --chapter 1
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" rag stats
```

### Test Entry Points

```bash
pwsh "${CLAUDE_PLUGIN_ROOT}/scripts/run_tests.ps1" -Mode smoke
pwsh "${CLAUDE_PLUGIN_ROOT}/scripts/run_tests.ps1" -Mode full
```