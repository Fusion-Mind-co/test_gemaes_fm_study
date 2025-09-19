import json

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView

from .forms import GameResultForm
from .models import GameResult
from .presets import DIFFICULTY_PRESETS


class AimTrainerView(TemplateView):
    template_name = 'aim_game/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['difficulty_presets'] = DIFFICULTY_PRESETS
        return context


class GameResultCreateView(FormView):
    form_class = GameResultForm
    success_url = reverse_lazy('aim_game:home')
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        self.json_payload = None
        content_type = request.META.get('CONTENT_TYPE', '')
        if content_type.startswith('application/json'):
            try:
                raw_body = request.body.decode('utf-8') or '{}'
                self.json_payload = json.loads(raw_body)
            except json.JSONDecodeError:
                return JsonResponse({'errors': {'__all__': ['Invalid JSON payload.']}}, status=400)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.json_payload is not None:
            kwargs['data'] = self.json_payload
            kwargs['files'] = None
        return kwargs

    def form_valid(self, form):
        result = form.save()
        data = {
            'id': result.pk,
            'message': 'Result saved',
        }
        return JsonResponse(data, status=201)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class RecentResultsView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        results = GameResult.objects.order_by('-played_at')[:10]
        payload = [
            {
                'score': result.score,
                'kills': result.kills,
                'accuracy': result.accuracy,
                'avg_ttk': result.avg_ttk,
                'max_combo': result.max_combo,
                'misses': result.misses,
                'difficulty': result.get_difficulty_display(),
                'played_at': result.played_at.isoformat(),
            }
            for result in results
        ]
        return JsonResponse({'results': payload})
