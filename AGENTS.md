# Project instructions

## Sweet Home 3D workflow

- Treat `wielicka.sh3d` as the single source of truth for the layout. Make all
  layout changes by editing `wielicka.sh3d` only, and keep it a valid Sweet
  Home 3D archive that opens successfully in Sweet Home 3D after every change.
- Never edit SVG files by hand. SVG previews are generated artifacts and must
  only be produced by the renderer from `wielicka.sh3d`.
- Sweet Home 3D is open source. If the `.sh3d` format or the correct way to
  apply a layout change is unclear, find and consult the Sweet Home 3D source
  code rather than guessing or treating a generated preview as an input.
- Before every commit, render the current layout with
  `./deps/.venv/bin/python tools/render_layout.py wielicka.sh3d -o out/wielicka.svg`.
- Keep all generated renders and other preview artifacts under `out/`.
- Commit `out/wielicka.svg` so the README preview is visible on GitHub. Always
  regenerate it before committing changes.
- Keep the README's layout preview pointing to `out/wielicka.svg`, and verify
  that the preview is regenerated before committing.

## Change checklist

1. Make layout changes only in `wielicka.sh3d`; edit supporting tooling only
   when the requested change is specifically about that tooling.
2. Render the layout into `out/`.
3. Confirm the `.sh3d` file remains a readable ZIP archive and can be loaded by
   the local renderer.
4. Confirm the README preview points to the current render.
5. Review `git status` to ensure the current `out/wielicka.svg` is included
   when committing the layout preview update.
