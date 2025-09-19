from django.db import models


class GameResult(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Easy'
        NORMAL = 'normal', 'Normal'
        HARD = 'hard', 'Hard'

    score = models.PositiveIntegerField()
    kills = models.PositiveIntegerField()
    accuracy = models.FloatField(help_text='Hit percentage as 0-100 value')
    avg_ttk = models.FloatField(help_text='Average time to kill in milliseconds')
    max_combo = models.PositiveIntegerField()
    misses = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=12, choices=Difficulty.choices)
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']

    def __str__(self) -> str:
        return f"{self.get_difficulty_display()} - {self.score} pts"
