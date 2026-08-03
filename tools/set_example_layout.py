#!/usr/bin/env python3
"""Replace the example project with a simple 5 m by 5 m room."""

from __future__ import annotations

import argparse
import zipfile
import struct
import xml.etree.ElementTree as ET
from pathlib import Path


SIDE = 500.0  # Sweet Home 3D stores dimensions in centimetres.
POINTS = ((0.0, 0.0), (SIDE, 0.0), (SIDE, SIDE), (0.0, SIDE))
WALL_ENDPOINTS = tuple(
    (POINTS[index], POINTS[(index + 1) % 4]) for index in range(4)
) + (((0.0, 0.0), (0.0, 0.0)),) * 2
WALL_COORDINATE_OFFSETS = (6160, 6410, 6515, 6620, 6725, 6830)


def update_binary(home_data: bytes) -> bytes:
    updated = bytearray(home_data)
    for offset, (start, end) in zip(WALL_COORDINATE_OFFSETS, WALL_ENDPOINTS):
        values = (end[0], start[0], end[1], start[1])
        for value in values:
            updated[offset : offset + 4] = struct.pack(">f", value)
            offset += 4
    return bytes(updated)


def update_xml(xml_data: bytes) -> bytes:
    root = ET.fromstring(xml_data)
    old_walls = root.findall("wall")
    if len(old_walls) < 6:
        raise ValueError("Home.xml must contain at least six walls")

    for wall in old_walls:
        root.remove(wall)

    wall_ids = [wall.get("id") for wall in old_walls[:6]]
    for index, wall_id in enumerate(wall_ids):
        start, end = WALL_ENDPOINTS[index]
        wall = ET.Element(
            "wall",
            {
                "id": wall_id or f"wall-example-{index + 1}",
                "wallAtStart": wall_ids[index - 1] or f"wall-example-{index}" if index else wall_ids[-1] or "wall-example-6",
                "wallAtEnd": wall_ids[(index + 1) % 6] or f"wall-example-{(index + 1) % 6 + 1}",
                "xStart": str(start[0]),
                "yStart": str(start[1]),
                "xEnd": str(end[0]),
                "yEnd": str(end[1]),
                "height": "250.0",
                "thickness": "7.5",
                "pattern": "hatchUp",
            },
        )
        root.append(wall)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def replace_archive(path: Path) -> None:
    with zipfile.ZipFile(path, "r") as source:
        entries = {name: source.read(name) for name in source.namelist()}

    entries["Home"] = update_binary(entries["Home"])
    entries["Home.xml"] = update_xml(entries["Home.xml"])

    temporary_path = path.with_suffix(".tmp.sh3d")
    with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as target:
        for name, data in entries.items():
            target.writestr(name, data)
    temporary_path.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    replace_archive(parser.parse_args().project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
