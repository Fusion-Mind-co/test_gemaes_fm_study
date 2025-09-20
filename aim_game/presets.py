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
        radius=26,
        spawn_interval_ms=(700, 950),
        lifetime_ms=1500,
        speed=(40, 90),
        max_concurrent=3,
        critical_threshold_px=5,
    ),
    'hard': DifficultyPreset(
        radius=20,
        spawn_interval_ms=(550, 750),
        lifetime_ms=1350,
        speed=(80, 140),
        max_concurrent=4,
        critical_threshold_px=4,
    ),
}
