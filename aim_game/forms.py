from django import forms

from .models import GameResult


class GameResultForm(forms.ModelForm):
    class Meta:
        model = GameResult
        fields = [
            'score',
            'kills',
            'accuracy',
            'avg_ttk',
            'max_combo',
            'misses',
            'difficulty',
        ]

    def clean_accuracy(self):
        accuracy = self.cleaned_data['accuracy']
        if not (0 <= accuracy <= 100):
            raise forms.ValidationError('Accuracy must be between 0 and 100.')
        return accuracy

    def clean_avg_ttk(self):
        avg_ttk = self.cleaned_data['avg_ttk']
        if avg_ttk < 0:
            raise forms.ValidationError('Average time to kill must be non-negative.')
        return avg_ttk
