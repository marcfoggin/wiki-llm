# LLM Wiki — Faith, Creation Care & Pastoralism

An Obsidian vault and AI-assisted knowledge base covering three interconnected domains: the Five Marks of Mission, Creation Care, and Nomadic Pastoralism. Built using the [Karpathy LLM Wiki pattern](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code) — raw sources go in, structured cross-referenced wiki pages come out.

## How It Works

1. Drop source documents (`.docx`, `.md`, `.pdf`) into `raw/`
2. Ask your AI assistant to ingest them
3. The AI reads the source, fetches external links, and compiles structured wiki pages under the appropriate topic
4. External resources are summarised in the AI's own words (never copied) with the original URL kept as canonical reference
5. All fetched URLs are logged in `wiki/source-registry.md`

## Structure

```
raw/                          # Source documents (immutable — never edited)
wiki/                         # AI-managed wiki pages
  index.md                    # Master index
  source-registry.md          # Tracks all fetched external URLs
  Five Marks of Mission/      # Topic 1 — proclamation, service, justice, creation care
  Creation Care/              # Topic 2 — ecosystems, biodiversity, stewardship
  Nomadic Pastoralism/        # Topic 3 — mobility, commons, indigenous knowledge
.obsidian/                    # Obsidian vault config
```

## Browsing

Open the root folder as a vault in [Obsidian](https://obsidian.md/). All `[[wikilinks]]` resolve to pages within the vault. The Homepage plugin opens `wiki/index.md` on startup.

## Conventions

All wiki conventions — page formats, naming rules, ingest workflow, source handling — live in `CLAUDE.md`. This is the single source of truth that every contributor's AI assistant must follow.

Key rules:
- The three top-level topics are fixed and must not be renamed or restructured
- Subfolder structure under each topic is flexible — only add subfolders when they help
- External content is never stored verbatim (copyright) — only AI-generated summaries with source URLs
- Every fetched URL is logged in `wiki/source-registry.md` with status, date, and focus
- `raw/` is immutable — source documents are never modified after being added

## Setting Up Your AI Assistant

The file `CLAUDE.md` contains all the rules, workflows, and page formats your AI assistant needs to follow. Despite the name, it is not Claude-specific — it works with any AI tool.

### Claude Code
No setup needed. Claude Code reads `CLAUDE.md` automatically when you open the project.

### Cursor
Cursor reads `.cursorrules` automatically. Copy `CLAUDE.md` to `.cursorrules` in the project root:
1. Open a terminal in the project folder
2. Run: `cp CLAUDE.md .cursorrules`
3. Cursor will now follow the wiki conventions automatically

If the project's `.cursorrules` gets out of date, re-copy from `CLAUDE.md` — that file is always the canonical version.

### GitHub Copilot
Copilot reads `.github/copilot-instructions.md` automatically. Copy the conventions there:
1. Run: `cp CLAUDE.md .github/copilot-instructions.md`
2. Copilot will now follow the wiki conventions in chat and suggestions

### Windsurf
Windsurf reads `.windsurfrules` automatically:
1. Run: `cp CLAUDE.md .windsurfrules`

### ChatGPT, Gemini, or other chat-based tools
Paste the contents of `CLAUDE.md` into your first message at the start of each session. For example:
> "Here are the conventions for this wiki project. Follow these rules for all work in this session: [paste CLAUDE.md contents]"

### Important
- `CLAUDE.md` is the canonical source — if you create a tool-specific copy (`.cursorrules`, etc.), keep it in sync
- Do not commit tool-specific copies to the repository unless the team agrees — they can drift out of date
- When in doubt, re-read `CLAUDE.md` directly

## Contributing

This project supports multi-user collaboration. New contributors should start with `ONBOARDING.md` for a step-by-step setup guide.

Key workflow rules:
- Work on a named branch (`yourname/topic`) — no direct pushes to `main`
- Open a PR using the provided template and wait for review before merge
- Check `wiki/source-registry.md` before fetching any URL to avoid duplicate work
- Feed `CLAUDE.md` to your AI tool at session start (Claude Code reads it automatically)
- Review PRs for content contradictions and overlapping summaries
