# System Architecture & Module Design

## Core Principles

### Three Anti-Hallucination Laws

| Law | Description | Enforcement |
|------|------|---------|
| **Outline is Law** | Follow the outline strictly; no ad-lib | Context Agent force-loads chapter outlines |
| **Setting is Physics** | Respect settings; no self-contradictions | Consistency Checker performs real-time validation |
| **Inventions Must Be Registered** | New entities must be tracked in the database | Data Agent extracts and disambiguates automatically |

### Strand Weave Pacing System

| Strand | Meaning | Ideal Ratio | Description |
|--------|------|---------|------|
| **Quest** | Main plot | 60% | Drives core conflict |
| **Fire** | Romance | 20% | Character relationship development |
| **Constellation** | World-building | 20% | Background / factions / settings |

Pacing red lines:

- Quest: no more than 5 consecutive chapters
- Fire: no more than 10 chapters gap
- Constellation: no more than 15 chapters gap

## Overall Architecture Diagram

```text
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code                           │
├─────────────────────────────────────────────────────────────┤
│  Skills (7): init / plan / write / review / query / ...    │
├─────────────────────────────────────────────────────────────┤
│  Agents (8): Context / Data / Multi-dimensional Checkers   │
├─────────────────────────────────────────────────────────────┤
│  Data Layer: state.json / index.db / vectors.db            │
└─────────────────────────────────────────────────────────────┘
```

## Dual Agent Architecture

### Context Agent (Read)

Responsibilities: Before writing, builds a "Creative Task Brief" providing the current chapter's context, constraints, and reader-retention strategy.

### Data Agent (Write)

Responsibilities: Extracts entities and state changes from the chapter text; updates `state.json`, `index.db`, and `vectors.db` to maintain a closed data loop.

## Six-Dimensional Parallel Review

| Checker | Focus |
|---------|---------|
| High-point Checker | Cool-point density and quality |
| Consistency Checker | Setting consistency (combat power / location / timeline) |
| Pacing Checker | Strand ratio and gap monitoring |
| OOC Checker | Whether character behavior deviates from established personality |
| Continuity Checker | Scene and narrative continuity |
| Reader-pull Checker | Hook strength, expectation management, reader retention |