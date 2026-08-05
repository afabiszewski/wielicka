#!/usr/bin/env python3
"""Render a Sweet Home 3D project to SVG using the local sh3dkit copy."""

from __future__ import annotations

import argparse
import math
import re
import sys
from types import MethodType
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "deps" / "sh3dkit"))

from sh3d.FileLoader import FileLoader  # noqa: E402
from sh3d.model.Wall import Wall  # noqa: E402
from sh3dkit.renderer.SvgHomeRenderer import SvgHomeRenderer  # noqa: E402


def _safe_compute_intersection(self, point1, point2, point3, point4, limit):
    """Intersect wall-edge lines without slope singularities."""
    direction1_x = point2[0] - point1[0]
    direction1_y = point2[1] - point1[1]
    direction2_x = point4[0] - point3[0]
    direction2_y = point4[1] - point3[1]
    determinant = direction1_x * direction2_y - direction1_y * direction2_x

    if math.isclose(determinant, 0.0, abs_tol=1e-12):
        return

    offset_x = point3[0] - point1[0]
    offset_y = point3[1] - point1[1]
    distance = (offset_x * direction2_y - offset_y * direction2_x) / determinant
    x = point1[0] + distance * direction1_x
    y = point1[1] + distance * direction1_y

    if (point1[0] - x) ** 2 + (point1[1] - y) ** 2 < limit * limit:
        point1[0] = x
        point1[1] = y


Wall._compute_intersection = _safe_compute_intersection


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a .sh3d layout to SVG.")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("out/layout.svg"))
    parser.add_argument("-l", "--level-name", help="Render only this level.")
    args = parser.parse_args()

    input_path = args.input_file.resolve()
    output_path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with FileLoader(input_path) as file_loader:
        # Older/minimal Sweet Home 3D files may omit ContentDigests when they
        # contain no embedded furniture or textures. sh3d.py currently treats
        # that optional archive member as mandatory.
        if "ContentDigests" not in file_loader.zip_file.namelist():
            file_loader.asset_manager.load_assets = MethodType(lambda _self, _zip: None, file_loader.asset_manager)
        levels = list(file_loader.home.levels)
        if args.level_name:
            levels = [level for level in levels if level.name == args.level_name]
            if not levels:
                names = ", ".join(level.name for level in file_loader.home.levels)
                raise SystemExit(f"Level not found: {args.level_name}. Available: {names or '(none)'}")

        renderer = SvgHomeRenderer(file_loader.home)
        if levels:
            for level in levels:
                level.is_visible = True
                safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", level.name)
                level_output = output_path.with_name(f"{output_path.stem}_{safe_name}{output_path.suffix}")
                renderer.save_to_file(level_output, level)
                print(f"Rendered {input_path.name} -> {level_output}")
        else:
            renderer.save_to_file(output_path)
            print(f"Rendered {input_path.name} -> {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
