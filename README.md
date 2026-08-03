# Wielicka Sweet Home 3D

![Wielicka layout](out/wielicka.svg?version=2)

## Weryfikacja projektu

Przed zatwierdzeniem zmian odśwież podgląd i sprawdź archiwum projektu:

```bash
./deps/.venv/bin/python tools/render_layout.py wielicka.sh3d -o out/wielicka.svg
python -m zipfile -t wielicka.sh3d
```

Plik `wielicka.sh3d` jest źródłem projektu, a `out/wielicka.svg` jego podglądem
wyświetlanym powyżej.
