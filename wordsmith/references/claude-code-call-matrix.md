# Claude Code Call Matrix (Command Ownership and Trigger Points)

> Purpose: Clearly define "who calls what, when, and which scripts" to avoid mistaking Claude Code internal processes for manual user commands.

## Rules

- Scripts in this project are triggered by **Claude Code Skills/Agents** at pipeline nodes by default.
- Unless explicitly stated in the documentation, scripts are not treated as routine user-facing commands.
- When adding new scripts or new command trigger points, this file must be updated at the same time.

## Command-Level Matrix (Entry → Caller → Trigger Point)

| Entry Command | Caller | Trigger Point | Key Script / Action |
|---|---|---|---|
| `/webnovel-init` | `webnovel-init` Skill | New project creation, deep initialization phase | `scripts/init_project.py` + generate `idea_bank.json` |
| `/webnovel-plan` | `webnovel-plan` Skill | When volume/chapter outline generation completes and state is written back | `scripts/update_state.py --volume-planned ...` |
| `/webnovel-write` | `webnovel-write` Skill | Step 5 data chain update during the writing workflow | Task calls `data-agent` (which internally writes state/index) |
| `/webnovel-query` | `webnovel-query` Skill | When analysis requests for "foreshadowing urgency / Strand pacing" are made | `scripts/status_reporter.py --focus urgency/strand` |
| `/webnovel-resume` | `webnovel-resume` Skill | Interruption detection, cleanup, and breakpoint recovery | `scripts/workflow_manager.py detect/cleanup/clear` |

## Script-Level Matrix (Script → Who Triggers → When)

| Script | Primary Trigger | Trigger Node | Notes |
|---|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}/scripts/webnovel.py` | All Skills / Agents | Any node requiring a CLI call | **Unified entry point**: resolves the true book `project_root` and forwards to `data_modules/*` or `scripts/*.py`, avoiding hidden failures caused by `PYTHONPATH/cd/parameter ordering` |
| `${CLAUDE_PLUGIN_ROOT}/scripts/update_state.py` | `webnovel-plan` Skill | Updates `state.json` after chapter/volume planning is persisted | Can also be called by automation scripts; not a routine manual entry point by default |
| `${CLAUDE_PLUGIN_ROOT}/scripts/status_reporter.py` | `webnovel-query` Skill / `pacing-checker` Agent (optional) | During query analysis or pacing review | Produces health reports and urgency analysis |
| `${CLAUDE_PLUGIN_ROOT}/scripts/workflow_manager.py` | `webnovel-resume` Skill | Recovery workflow: detect/cleanup/clear | Only triggered in recovery scenarios |
| `${CLAUDE_PLUGIN_ROOT}/scripts/init_project.py` | `webnovel-init` Skill | Project initialization phase | Responsible for project scaffolding and base state files |

## Internal Library Calls (Not Standalone Commands)

| Internal Module | Caller | Trigger Point |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}/scripts/data_modules/state_validator.py` | `update_state.py`, `status_reporter.py` | Automatically normalizes and validates on each `state.json` read/write |

## Change Constraints (Must Be Followed in Future Development)

1. If a new script that can be triggered by a Skill/Agent is added, it must be appended to this matrix.
2. If a script's trigger point changes (e.g., moved from the plan phase to the write phase), this matrix must be updated accordingly.
3. PR/commit messages must clearly state "caller + trigger node + whether manual invocation is permitted".