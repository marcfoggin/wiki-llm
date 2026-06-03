# Upgrading navtree-app to consume NavTree v2 format

Instructions for upgrading the existing navtree-app (Astro + React) to read
the v2 data format instead of the v1 docx-pipeline JSON.

## Current state (v1)

The app reads content from `src/data/content/{lang}/{bookFolder}/{chapter}/{section}.json`.
Each JSON file contains structured content blocks. The app scans this folder
hierarchy at build time via `loadIndex()` in `src/lib/content.ts`.

## Target state (v2)

The app reads from a v2 output folder containing:
- Numbered folders (`01/`, `01/01/`, etc.) — the folder hierarchy IS the tree
- `index.toml` in each folder — node metadata and optional `redirect_to`
- `content.md` in each folder — markdown content
- `search-positions.json` — content_id → tree positions map
- `config.toml` — global config (media sources, project name)

Key design points:
- **Folder hierarchy = navigation tree** — no separate tree.json to parse
- **Tree IDs are numeric** (`01`, `01/05`, `01/05/01`) — same convention as v1
- **Deduplication via redirects** — secondary positions have `redirect_to` in `index.toml`
- **Titles come from locale files or index.toml** — not from file paths

See `docs/navtree-v2-format.md` for the full spec.

## What needs to change

### 1. Replace `loadIndex()` with folder scanner

**File:** `src/lib/content.ts`

**Current:** `loadIndex(lang)` scans `src/data/content/{lang}/{book}/` for
chapter folders and JSON files, builds `BookIndex` with `Chapter[]` and
`Section[]` arrays.

**New:** Scan the v2 output folder hierarchy. Each numbered subfolder is a
tree node. Read `index.toml` from each folder for metadata.

```typescript
interface TreeNode {
  id: string            // folder path: "01", "01/05", "01/05/01"
  content_id: string    // stable content ref from index.toml
  title: string         // from index.toml or locales
  redirect_to?: string  // if present, fetch content from this path instead
  children: TreeNode[]  // from scanning numbered subfolders
}
```

Map to existing app interfaces:
- Each root folder → a top-level nav group
- Subfolders → nested `Section[]`
- `Section.slug` = folder path (e.g., `"01/05"`)
- `Section.title` = resolved from `index.toml [locales.{lang}]`, fallback to `title`
- `Section.id` = `content_id` from `index.toml`

When `redirect_to` is present, fetch content from that folder path instead.

### 2. Replace JSON section loader with markdown parser

**File:** `src/lib/content.ts` — `loadSection()` function

**Current:** Reads `{chapter}/{slug}.json`, returns `SectionContent` with
`content: ContentBlock[]`.

**New:** Read `{folder}/content.md`, parse markdown into `ContentBlock[]`.
If `index.toml` has `redirect_to`, read from the target folder instead.

Required parsing:
- `# Heading` / `## Heading` → `{type: "heading", text: "..."}`
- Plain paragraphs → `{type: "paragraph", text: "..."}`
- `![alt](path)` → `{type: "image", path: "...", alt: "...", caption: "..."}`
- Markdown tables → `{type: "table", rows: [...]}`
- `[[wikilinks]]` → convert to app-internal links using content_id

Recommended: use a library like `marked` or `markdown-it` to parse,
then walk the AST to produce `ContentBlock[]`.

### 3. Generate prev/next links from folder scan order

**Current:** Each JSON file has `links: [{type: "previous", target: "..."}, ...]`.

**New:** Compute prev/next by walking the folder tree in display order (depth-first).
Build a flat ordered list, then each node's prev/next is its neighbours:

```typescript
function buildNavOrder(roots: TreeNode[]): TreeNode[] {
  const order: TreeNode[] = []
  function walk(node: TreeNode) {
    order.push(node)
    node.children.forEach(walk)
  }
  roots.forEach(walk)
  return order
}
```

### 4. Read index.toml for metadata and locale-specific titles

Each `{folder}/index.toml` contains:

```toml
content_id = "stewarding-creation"
title = "Stewarding Creation"

[locales.eng]
title = "Stewarding Creation"

[locales.swe]
title = "Förvaltande av skapelsen"
```

The app should:
1. Read `index.toml` for each folder
2. Resolve title for current language from `[locales.{lang}]`
3. Fall back to `title` if no locale match
4. Read `[[pictures]]`, `[[audio]]`, `[[video]]` arrays when rendering media

### 5. Update routing

**Current routes:**
- `/{lang}/chapter/{N}` — chapter view
- `/{lang}/chapter/{N}/section/{slug}` — section view

**New routes (using numeric folder paths):**
- `/{lang}/01` — root node
- `/{lang}/01/05` — child node
- `/{lang}/01/05/01` — deeper node, unlimited depth

Use a catch-all route `[...path].astro` that parses numeric segments,
finds the folder, reads `index.toml`, and loads content.

### 6. Update Sidebar component

**Current:** Renders chapters with collapsible sections (2 levels).

**New:** Render folder tree recursively to any depth. Each node is collapsible
if it has children.

### 7. Handle redirects

When the app encounters `redirect_to` in `index.toml`, it should:
1. Display the node normally in the sidebar (with its own title)
2. Fetch `content.md` and media from the target folder path
3. Optionally show "Also found at: ..." using `search-positions.json`

## Files to modify (summary)

| File | Change |
|------|--------|
| `src/lib/content.ts` | Replace folder scanning + add markdown parsing + redirect handling |
| `src/components/Sidebar.jsx` | Recursive tree rendering (unlimited depth) |
| `src/pages/[lang]/chapter/[chapter].astro` | Replace with `[lang]/[...path].astro` catch-all |
| `src/pages/[lang]/chapter/[chapter]/section/[section].astro` | Remove (merged into catch-all) |
| `src/components/ContentRenderer.jsx` | Add markdown → ContentBlock[] conversion |
| `package.json` | Add `marked` (or `markdown-it`) + TOML parser dependency |

## Migration order

1. Add folder scanner (replaces loadIndex)
2. Add markdown parser (replaces JSON section loader)
3. Add index.toml reader with locale resolution and redirect handling
4. Update routing to use numeric folder paths
5. Update Sidebar for recursive rendering
6. Test with v2 output from `python3 build_navtree.py`
7. Add search-positions.json support (when search is implemented)
