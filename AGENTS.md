# Project instructions

## Sweet Home 3D workflow

- Treat `wielicka.sh3d` as the only source of truth for the layout. Keep it a
  valid Sweet Home 3D archive that opens successfully in Sweet Home 3D after
  every change.
- Make every layout change in `wielicka.sh3d` first. Never hand-edit a render
  independently of the SH3D source.
- Before every commit, render the current layout with
  `./deps/.venv/bin/python tools/render_layout.py wielicka.sh3d -o out/wielicka.svg`.
- Keep all generated renders and other preview artifacts under `out/`.
- Commit `out/wielicka.svg` so the README preview is visible on GitHub. Always
  regenerate it before committing changes.
- Keep the README's layout preview pointing to `out/wielicka.svg`, and verify
  that the preview is regenerated before committing.

## Change checklist

1. Make the change to `wielicka.sh3d` or the supporting tooling.
2. Render the layout into `out/` from `wielicka.sh3d`.
3. Confirm the `.sh3d` file remains a readable ZIP archive and can be loaded by
   the local renderer.
4. Confirm the README preview points to the current render.
5. Review `git status` to ensure the current `out/wielicka.svg` is included
   when committing the layout preview update.
