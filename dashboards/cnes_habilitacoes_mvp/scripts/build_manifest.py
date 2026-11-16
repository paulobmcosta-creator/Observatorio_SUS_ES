#!/usr/bin/env python3
"""Gera um manifesto SHA-256 deterministico do pacote distribuivel."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


EXCLUDED_PARTS = {".git", "node_modules", "__pycache__"}
EXCLUDED_NAMES = {".DS_Store", "MANIFESTO_PACOTE.sha256"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return (
        path.is_file()
        and not path.is_symlink()
        and not EXCLUDED_PARTS.intersection(relative.parts)
        and path.name not in EXCLUDED_NAMES
        and path.suffix not in EXCLUDED_SUFFIXES
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    output = (args.output or root / "MANIFESTO_PACOTE.sha256").resolve()
    entries = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if included(path, root):
            entries.append(f"{sha256(path)}  {path.relative_to(root).as_posix()}")

    output.write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(f"Manifesto gerado: {output} ({len(entries)} arquivos)")


if __name__ == "__main__":
    main()
