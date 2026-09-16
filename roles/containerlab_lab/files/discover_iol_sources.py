#!/usr/bin/env python3
"""Discover supported Cisco IOL-XE build sources in one local directory."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml


ARCHIVE_PATTERN = re.compile(
    r"^(?P<family>iol|ioll2)-xe-(?P<version>[0-9]+(?:-[0-9]+)+)\.tar\.gz$"
)
DEFINITION_IDS = {
    "iol-xe": ("l3", "iol-xe-"),
    "ioll2-xe": ("l2", "ioll2-xe-"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_record(path: Path, version: str, image_type: str, source_format: str) -> dict:
    return {
        "kind": "cisco_iol",
        "source": str(path),
        "version": version,
        "type": image_type,
        "format": source_format,
        "authorised_use": True,
        "sha256": sha256(path),
    }


def discover_archives(root: Path) -> list[dict]:
    records = []
    for path in sorted(root.glob("*.tar.gz")):
        match = ARCHIVE_PATTERN.fullmatch(path.name)
        if match is None:
            continue
        image_type = "l2" if match.group("family") == "ioll2" else "l3"
        version = match.group("version").replace("-", ".")
        records.append(build_record(path, version, image_type, "oci_archive"))
    return records


def discover_binaries(root: Path) -> list[dict]:
    records = []
    for definition_path in sorted((*root.glob("*.yaml"), *root.glob("*.yml"))):
        definition = yaml.safe_load(definition_path.read_text(encoding="utf-8"))
        if not isinstance(definition, dict):
            continue

        node_definition_id = str(definition.get("node_definition_id", "")).strip()
        if node_definition_id not in DEFINITION_IDS:
            continue

        image_type, identifier_prefix = DEFINITION_IDS[node_definition_id]
        identifier = str(definition.get("id", "")).strip()
        if not identifier.startswith(identifier_prefix):
            raise ValueError(
                f"{definition_path.name}: id must begin with {identifier_prefix}"
            )

        version_text = identifier.removeprefix(identifier_prefix)
        if re.fullmatch(r"[0-9]+(?:-[0-9]+)+", version_text) is None:
            raise ValueError(f"{definition_path.name}: id does not contain a valid version")

        disk_image = str(definition.get("disk_image", "")).strip()
        if not disk_image or Path(disk_image).name != disk_image:
            raise ValueError(
                f"{definition_path.name}: disk_image must name a file in the same directory"
            )

        source = root / disk_image
        if not source.is_file():
            raise ValueError(
                f"{definition_path.name}: referenced binary is missing: {disk_image}"
            )

        version = version_text.replace("-", ".")
        records.append(build_record(source, version, image_type, "binary"))
    return records


def discover(root: Path) -> list[dict]:
    if not root.is_absolute():
        raise ValueError("image directory must be an absolute path")
    if not root.is_dir():
        raise ValueError(f"image directory does not exist: {root}")

    records = discover_archives(root) + discover_binaries(root)
    if not records:
        raise ValueError(
            "no supported IOL-XE sources found; keep each loose CML binary with "
            "its image-definition YAML, or use a standard iol-xe/ioll2-xe OCI archive name"
        )

    unique = {}
    for record in records:
        identity = (record["type"], record["version"])
        previous = unique.get(identity)
        if previous is not None and previous["source"] != record["source"]:
            raise ValueError(
                f"duplicate {record['type']} version {record['version']} sources: "
                f"{previous['source']} and {record['source']}"
            )
        unique[identity] = record
    return [unique[identity] for identity in sorted(unique)]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: discover_iol_sources.py IMAGE_DIRECTORY", file=sys.stderr)
        return 2
    try:
        records = discover(Path(sys.argv[1]).expanduser())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(records, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
