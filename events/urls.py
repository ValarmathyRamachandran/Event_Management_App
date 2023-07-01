from django.urls import path
from events.views import BookedEventsAPIView, CancelTicketAPIView, EventSummaryAPIView, EventsApiView, BookTicketAPIView

urlpatterns = [
    path('events/', EventsApiView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventsApiView.as_view(), name='event_operations'),
    path('events/summary/', EventSummaryAPIView.as_view(), name='event-summary-api'),
    path('events/book-ticket/', BookTicketAPIView.as_view(), name='book-ticket'),
    path('events/booked-events/', BookedEventsAPIView.as_view(), name='booked-events'),
    path('tickets/cancel/', CancelTicketAPIView.as_view(), name='cancel-ticket'),

]