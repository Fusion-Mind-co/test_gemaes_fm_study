import math
import os
import struct
import wave
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pygame
from django.conf import settings
from django.core.management.base import BaseCommand

from aim_game.presets import DIFFICULTY_PRESETS


Harmonic = Tuple[float, float]


class Command(BaseCommand):
    help = 'Generate target sprite images and audio cues for each difficulty.'

    AUDIO_SPECS: Dict[str, Dict[str, object]] = {
        'hit': {
            'frequency': 880.0,
            'duration': 0.16,
            'volume': 0.45,
            'attack': 0.006,
            'release': 0.08,
            'harmonics': [(1.5, 0.35), (2.0, 0.18)],
        },
        'critical': {
            'frequency': 1200.0,
            'duration': 0.22,
            'volume': 0.5,
            'attack': 0.004,
            'release': 0.12,
            'harmonics': [(1.33, 0.4), (2.0, 0.2)],
        },
        'miss': {
            'frequency': 320.0,
            'duration': 0.2,
            'volume': 0.38,
            'attack': 0.008,
            'release': 0.09,
            'harmonics': [(2.0, 0.1)],
        },
        'finish': {
            'frequency': 520.0,
            'duration': 0.9,
            'volume': 0.55,
            'attack': 0.02,
            'release': 0.4,
            'harmonics': [(1.5, 0.35), (2.0, 0.25), (2.5, 0.15)],
        },
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate assets even if files already exist.',
        )

    def handle(self, *args, **options):
        force = options['force']
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        pygame.init()
        try:
            image_dir = Path(settings.BASE_DIR) / 'static' / 'aim_game' / 'img'
            audio_dir = Path(settings.BASE_DIR) / 'static' / 'aim_game' / 'audio'
            image_dir.mkdir(parents=True, exist_ok=True)
            audio_dir.mkdir(parents=True, exist_ok=True)

            generated_images = self._generate_images(image_dir, force)
            generated_audio = self._generate_audio(audio_dir, force)

            if generated_images:
                self.stdout.write(self.style.SUCCESS(f'Generated images: {", ".join(generated_images)}'))
            else:
                self.stdout.write(self.style.NOTICE('No images generated (use --force to overwrite).'))

            if generated_audio:
                self.stdout.write(self.style.SUCCESS(f'Generated audio: {", ".join(generated_audio)}'))
            else:
                self.stdout.write(self.style.NOTICE('No audio generated (use --force to overwrite).'))
        finally:
            pygame.quit()

    def _generate_images(self, target_dir: Path, force: bool) -> Iterable[str]:
        generated: list[str] = []
        for key, preset in DIFFICULTY_PRESETS.items():
            path = target_dir / f'target_{key}.png'
            if path.exists() and not force:
                continue
            surface = self._create_surface(preset.radius)
            self._draw_target(surface, preset.radius, preset.critical_threshold_px)
            pygame.image.save(surface, path.as_posix())
            generated.append(path.name)
        return generated

    def _generate_audio(self, audio_dir: Path, force: bool) -> Iterable[str]:
        generated: list[str] = []
        for name, spec in self.AUDIO_SPECS.items():
            path = audio_dir / f'{name}.wav'
            if path.exists() and not force:
                continue
            self._write_tone(path, **spec)
            generated.append(path.name)
        return generated

    def _create_surface(self, radius: int) -> 'pygame.Surface':
        size = radius * 2
        return pygame.Surface((size, size), pygame.SRCALPHA)

    def _draw_target(self, surface: 'pygame.Surface', radius: int, core_radius: int) -> None:
        center = radius
        base_color = pygame.Color(244, 67, 54, 255)
        edge_color = pygame.Color(255, 205, 210, 235)

        for r in range(radius, 0, -1):
            blend = r / radius
            color = base_color.lerp(edge_color, 1 - blend)
            pygame.draw.circle(surface, color, (center, center), r)

        pygame.draw.circle(surface, pygame.Color(255, 255, 255, 240), (center, center), max(core_radius, 1))

    def _write_tone(
        self,
        path: Path,
        *,
        frequency: float,
        duration: float,
        volume: float,
        attack: float = 0.005,
        release: float = 0.05,
        harmonics: List[Harmonic] | None = None,
        sample_rate: int = 44100,
    ) -> None:
        n_samples = int(duration * sample_rate)
        amplitude = max(0.0, min(volume, 1.0)) * 32767
        harmonics = harmonics or []

        with wave.open(str(path), 'w') as wav_file:
            wav_file.setparams((1, 2, sample_rate, n_samples, 'NONE', 'not compressed'))
            for i in range(n_samples):
                t = i / sample_rate
                envelope = self._envelope(t, duration, attack, release)
                base = math.sin(2 * math.pi * frequency * t)
                partials = sum(
                    weight * math.sin(2 * math.pi * frequency * multiple * t)
                    for multiple, weight in harmonics
                )
                value = (base + partials) * envelope
                value = max(-1.0, min(1.0, value))
                sample = int(amplitude * value)
                wav_file.writeframes(struct.pack('<h', sample))

    def _envelope(self, t: float, duration: float, attack: float, release: float) -> float:
        attack = max(attack, 0.0)
        release = max(release, 0.0)
        sustain_time = max(duration - attack - release, 0.0)

        if t < attack:
            return t / attack if attack > 0 else 1.0
        if t < attack + sustain_time:
            return 1.0
        remaining = duration - t
        if release > 0:
            return max(0.0, remaining / release)
        return 0.0

