from django.urls import path
from .views import get_categories, get_events, get_events_and_push_to_db, get_events_by_id

urlpatterns = [
    path('', get_events_and_push_to_db, name='get_eventos'),
    path('events', get_events, name='get_events'),
    path('events/<str:event_id>', get_events_by_id, name='get_events_by_id'),
    path('categories', get_categories, name='get_categories'),
]