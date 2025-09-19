# django_aim_trainer

Django-based aim trainer inspired by Valorant. The project serves a 2D mouse-aiming exercise with configurable difficulty presets and score tracking.

## Features
- Easy/Normal/Hard difficulty presets preconfigured with spawn, lifetime, speed, and size parameters.
- HTML-based UI with a canvas that renders the arena and targets, including dynamic background swaps and milestone burst effects by kill thresholds.
- Scoring rules that match the provided specification (base, critical, combo multiplier).
- Result submission endpoint for persisting metrics (score, kills, accuracy, avg_ttk, max_combo, misses, difficulty, played_at).
- Recent results JSON endpoint for dashboard/statistics overlays.
- Pygame-powered asset generation for consistent target sprites, background art, and audio cues.

## Getting Started

### Generate target, audio & background assets
Run `python manage.py generate_target_assets` to (re)build the sprite images under `static/aim_game/img/` and the sound cues under `static/aim_game/audio/`. Use `--force` to overwrite existing files. Custom background images can be dropped into `static/aim_game/img/backgrounds/` and referenced from `templates/aim_game/index.html`.

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Apply migrations via `python manage.py migrate`.
4. Run the development server with `python manage.py runserver` (or use `start_aim_trainer.bat`).
5. Access http://127.0.0.1:8000/ to launch the trainer UI.

## Development Notes
- Static assets live under `static/aim_game/` and templates under `templates/`.
- Difficulty presets are defined in `aim_game/presets.py` and injected into the landing page context.
- Result submissions expect POST requests to `/results/` with the fields defined in `GameResultForm`.

## Background Rotation
- Configure kill-threshold backgrounds in `templates/aim_game/index.html` under the `background-assets` script block.
- Thresholds are inclusive; the highest threshold less than or equal to the current kill count determines the active background.
- Sample arena images are provided under `static/aim_game/img/backgrounds/` for easy customization.

## Next Steps
- Build comprehensive tests for scoring logic and API endpoints.
- Add authentication if individual user tracking is required.
- Polish audio/visual feedback (e.g., alternative sound sets, particle effects).
