# Wiki — Schema & Workflow Instructions

This wiki is an Obsidian vault maintained by Claude Code following the Karpathy LLM Wiki pattern. The user provides raw sources; Claude compiles them into structured, cross-referenced wiki pages.

## Core Rules

### 1. Three Top Topics Are Fixed

The wiki is organized under exactly three top-level topics. These are stable and must not be renamed, removed, merged, or reordered:

1. **Five Marks of Mission** — `wiki/Five Marks of Mission/`
2. **Creation Care / Stewardship** — `wiki/Creation Care/`
3. **Nomadic Pastoralism** — `wiki/Nomadic Pastoralism/`

Every wiki page must belong to one of these three topics. Content that spans multiple topics lives under its primary topic with cross-links to the others.

### 2. Subfolders Serve the Topic

Subfolder structure (e.g. Concepts/, Entities/, Sources/) is not fixed. A subfolder is only created under a top topic when it is genuinely useful for organizing that topic's content. Do not impose a uniform subfolder scheme across all three topics — let each topic's content dictate its own structure.

### 3. Raw Is Immutable

Never modify files in `raw/`. They are source material.

### 4. Index Must Stay Current

Always update `wiki/index.md` when adding or removing pages.

### 5. Cross-Link Aggressively

Every page should link to related pages across and within topics. Use `[[Topic Folder/page-name]]` wikilinks.

### 6. Append, Don't Overwrite

When updating an existing page with new source material, append rather than overwrite. Preserve prior claims and note the new source.

### 7. Mark Unverified Claims

If a factual claim on a wiki page has no source, mark it with `[needs verification]` inline. Do not silently present unsourced claims as established facts. When a source is later found, replace the marker with a proper citation.

### 8. External Links: Summarise, Don't Copy

When a source document contains external URLs (articles, papers, org pages):
- **Never** store full fetched content in `raw/` or anywhere else (copyright).
- **Do** fetch and read the linked resource when processing a source.
- **Do** write an AI-generated summary in your own words on the relevant wiki page.
- **Always** keep the original URL as the canonical reference.
- Format external references as: `[Title / Description](URL) — summary in own words`
- **Always** update `wiki/source-registry.md` after fetching (see Rule 9).

### 9. Operation Log

After every ingest or significant wiki update, append an entry to `wiki/log.md` recording the date, what source was processed, and which pages were created or updated. This provides a human-readable changelog browsable inside Obsidian without needing git.

### 10. Source Registry

Every external URL that is fetched must be logged in `wiki/source-registry.md`. This is the single source of truth for what has been processed.

For each URL, record:
- **URL** — the canonical link
- **Status** — `done`, `revisit`, or `failed`
- **Last Fetched** — date of most recent fetch
- **Pages Updated** — which wiki pages received content from this URL
- **Focus / Notes** — what was extracted; what was skipped

Before fetching a URL during ingest:
1. Check the registry — if the URL is already `done`, skip it unless the user explicitly requests a revisit or the status is `revisit`.
2. If the fetch fails (paywall, 403, dead link), log it as `failed` with the reason.

The user may mark any URL as `revisit` to request a second pass with a different focus. When revisiting, append new findings to the wiki page rather than replacing existing summaries.

## Directory Layout

```
raw/                          # Immutable source documents
wiki/                         # Claude owns this layer
  index.md                   # Master index — update on every ingest
  log.md                     # Append-only operation log
  source-registry.md         # Tracks all fetched external URLs
  Sources/                   # Detailed literature notes (shared across topics)
  Five Marks of Mission/     # Topic 1
  Creation Care/             # Topic 2
  Nomadic Pastoralism/       # Topic 3
.obsidian/                    # Vault config — do not modify
```

## Page Format

Every wiki page uses this frontmatter:

```yaml
---
title: "Page Title"
type: topic | subtopic | concept | entity | source | comparison
tags: []
sources: []
last_updated: YYYY-MM-DD
---
```

Use `[[Folder/page-name]]` wikilinks (Obsidian-style, with subfolder path).

## Ingest Workflow

Triggered by: *"ingest raw/\<file\>"*

Steps:
1. Read the source document fully
2. Read `wiki/index.md` for current wiki context
3. Discuss key takeaways with the user before writing anything — confirm which topics are relevant and what pages should be created or updated
4. Determine which of the three top topics the source relates to
5. Create/update pages under the appropriate topic folder(s)
6. Update `wiki/index.md` — add entries under the appropriate sections
7. Flag any contradictions with existing wiki content
8. Append an entry to `wiki/log.md` (see Rule 9)
9. Print a change summary listing all created/updated pages

### Source Page Format (Literature Notes)

Detailed literature notes live in `wiki/Sources/`. This is a shared folder — source pages serve all three topics via cross-links. Each external resource that warrants detailed treatment gets its own page here. Subtopic pages keep a short one-liner and link to the full source page.

On subtopic pages, format source references as:
`[Title](URL) — short summary. [[Sources/slug|Full notes]]`

```markdown
---
title: "Source Title"
type: source
tags: []
date: YYYY-MM-DD
url: https://...
last_updated: YYYY-MM-DD
---

## Summary
4–6 paragraph detailed summary in own words.

## Key Claims
- Claim 1
- Claim 2

## Key Quotes
> "Quote here"

## Connections
- [[Topic/page-name]] — how it relates

## Contradictions
- Contradicts [[page]] on: ...
```

### Subtopic Page Format

```markdown
---
title: "Subtopic Name"
type: subtopic
tags: []
sources: []
last_updated: YYYY-MM-DD
---

## Overview
1–3 paragraph explanation.

## Key Points
- Point 1
- Point 2

## Related
- [[Topic/related-page]]

## Sources
- [[Topic/source-page]]
```

## Query Workflow

Triggered by: *"query: \<question\>"*

Steps:
1. Read `wiki/index.md` to identify relevant pages
2. Read those pages
3. Synthesize an answer with inline `[[wikilinks]]` citations
4. Ask if the user wants the answer saved as a page under the relevant topic

## Lint Workflow

Triggered by: *"lint the wiki"*

Check for:
- **Orphan pages** — pages with no inbound links
- **Broken links** — `[[wikilinks]]` pointing to nonexistent pages
- **Stale pages** — pages not updated after newer sources were ingested
- **Missing pages** — topics mentioned in 3+ pages but lacking their own page
- **Misplaced pages** — pages that don't clearly belong to their top topic

Output a report and ask if fixes should be applied.

## Naming Conventions

- All page filenames: `kebab-case.md`
- Wikilinks include subfolder: `[[Five Marks of Mission/stewarding-creation]]`
- Index entries: `- [[Folder/slug]] — one-line description`

## NavTree vault coordination

Some notes in this vault appear at multiple positions in the navigation
tree built by ../.navtree/build_navtree.py. Before making structural
changes (rename, restructure links, split, delete), read
../.navtree/output/redirects.toml to check if the note is multi-position.

Rules:
- Editing content: always safe, no logging needed.
- Adding new notes/links to non-multi-position notes: safe, no logging.
- Rename/restructure/split/delete a note listed in redirects.toml:
  make the change, then append an entry to vault-changelog.toml
  (in this vault root):

  [[change]]
  date = "YYYY-MM-DD"
  agent = "your-agent-name"
  type = "rename"              # rename | restructure | split | delete
  note = "Original Note Name"
  new_name = "New Name"        # renames only
  action = "What changed"      # restructure/split only
  reason = "Why"
  affected_positions = ["01/05/01", "02"]   # from redirects.toml

- Notes NOT in redirects.toml can be changed freely without logging.
