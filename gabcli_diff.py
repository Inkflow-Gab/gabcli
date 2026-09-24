"""Colored, reviewable file-change previews for GabCli."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import List

from gabcli_ui import paint


@dataclass(frozen=True)
class DiffSummary:
    added: int
    removed: int

    @property
    def changed(self) -> bool:
        return bool(self.added or self.removed)

    def label(self) -> str:
        return f"+{self.added} -{self.removed}"


def make_unified_diff(old: str, new: str, display_path: str, context: int = 3) -> str:
    """Return a unified diff with Git-style headers."""
    before = old.splitlines(keepends=True)
    after = new.splitlines(keepends=True)
    lines = unified_diff(
        before,
        after,
        fromfile=f"a/{display_path}",
        tofile=f"b/{display_path}",
        n=context,
    )
    return "".join(lines)


def summarize(diff: str) -> DiffSummary:
    added = 0
    removed = 0
    for line in diff.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            removed += 1
    return DiffSummary(added=added, removed=removed)


def colorize_diff(diff: str, plain: bool = False) -> str:
    """Color additions green, removals red, and hunk headers cyan."""
    if plain:
        return diff
    rendered: List[str] = []
    for line in diff.splitlines(keepends=True):
        bare = line.rstrip("\r\n")
        ending = line[len(bare) :]
        if bare.startswith("+++"):
            rendered.append(paint(bare, "32", False) + ending)
        elif bare.startswith("---"):
            rendered.append(paint(bare, "31", False) + ending)
        elif bare.startswith("+"):
            rendered.append(paint(bare, "32", False) + ending)
        elif bare.startswith("-"):
            rendered.append(paint(bare, "31", False) + ending)
        elif bare.startswith("@@"):
            rendered.append(paint(bare, "36", False) + ending)
        else:
            rendered.append(paint(bare, "90", False) + ending)
    return "".join(rendered)


def limit_diff(diff: str, max_chars: int = 28_000) -> str:
    if len(diff) <= max_chars:
        return diff
    return diff[:max_chars] + f"\n... diff preview truncated at {max_chars:,} characters ...\n"
