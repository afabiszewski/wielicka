# Project instructions

## Setup

Use Python 3.11 or newer:

```bash
./tools/setup.sh
```

To select a specific Python executable:

```bash
PYTHON=python3.13 ./tools/setup.sh
```

## Render the layout

```bash
./deps/.venv/bin/python tools/render_layout.py wielicka.sh3d -o out/wielicka.svg
```

The renderer reads the `.sh3d` archive directly and writes the committed SVG
preview used by the README.

## Before committing

1. Regenerate `out/wielicka.svg`.
2. Confirm `wielicka.sh3d` remains a readable Sweet Home 3D archive.
3. Confirm the README preview points to `out/wielicka.svg`.
4. Review `git status` and include the updated render in the commit.
