import json
from pathlib import Path

from django.test import Client, TestCase
from django.urls import reverse

from .forms import GameResultForm
from .models import GameResult


class GameResultFormTests(TestCase):
    def test_form_accepts_valid_data(self):
        form = GameResultForm(
            data={
                'score': 1200,
                'kills': 12,
                'accuracy': 75.0,
                'avg_ttk': 450.5,
                'max_combo': 8,
                'misses': 4,
                'difficulty': GameResult.Difficulty.NORMAL,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_rejects_accuracy_out_of_bounds(self):
        form = GameResultForm(
            data={
                'score': 100,
                'kills': 1,
                'accuracy': 150,
                'avg_ttk': 500,
                'max_combo': 1,
                'misses': 0,
                'difficulty': GameResult.Difficulty.EASY,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('accuracy', form.errors)


class GameResultViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_payload = {
            'score': 900,
            'kills': 9,
            'accuracy': 60.0,
            'avg_ttk': 520.0,
            'max_combo': 6,
            'misses': 3,
            'difficulty': GameResult.Difficulty.HARD,
        }

    def test_submit_result_via_form(self):
        response = self.client.post(reverse('aim_game:results'), data=self.valid_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(GameResult.objects.count(), 1)

    def test_submit_result_via_json(self):
        response = self.client.post(
            reverse('aim_game:results'),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(GameResult.objects.count(), 1)

    def test_recent_results_endpoint(self):
        GameResult.objects.create(**self.valid_payload)
        response = self.client.get(reverse('aim_game:recent_results'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertGreaterEqual(len(data['results']), 1)



class AssetGenerationCommandTests(TestCase):
    def test_generate_target_assets_creates_assets(self):
        from django.conf import settings
        from django.core.management import call_command

        call_command('generate_target_assets', '--force')
        base_dir = Path(settings.BASE_DIR) / 'static' / 'aim_game'
        image_dir = base_dir / 'img'
        audio_dir = base_dir / 'audio'
        for name in ['easy', 'normal', 'hard']:
            self.assertTrue((image_dir / f'target_{name}.png').exists())
        for name in ['hit', 'critical', 'miss']:
            self.assertTrue((audio_dir / f'{name}.wav').exists())
