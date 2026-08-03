# Wielicka Sweet Home 3D CLI

This repository keeps a local copy of `sh3dkit` in `deps/sh3dkit` and uses a
Python environment under `deps/.venv`.

## Setup

Use Python 3.11 or newer:

```bash
./tools/setup.sh
```

To select a specific Python executable:

```bash
PYTHON=python3.13 ./tools/setup.sh
```

## Render a layout

```bash
./deps/.venv/bin/python tools/render_layout.py wielicka.sh3d -o out/wielicka.svg
```

The renderer reads the `.sh3d` archive directly and writes an SVG floor plan.
Generated renders belong in `out/` and are ignored by Git. The current layout
preview is shown below when the render has been generated locally:

![Wielicka layout](out/wielicka.svg)

The local virtual environment is also ignored and can be recreated with
`tools/setup.sh`. Before committing, make sure `wielicka.sh3d` still opens in
Sweet Home 3D and regenerate the preview in `out/`.
