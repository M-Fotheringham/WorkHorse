"""Filename and text replacement helpers."""

from __future__ import annotations

import os
from pathlib import Path


def name_replacer(
    directory: str | os.PathLike[str],
    original_text: str,
    new_text: str,
    inside: bool = False,
) -> int:
    """Replace text in file names under ``directory``.

    Args:
        directory: Folder to search recursively.
        original_text: Text to replace in file names and optionally file contents.
        new_text: Replacement text.
        inside: When true, also replace text inside ``.txt`` files.

    Returns:
        Number of files renamed.

    Raises:
        ValueError: If ``original_text`` is empty.
        NotADirectoryError: If ``directory`` is not a valid directory.
        FileExistsError: If a replacement name would overwrite an existing file.
    """
    if not original_text:
        raise ValueError("original_text must not be empty")

    base = Path(directory)
    if not base.is_dir():
        raise NotADirectoryError(f"Not a directory: {base}")

    renamed = 0
    for path in base.rglob("*"):
        if not path.is_file():
            continue

        if inside and path.suffix.lower() == ".txt":
            content = path.read_text(encoding="utf-8")
            path.write_text(content.replace(original_text, new_text), encoding="utf-8")

        if original_text not in path.name:
            continue

        new_path = path.with_name(path.name.replace(original_text, new_text))
        if new_path.exists() and new_path != path:
            raise FileExistsError(f"Cannot rename {path} to {new_path}; target exists.")
        path.rename(new_path)
        renamed += 1

    return renamed
