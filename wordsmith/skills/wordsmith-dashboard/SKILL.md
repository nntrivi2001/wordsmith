---
name: wordsmith-dashboard
description: Launch the visual novel management dashboard (read-only Web Dashboard) to view project status, entity graphs, and chapter content in real time.
allowed-tools: Bash Read
---

# Webnovel Dashboard

## IMPORTANT: Before Executing — Read STYLE_GUIDE_VN.md First

**You MUST read `../../STYLE_GUIDE_VN.md` before starting any task.**

The STYLE_GUIDE_VN.md contains authoritative Vietnamese writing patterns that MUST be applied:
- Section 11: QUY TẮC CỤ THỂ (Units, Punctuation, Sentence Structure)
- Section 13: PATTERN ANALYSIS TỪ 4 NGUỒN TRUYỆN (Primary source: Ta Dung Nhin Vo Lam Toang)

**8 Error Types to Avoid (from user feedback):**
1. Units: Use mét/cm/km/kg (NOT trượng, dặm, tấc, thốn, ly)
2. Vocabulary: Match context ("đứa" not "đồng" for people)
3. Punctuation: Use — (single) NOT —— (double) for dialogue
4. Sentence structure: Must have subject + predicate (NO fragmented sentences)
5. Spelling: "ken két" not "kẽ kẽy"
6. Connectors: Use và/nhưng/nên/vì/sau đó/rồi/thì/mà
7. Subject: Descriptions MUST have explicit subject
8. Natural Vietnamese: Use natural words, not machine-translated Sino-Vietnamese

**Key Patterns from Ta Dung Nhin Vo Lam Toang:**
- Dialogue: "Nội dung" + (action tag) — no ——
- Inner thoughts: Third-person narrative without quotes, use "cậu" for self
- Scene breaks: --- for major, *— Hết Chương X —* for chapter end
- First-person: "cậu/mình" in internal monologue, "tao/mày" for close relationships
- Slang: "vãi", "cứt", "bro", "(@ v @)" acceptable in GenZ contexts

## Objective

Launch a **read-only** local web dashboard for visualizing the current novel project:
- Writing progress and Strand pacing distribution
- Settings dictionary (characters / locations / factions and other entities)
- Relationship graph
- Chapter and outline content browser
- Reader-pull analytics data

The dashboard uses `watchdog` to monitor changes in the `.webnovel/` directory and refreshes in real time; it does not modify the project in any way.

## Execution Steps

### Step 0: Environment Check

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -z "${CLAUDE_PLUGIN_ROOT}" ] || [ ! -d "${CLAUDE_PLUGIN_ROOT}/dashboard" ]; then
  echo "ERROR: Dashboard module not found: ${CLAUDE_PLUGIN_ROOT}/dashboard" >&2
  exit 1
fi
export DASHBOARD_DIR="${CLAUDE_PLUGIN_ROOT}/dashboard"
```

### Step 1: Install Dependencies (First Run)

```bash
python -m pip install -r "${DASHBOARD_DIR}/requirements.txt" --quiet
```

### Step 2: Resolve Project Root and Prepare Python Module Path

```bash
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT}/scripts"
export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
echo "Project path: ${PROJECT_ROOT}"

# Ensure `python -m dashboard.server` can locate the plugin module from any working directory
if [ -n "${PYTHONPATH:-}" ]; then
  export PYTHONPATH="${CLAUDE_PLUGIN_ROOT}:${PYTHONPATH}"
else
  export PYTHONPATH="${CLAUDE_PLUGIN_ROOT}"
fi

# The frontend dist is shipped with the plugin; if missing, the installation package is corrupted
if [ ! -f "${DASHBOARD_DIR}/frontend/dist/index.html" ]; then
  echo "ERROR: Missing frontend build artifact ${DASHBOARD_DIR}/frontend/dist/index.html" >&2
  echo "Please reinstall the plugin or contact the maintainer to fix the release package." >&2
  exit 1
fi
```

### Step 3: Launch Dashboard

```bash
python -m dashboard.server --project-root "${PROJECT_ROOT}"
```

The browser will open automatically to `http://127.0.0.1:8765` after startup.

To launch without opening the browser automatically:

```bash
python -m dashboard.server --project-root "${PROJECT_ROOT}" --no-browser
```

## Notes

- The Dashboard is a purely read-only panel; all APIs are GET-only with no write endpoints.
- File access is strictly scoped to `PROJECT_ROOT` to prevent path traversal.
- To use a custom port, add the `--port 9000` argument.
- For Vietnamese webnovel writing patterns and methodology, refer to [STYLE_GUIDE_VN.md](../../STYLE_GUIDE_VN.md).
