# Roadmap

## Completed: Solo Maintainer Phase

- [x] Obsidian vault structure with three fixed top topics
- [x] CLAUDE.md with wiki conventions and workflows (10 rules)
- [x] Source registry for tracking fetched external URLs
- [x] Git versioning
- [x] Complete initial ingest of `raw/ClusterDocsTablesV2.docx` (all three topics)
- [x] 18 subtopic pages + 26 source pages populated
- [x] Cross-link audit and enrichment
- [x] Operation log (`wiki/log.md`)
- [x] Unsourced claims tagged with `[needs verification]`

## Current: Multi-User Collaboration

Target: 2–3 contributors, each using their own AI assistant.

### Setup
- [x] Create GitHub repository and push main branch
- [x] Protect `main` branch — branch ruleset (no force push, no delete, require PR with 1 approval)
- [x] Add PR template (`.github/pull_request_template.md`) with checklist
- [ ] Add contributors with write access

### Workflow Rules
- Each contributor works on a named branch (`yourname/topic`)
- PRs require at least one review before merge
- Check `wiki/source-registry.md` before fetching any URL — avoid duplicate work
- Conflicts in `index.md` and `source-registry.md` are resolved by the merger (these are append-only files, so conflicts are typically mechanical)

### AI Tool Compatibility
- Claude Code users: `CLAUDE.md` is read automatically
- Other AI tools: contributors must feed `CLAUDE.md` to their tool at session start
- Consider adding tool-specific config files if needed (e.g., `.cursorrules`)

### Known Risks
- **Merge conflicts** in shared files (`index.md`, `source-registry.md`) — mitigated by branch workflow and append-only design
- **Convention drift** across different AI tools — mitigated by single `CLAUDE.md` source of truth and PR review
- **Duplicate ingests** — mitigated by source registry check before fetching
- **Contradictory summaries** — flagged during PR review; wiki pages should note contradictions explicitly rather than silently overwriting

## Later: Automation & Quality

- [ ] Lint workflow — automated checks for orphan pages, broken links, stale content
- [ ] Pre-commit hook or CI check that validates frontmatter format and index consistency
- [ ] Change detection for external URLs — periodic check for updated sources (HTTP headers or content hashing)
- [ ] Knowledge graph visualisation (`graph/` folder with auto-generated data)
- [ ] GitHub Actions to run lint on PR
