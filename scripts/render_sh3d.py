#!/usr/bin/env python3
"""Render the wall outline stored in a Sweet Home 3D file to SVG."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


def number(value: float) -> str:
    return f"{value:g}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    with zipfile.ZipFile(args.source) as archive:
        home = ET.fromstring(archive.read("Home.xml"))

    walls = home.findall("wall")
    if len(walls) != 4:
        raise ValueError(f"Expected four walls, found {len(walls)}")

    points = [
        (float(wall.attrib["xStart"]), float(wall.attrib["yStart"]))
        for wall in walls
    ]
    end = (
        float(walls[-1].attrib["xEnd"]),
        float(walls[-1].attrib["yEnd"]),
    )
    if end != points[0]:
        raise ValueError("Walls don't form a closed outline")

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width, height = max_x - min_x, max_y - min_y
    if sorted((width, height)) != [300.0, 400.0]:
        raise ValueError(f"Expected a 3 × 4 m rectangle, found {width} × {height} cm")

    thickness = float(walls[0].attrib["thickness"])
    margin = 36.0
    view_x = min_x - thickness / 2 - margin
    view_y = min_y - thickness / 2 - margin
    view_width = width + thickness + 2 * margin
    view_height = height + thickness + 2 * margin
    polygon = " ".join(f"{number(x)},{number(y)}" for x, y in points)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="{number(view_x)} {number(view_y)} {number(view_width)} {number(view_height)}"
  width="{number(view_width)}" height="{number(view_height)}" data-source="{args.source.name}">
  <rect x="{number(view_x)}" y="{number(view_y)}" width="{number(view_width)}" height="{number(view_height)}" fill="#fff"/>
  <polygon points="{polygon}" fill="#f8f8f8" stroke="#111" stroke-width="{number(thickness)}" stroke-linejoin="miter"/>
  <text x="{number(center_x)}" y="{number(min_y - 14)}" text-anchor="middle" font-family="sans-serif" font-size="16">3 m</text>
  <text x="{number(max_x + 22)}" y="{number(center_y)}" text-anchor="middle" font-family="sans-serif" font-size="16" transform="rotate(90 {number(max_x + 22)} {number(center_y)})">4 m</text>
</svg>
"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
