# Project instructions

## Sweet Home 3D workflow

- All layout changes must be made only to `wielicka.sh3d`. Treat
  `wielicka.sh3d` as the single source of truth for the layout, and keep it a
  valid Sweet Home 3D archive that opens successfully in Sweet Home 3D after
  every change.
- The current layout in `wielicka.sh3d`, including its north orientation, is
  the agreed working layout. Never change its geometry, dimensions, wall
  positions, or north orientation automatically. Only change this layout when
  the user explicitly requests a layout change.
- SVG files are renderer output only. Never edit them directly; generate them
  with the renderer.
- Before every commit, render the current layout with
  `./deps/.venv/bin/python tools/render_layout.py wielicka.sh3d -o out/wielicka.svg`.
- Keep all generated renders and other preview artifacts under `out/`.
- Commit `out/wielicka.svg` so the README preview is visible on GitHub. Always
  regenerate it before committing changes.
- Keep the README's layout preview pointing to `out/wielicka.svg`, and verify
  that the preview is regenerated before committing.
- When a layout change is difficult to apply, consult the open-source Sweet
  Home 3D source code to understand the `.sh3d` format and apply the change to
  `wielicka.sh3d` directly.
- When creating a pull request, always embed the generated `out/wielicka.svg`
  in the pull request description.

## Change checklist

1. Make all layout changes only to `wielicka.sh3d`.
2. Render the layout into `out/`.
3. Confirm the `.sh3d` file remains a readable ZIP archive and can be loaded by
   the local renderer.
4. Confirm the README preview points to the current render.
5. Review `git status` to ensure the current `out/wielicka.svg` is included
   when committing the layout preview update.
6. Embed the generated `out/wielicka.svg` in the pull request description.
