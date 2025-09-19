from django.urls import path

from . import views

app_name = 'aim_game'

urlpatterns = [
    path('', views.AimTrainerView.as_view(), name='home'),
    path('results/', views.GameResultCreateView.as_view(), name='results'),
    path('recent-results/', views.RecentResultsView.as_view(), name='recent_results'),
]
