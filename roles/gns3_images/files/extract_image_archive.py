#!/usr/bin/env python3
"""Extract a GNS3 image archive without allowing paths outside the target."""

from __future__ import annotations

import gzip
import shutil
import stat
import sys
import tarfile
import zipfile
from pathlib import Path


def _target(root: Path, member_name: str) -> Path:
    target = (root / member_name).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"archive member escapes the extraction root: {member_name}") from exc
    return target


def _extract_tar(source: Path, target: Path) -> None:
    with tarfile.open(source, "r:*") as archive:
        for member in archive.getmembers():
            _target(target, member.name)
            if member.issym() or member.islnk() or member.isdev():
                raise ValueError(f"unsupported archive member: {member.name}")
        archive.extractall(target)


def _extract_zip(source: Path, target: Path) -> None:
    with zipfile.ZipFile(source) as archive:
        for member in archive.infolist():
            _target(target, member.filename)
            if stat.S_ISLNK(member.external_attr >> 16):
                raise ValueError(f"unsupported archive member: {member.filename}")
        archive.extractall(target)


def _extract_gzip(source: Path, target: Path) -> None:
    output_name = source.name[:-3]
    if not output_name:
        raise ValueError("gzip image archive has no output filename")
    with gzip.open(source, "rb") as compressed, (target / output_name).open("wb") as output:
        shutil.copyfileobj(compressed, output)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: extract_image_archive.py SOURCE TARGET", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).resolve()
    target = Path(sys.argv[2]).resolve()
    target.mkdir(parents=True, exist_ok=True)
    try:
        if tarfile.is_tarfile(source):
            _extract_tar(source, target)
        elif zipfile.is_zipfile(source):
            _extract_zip(source, target)
        elif source.name.lower().endswith(".gz"):
            _extract_gzip(source, target)
        else:
            raise ValueError("unsupported image archive")
    except (OSError, tarfile.TarError, zipfile.BadZipFile, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
