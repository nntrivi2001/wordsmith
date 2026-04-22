# Command Reference

## `/wordsmith-init`

Purpose: Initialize a novel project (directory structure, setting templates, state files).

Output:

- `.webnovel/state.json`
- `Settings/`
- `Outline/general-outline.md`

## `/wordsmith-plan [volume-number]`

Purpose: Generate volume-level planning and chapter outlines.

Examples:

```bash
/wordsmith-plan 1
/wordsmith-plan 2-3
```

## `/wordsmith-write [chapter-number]`

Purpose: Execute the full chapter writing workflow (context → draft → review → polish → data persistence).

Examples:

```bash
/wordsmith-write 1
/wordsmith-write 45
```

Common modes:

- Standard mode: full pipeline
- Fast mode: `--fast`
- Minimal mode: `--minimal`

## `/wordsmith-review [range]`

Purpose: Perform multi-dimensional quality review on existing chapters.

Examples:

```bash
/wordsmith-review 1-5
/wordsmith-review 45
```

## `/wordsmith-query [keyword]`

Purpose: Query runtime information such as characters, foreshadowing, pacing, and state.

Examples:

```bash
/wordsmith-query protagonist_name
/wordsmith-query foreshadowing
/wordsmith-query urgency
```

## `/wordsmith-resume`

Purpose: Automatically detect the last breakpoint and resume after a task interruption.

Examples:

```bash
/wordsmith-resume
```

## `/wordsmith-dashboard`

Purpose: Launch a read-only visualization panel to inspect project state, entity relationships, chapters, and outlines.

Examples:

```bash
/wordsmith-dashboard
```

Notes:

- Read-only by default; does not modify project files
- Useful for diagnosing context, entity relationships, and chapter progress

## `/wordsmith-learn [content]`

Purpose: Extract reusable writing patterns from the current session or user input and write them into the project memory.

Examples:

```bash
/wordsmith-learn "The crisis hook design in this chapter was very effective, full of suspense"
```

Output:

- `.webnovel/project_memory.json`