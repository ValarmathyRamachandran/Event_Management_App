from django.urls import path
from events.views import EventsApiView

urlpatterns = [
    path('events/', EventsApiView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventsApiView.as_view(), name='event_operations'),
]