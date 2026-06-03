#!/usr/bin/env python3
"""Build a NavTree v2 structure from an Obsidian vault.

Reads an Obsidian vault, follows [[wikilinks]] from root notes,
and outputs the v2 format:
- Hierarchical numbered folders with index.toml + content.md
- search-positions.json for search result linking
- config.toml for global settings
- redirects.toml in the vault for AI agent awareness of multi-position content
"""

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]")

KNOWN_NODE_FIELDS = {"content_id", "title", "description", "thumbnail", "sort_order"}
MEDIA_CONFIG_KEYS = {"pictures_config", "audio_config", "video_config"}


def slugify(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


def parse_links(filepath: Path) -> list[str]:
    text = filepath.read_text(encoding="utf-8")
    return WIKILINK_RE.findall(text)


def load_vault(vault_path: Path) -> dict[str, Path]:
    """Index vault notes by both stem and folder/stem relative path."""
    notes = {}
    for p in vault_path.glob("**/*.md"):
        notes[p.stem] = p
        rel = p.relative_to(vault_path).with_suffix("")
        notes[str(rel)] = p
    return notes


def resolve_link(link: str, vault: dict[str, Path]) -> tuple[str, Path | None]:
    """Resolve a wikilink to a (display_name, filepath) pair."""
    if link in vault:
        filepath = vault[link]
        return filepath.stem, filepath

    stem = link.rsplit("/", 1)[-1] if "/" in link else link
    if stem in vault:
        return stem, vault[stem]

    return stem, None


def find_vault_source(content_id: str, vault: dict[str, Path]) -> Path | None:
    """Find the vault source file for a content_id."""
    for _key, path in vault.items():
        if path.stem == content_id or slugify(path.stem) == content_id:
            return path
    return None


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter fields from a markdown file."""
    if not filepath or not filepath.exists():
        return {}
    text = filepath.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.+?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        return {}
    fields = {}
    current_section = None
    for line in fm_match.group(1).splitlines():
        section_match = re.match(r"^(\w[\w_]*):\s*$", line)
        if section_match:
            current_section = section_match.group(1)
            fields[current_section] = {}
            continue
        if current_section:
            kv_match = re.match(r"^\s+(\w[\w_]*):\s*(.+)$", line)
            if kv_match:
                fields[current_section][kv_match.group(1)] = kv_match.group(2).strip().strip("\"'")
            elif re.match(r"^\S", line):
                current_section = None
        if not current_section:
            kv_match = re.match(r"^(\w[\w_]*):\s*(.+)$", line)
            if kv_match:
                val = kv_match.group(2).strip().strip("\"'")
                fields[kv_match.group(1)] = val
    return fields


def get_title(filepath: Path, fallback_name: str) -> str:
    title = fallback_name.replace("-", " ").title()
    if filepath and filepath.exists():
        text = filepath.read_text(encoding="utf-8")
        fm_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
        if fm_match:
            title = fm_match.group(1)
    return title


def format_toml_value(val):
    """Format a Python value as a TOML literal."""
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    return f'"{val}"'


def build_tree(
    note_name: str,
    vault: dict[str, Path],
    visited: set | None = None,
    parent_id: str = "",
    sibling_counter: dict | None = None,
    max_depth: int = 10,
    filepath: Path | None = None,
    skip_prefixes: list | None = None,
    content_id_primary: dict | None = None,
    is_root: bool = False,
) -> dict | None:
    if visited is None:
        visited = set()
    if sibling_counter is None:
        sibling_counter = {"n": 0}
    if skip_prefixes is None:
        skip_prefixes = ["Sources/", "source"]
    if content_id_primary is None:
        content_id_primary = {}

    if filepath is None:
        filepath = vault.get(note_name)

    resolved_key = str(filepath) if filepath else note_name
    if max_depth <= 0:
        return None
    if resolved_key in visited and not is_root:
        return None

    content_id = slugify(note_name)
    has_content = filepath is not None
    title = get_title(filepath, note_name)

    sibling_counter["n"] += 1
    numeric_segment = f"{sibling_counter['n']:02d}"
    node_id = f"{parent_id}/{numeric_segment}" if parent_id else numeric_segment

    redirect_to = None
    if content_id in content_id_primary:
        redirect_to = content_id_primary[content_id]
    else:
        content_id_primary[content_id] = node_id

    node = {
        "id": node_id,
        "content_id": content_id,
        "title": title,
        "has_content": has_content,
        "redirect_to": redirect_to,
        "children": [],
    }

    if not has_content or redirect_to:
        return node

    visited.add(resolved_key)

    child_counter = {"n": 0}
    for link in parse_links(filepath):
        child_name, child_path = resolve_link(link, vault)
        if child_path and str(child_path) in visited:
            continue
        if any(link.startswith(p) for p in skip_prefixes):
            continue
        child = build_tree(
            child_name, vault, visited, node_id, child_counter, max_depth - 1,
            filepath=child_path, skip_prefixes=skip_prefixes,
            content_id_primary=content_id_primary,
        )
        if child is not None:
            node["children"].append(child)

    return node


def build_index_toml(node: dict, vault: dict[str, Path]) -> str:
    """Build index.toml content for a node."""
    cid = node["content_id"]
    lines = [
        f'content_id = "{cid}"',
        f'title = "{node["title"]}"',
    ]

    if node.get("redirect_to"):
        lines.append(f'redirect_to = "{node["redirect_to"]}"')
    else:
        source = find_vault_source(cid, vault)
        fm = parse_frontmatter(source) if source else {}
        for k, v in fm.items():
            if k in KNOWN_NODE_FIELDS or k == "title":
                continue
            if k in MEDIA_CONFIG_KEYS:
                continue
            if isinstance(v, dict):
                continue
            lines.append(f"{k} = {format_toml_value(v)}")

        for config_key in sorted(MEDIA_CONFIG_KEYS):
            if config_key in fm and isinstance(fm[config_key], dict):
                lines.append(f"\n[{config_key}]")
                for ck, cv in fm[config_key].items():
                    lines.append(f"{ck} = {format_toml_value(cv)}")

    return "\n".join(lines) + "\n"


def write_hierarchical_tree(output_dir: Path, nodes: list[dict], vault: dict[str, Path]) -> None:
    """Write numbered folder hierarchy with index.toml + content.md per node."""
    for node in nodes:
        node_dir = output_dir / node["id"]
        node_dir.mkdir(parents=True, exist_ok=True)

        (node_dir / "index.toml").write_text(
            build_index_toml(node, vault), encoding="utf-8"
        )

        if not node.get("redirect_to") and node["has_content"]:
            source = find_vault_source(node["content_id"], vault)
            if source and source.exists():
                content = source.read_text(encoding="utf-8")
                (node_dir / "content.md").write_text(content, encoding="utf-8")

        write_hierarchical_tree(output_dir, node["children"], vault)


def collect_tree_positions(nodes: list[dict], positions: dict | None = None, breadcrumb: list | None = None) -> dict:
    """Build a map of content_id → list of tree positions (for search linking)."""
    if positions is None:
        positions = {}
    if breadcrumb is None:
        breadcrumb = []

    for node in nodes:
        path = breadcrumb + [node["title"]]
        cid = node["content_id"]
        if cid not in positions:
            positions[cid] = []
        positions[cid].append({
            "tree_id": node["id"],
            "breadcrumb": path,
        })
        collect_tree_positions(node["children"], positions, path)

    return positions


def collect_content_map(nodes: list[dict]) -> dict[str, dict]:
    """Collect content_id → title map for the multi-position log."""
    content_map = {}
    for node in nodes:
        cid = node["content_id"]
        if cid not in content_map:
            content_map[cid] = {"title": node["title"], "content_id": cid}
        content_map.update(collect_content_map(node["children"]))
    return content_map


def write_search_index(output_dir: Path, positions: dict) -> None:
    """Write content_id → tree positions map for search result linking."""
    (output_dir / "search-positions.json").write_text(
        json.dumps(positions, indent=2) + "\n", encoding="utf-8"
    )


def write_config_toml(output_dir: Path, project_name: str) -> None:
    config_path = output_dir / "config.toml"
    if config_path.exists():
        return

    config_path.write_text(
        f'format_version = "2.0"\n'
        f'project_name = "{project_name}"\n'
        f'default_language = "eng"\n'
        f'languages = ["eng"]\n'
        f"\n"
        f"[pictures]\n"
        f'local_dir = "media/pictures"\n'
        f"\n"
        f"[audio]\n"
        f'local_dir = "media/audio"\n'
        f'formats = ["mp3", "ogg"]\n'
        f"\n"
        f"[video]\n"
        f'local_dir = "media/video"\n'
        f'formats = ["mp4", "webm"]\n',
        encoding="utf-8",
    )


def load_build_config() -> dict:
    """Load build.toml if it exists, return defaults otherwise."""
    config_path = Path("build.toml")
    if config_path.exists() and tomllib:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    return {"vault_path": "wiki", "output_dir": "output"}


def parse_roots_from_index(vault_path: Path, vault: dict[str, Path], config: dict | None = None) -> list[tuple[str, Path | None]]:
    """Parse root notes from wiki/index.md.

    Roots are the first [[wikilink]] on each non-indented list item
    that appears directly under a ## heading (before any --- separator).
    """
    skip_prefixes = (config or {}).get("skip_prefixes", ["Sources/", "source"])
    exclude_roots = (config or {}).get("exclude_roots", [])

    index_path = vault_path / "index.md"
    if not index_path.exists():
        return []

    text = index_path.read_text(encoding="utf-8")
    roots = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = True
            continue
        if line.startswith("---"):
            in_section = False
            continue
        if not in_section:
            continue
        if line.startswith("- [[") and not line.startswith("  "):
            match = WIKILINK_RE.search(line)
            if not match:
                continue
            link = match.group(1)
            if any(link.startswith(p) for p in skip_prefixes):
                continue
            name, path = resolve_link(link, vault)
            if path and name not in exclude_roots and name not in [r[0] for r in roots]:
                roots.append((name, path))
    return roots


def write_multi_position_log(output_dir: Path, positions: dict, content_map: dict) -> None:
    """Write redirects.toml into output so AI agents and apps can read it."""
    multi = {cid: pos for cid, pos in positions.items() if len(pos) > 1}
    if not multi:
        log_path = output_dir / "redirects.toml"
        if log_path.exists():
            log_path.unlink()
        return

    lines = [
        "# Auto-generated by build_navtree.py — do not edit manually.",
        "# Lists notes that appear at multiple positions in the navigation tree.",
        "# If restructuring links to these notes, all positions are affected.",
        "",
    ]
    for cid, pos_list in sorted(multi.items()):
        title = content_map.get(cid, {}).get("title", cid)
        tree_ids = [p["tree_id"] for p in pos_list]
        lines.append("[[multi_position]]")
        lines.append(f'content = "{title}"')
        lines.append(f'content_id = "{cid}"')
        quoted = ", ".join(f'"{t}"' for t in tree_ids)
        lines.append(f"positions = [{quoted}]")
        lines.append(f'primary = "{tree_ids[0]}"')
        lines.append("")

    (output_dir / "redirects.toml").write_text("\n".join(lines), encoding="utf-8")


def validate_changelog(vault_path: Path, vault: dict[str, Path]) -> list[str]:
    """Validate vault-changelog.toml entries against current vault state.

    Returns a list of warning messages for unresolved references.
    """
    changelog_path = vault_path / "vault-changelog.toml"
    if not changelog_path.exists() or not tomllib:
        return []

    with open(changelog_path, "rb") as f:
        changelog = tomllib.load(f)

    warnings = []
    for entry in changelog.get("change", []):
        change_type = entry.get("type", "")
        note = entry.get("note", "")
        new_name = entry.get("new_name")
        slug = slugify(note)

        if change_type == "rename":
            if not new_name:
                warnings.append(f"Rename entry for '{note}' missing new_name")
            elif not find_vault_source(slugify(new_name), vault):
                warnings.append(f"Renamed note '{new_name}' (from '{note}') not found in vault")
        elif change_type == "delete":
            if find_vault_source(slug, vault):
                warnings.append(f"Note '{note}' marked as deleted but still exists in vault")
        elif change_type in ("restructure", "split"):
            if not find_vault_source(slug, vault):
                warnings.append(f"Note '{note}' ({change_type}) not found in vault")

    return warnings


def archive_changelog(vault_path: Path) -> None:
    """Move processed changelog entries to vault-changelog.archive.toml."""
    changelog_path = vault_path / "vault-changelog.toml"
    if not changelog_path.exists():
        return

    archive_path = vault_path / "vault-changelog.archive.toml"
    content = changelog_path.read_text(encoding="utf-8")

    if archive_path.exists():
        existing = archive_path.read_text(encoding="utf-8")
        archive_path.write_text(existing + "\n" + content, encoding="utf-8")
    else:
        archive_path.write_text(content, encoding="utf-8")

    changelog_path.unlink()


def count_nodes(nodes: list[dict]) -> int:
    return sum(1 + count_nodes(n["children"]) for n in nodes)


def count_redirects(nodes: list[dict]) -> int:
    count = 0
    for node in nodes:
        if node.get("redirect_to"):
            count += 1
        count += count_redirects(node["children"])
    return count


def main():
    config = load_build_config()
    vault_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(config.get("vault_path", "wiki"))
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(config.get("output_dir", "output"))

    vault = load_vault(vault_path)
    roots_from_index = parse_roots_from_index(vault_path, vault, config)

    if not roots_from_index:
        print("No roots found in index.md, falling back to command line args")
        root_names = sys.argv[3:] if len(sys.argv) > 3 else []
        if not root_names:
            print("Usage: build_navtree.py [vault_path] [output_dir] [root1] [root2] ...")
            sys.exit(1)
        roots_from_index = [(name, vault.get(name)) for name in root_names]

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    skip_prefixes = config.get("skip_prefixes", ["Sources/", "source"])
    global_visited = set()
    content_id_primary = {}
    root_nodes = []
    root_counter = {"n": 0}
    for root_name, root_path in roots_from_index:
        node = build_tree(
            root_name, vault, global_visited, "", root_counter,
            filepath=root_path, skip_prefixes=skip_prefixes,
            content_id_primary=content_id_primary,
            is_root=True,
        )
        if node:
            root_nodes.append(node)

    changelog_warnings = validate_changelog(vault_path, vault)
    if changelog_warnings:
        print("Changelog warnings:")
        for w in changelog_warnings:
            print(f"  WARNING: {w}")

    write_hierarchical_tree(output_dir, root_nodes, vault)

    positions = collect_tree_positions(root_nodes)
    write_search_index(output_dir, positions)

    write_config_toml(output_dir, vault_path.name)

    content_map = collect_content_map(root_nodes)
    write_multi_position_log(output_dir, positions, content_map)

    archive_changelog(vault_path)

    total = count_nodes(root_nodes)
    redirects = count_redirects(root_nodes)
    unique_content = len(content_map)
    multi_position = sum(1 for v in positions.values() if len(v) > 1)
    print(f"NavTree v2 output written to {output_dir}/")
    print(f"  {total} tree nodes ({redirects} redirects), {unique_content} unique content pieces, {len(root_nodes)} root(s)")
    print(f"  {multi_position} content pieces appear in multiple tree positions")
    for r in root_nodes:
        child_count = count_nodes(r["children"])
        redir = " (redirect)" if r.get("redirect_to") else ""
        print(f"  - [{r['id']}] {r['title']} ({child_count} children){redir}")


if __name__ == "__main__":
    main()
