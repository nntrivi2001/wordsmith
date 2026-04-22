# Wordsmith

Long-form webnovel writing system with integrated Vietnamese writing patterns.

## Features

- 8 skills: write, plan, review, init, query, resume, dashboard, learn
- 7 specialized agents for consistency, continuity, pacing, and more
- RAG with local vector index
- Vietnamese writing patterns from 4 reference sources

## Installation

Add to `CLAUDE_PLUGIN_PATHS` in your Claude Code settings:

```json
{
  "CLAUDE_PLUGIN_PATHS": [
    "/path/to/wordsmith"
  ]
}
```

## Usage

```bash
/webnovel-write        # Write a new chapter
/webnovel-write --fast # Fast mode
/webnovel-plan         # Plan plot/outline
/webnovel-review       # Review written chapter
/webnovel-init         # Initialize new project
/webnovel-dashboard    # Open visual dashboard
/webnovel-learn        # Extract patterns from session
```

## Vietnamese Writing Rules

See `STYLE_GUIDE_VN.md` for full details.

Key rules:
- Units: Use `mét, cm, km, kg` (not Chinese units)
- Dialogue: `"Content" - action tag`
- Inner thoughts: Third-person, no quotes
- Minimum 8 words per sentence
- Scene breaks: `---` for major, `*— Hết Chương X —*` for end

## Structure

```
wordsmith/
├── skills/        # 8 main skills
├── agents/        # 7 specialized agents
├── references/    # Shared references
├── genres/       # Genre-specific templates
├── scripts/       # Python scripts
├── dashboard/     # Web dashboard
└── STYLE_GUIDE_VN.md
```

## Author

nntrivi2001

## Version

| version | notes |
|------|------|
| **v1.0.0 (current)** | Initial release |

