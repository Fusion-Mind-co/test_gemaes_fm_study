from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class DifficultyPreset:
    radius: int
    spawn_interval_ms: Tuple[int, int]
    lifetime_ms: int
    speed: Tuple[int, int]
    max_concurrent: int
    critical_threshold_px: int


DIFFICULTY_PRESETS: Dict[str, DifficultyPreset] = {
    'easy': DifficultyPreset(
        radius=28,
        spawn_interval_ms=(800, 1000),
        lifetime_ms=1600,
        speed=(0, 60),
        max_concurrent=3,
        critical_threshold_px=6,
    ),
    'normal': DifficultyPreset(
        radius=22,
        spawn_interval_ms=(600, 800),
        lifetime_ms=1300,
        speed=(60, 120),
        max_concurrent=4,
        critical_threshold_px=4,
    ),
    'hard': DifficultyPreset(
        radius=16,
        spawn_interval_ms=(400, 600),
        lifetime_ms=1000,
        speed=(120, 180),
        max_concurrent=5,
        critical_threshold_px=3,
    ),
}
