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
BINARY_PATTERN = re.compile(
    r"^x86_64_crb_linux(?P<l2>_l2)?-[A-Za-z0-9][A-Za-z0-9._-]*$"
)
VERSION_PATTERN = re.compile(
    rb"(?<![0-9])B?(?P<version>(?:1[0-9]|2[0-9])\.[0-9]{1,2}\.[0-9]{1,2})(?![0-9])"
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


def inspect_binary(path: Path) -> None:
    with path.open("rb") as source:
        header = source.read(20)
    if (
        len(header) < 20
        or header[:4] != b"\x7fELF"
        or header[4] != 2
        or header[5] != 1
        or int.from_bytes(header[18:20], "little") != 62
    ):
        raise ValueError(f"{path.name}: expected a 64-bit x86 ELF binary")


def embedded_version(path: Path) -> str:
    overlap = b""
    with path.open("rb") as source:
        for block in iter(lambda: source.read(8 * 1024 * 1024), b""):
            content = overlap + block
            match = VERSION_PATTERN.search(content)
            if match is not None:
                return match.group("version").decode("ascii")
            overlap = content[-32:]
    raise ValueError(f"{path.name}: unable to determine the embedded IOS XE version")


def discover_binaries(root: Path) -> tuple[list[dict], set[Path]]:
    records = []
    referenced = set()
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
        referenced.add(source.resolve())
        records.append(build_record(source, version, image_type, "binary"))
    return records, referenced


def discover_unmapped_binaries(root: Path, referenced: set[Path]) -> list[dict]:
    records = []
    for path in sorted(root.iterdir()):
        if not path.is_file() or path.resolve() in referenced:
            continue
        match = BINARY_PATTERN.fullmatch(path.name)
        if match is None:
            continue
        inspect_binary(path)
        image_type = "l2" if match.group("l2") else "l3"
        records.append(
            build_record(path, embedded_version(path), image_type, "binary")
        )
    return records


def discover(root: Path) -> list[dict]:
    if not root.is_absolute():
        raise ValueError("image directory must be an absolute path")
    if not root.is_dir():
        raise ValueError(f"image directory does not exist: {root}")

    defined_binaries, referenced = discover_binaries(root)
    records = (
        discover_archives(root)
        + defined_binaries
        + discover_unmapped_binaries(root, referenced)
    )
    if not records:
        raise ValueError(
            "no supported IOL-XE sources found; use standard x86_64_crb_linux "
            "binary names, CML image-definition YAML, or iol-xe/ioll2-xe OCI archive names"
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
