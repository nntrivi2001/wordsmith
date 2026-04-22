# Command Reference

## `/webnovel-init`

Purpose: Initialize a novel project (directory structure, setting templates, state files).

Output:

- `.webnovel/state.json`
- `Settings/`
- `Outline/general-outline.md`

## `/webnovel-plan [volume-number]`

Purpose: Generate volume-level planning and chapter outlines.

Examples:

```bash
/webnovel-plan 1
/webnovel-plan 2-3
```

## `/webnovel-write [chapter-number]`

Purpose: Execute the full chapter writing workflow (context → draft → review → polish → data persistence).

Examples:

```bash
/webnovel-write 1
/webnovel-write 45
```

Common modes:

- Standard mode: full pipeline
- Fast mode: `--fast`
- Minimal mode: `--minimal`

## `/webnovel-review [range]`

Purpose: Perform multi-dimensional quality review on existing chapters.

Examples:

```bash
/webnovel-review 1-5
/webnovel-review 45
```

## `/webnovel-query [keyword]`

Purpose: Query runtime information such as characters, foreshadowing, pacing, and state.

Examples:

```bash
/webnovel-query protagonist_name
/webnovel-query foreshadowing
/webnovel-query urgency
```

## `/webnovel-resume`

Purpose: Automatically detect the last breakpoint and resume after a task interruption.

Examples:

```bash
/webnovel-resume
```

## `/webnovel-dashboard`

Purpose: Launch a read-only visualization panel to inspect project state, entity relationships, chapters, and outlines.

Examples:

```bash
/webnovel-dashboard
```

Notes:

- Read-only by default; does not modify project files
- Useful for diagnosing context, entity relationships, and chapter progress

## `/webnovel-learn [content]`

Purpose: Extract reusable writing patterns from the current session or user input and write them into the project memory.

Examples:

```bash
/webnovel-learn "The crisis hook design in this chapter was very effective, full of suspense"
```

Output:

- `.webnovel/project_memory.json`