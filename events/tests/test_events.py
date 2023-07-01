from django.test import TestCase
from rest_framework.test import APIRequestFactory,force_authenticate
from datetime import datetime
from django.utils import timezone
from accounts.models import User
from events.views import EventsApiView
from events.models import Event, Ticket
from events.serializers import EventSerializer, TicketSerializer


class EventsApiTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EventsApiView.as_view()
        self.user = User.objects.create_user(username='admin', password='admin123', is_admin=True)
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            start_date=datetime.now().date(),
            start_time=timezone.now().time(),
            location='Test Location',
            online=False,
            max_seats=10,
            booking_start_time=timezone.now(),
            booking_end_time=timezone.now() + timezone.timedelta(days=7)
        )
        self.data = {
            'title': 'New Event',
            'description': 'New Description',
            'start_date': datetime.now().date(),
            'start_time': timezone.now().time(),
            'location': 'New Location',
            'online': False,
            'max_seats': 10,
            'booking_start_time': timezone.now(),
            'booking_end_time': timezone.now() + timezone.timedelta(days=7)
        }

    def test_create_event(self):
        request = self.factory.post('/events/', self.data)
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Event was successfully created')
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(response.data['data']['title'], 'New Event')
        self.assertEqual(response.data['data']['description'], 'New Description')
      
        event = Event.objects.get(title='New Event')
        self.assertEqual(event.location, 'New Location')

    def test_get_all_events(self):
       
        request = self.factory.get('/events/')
        request.user = self.user
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'all events displayed successfully')
        self.assertEqual(response.data['code'], 200)
        self.assertEqual(len(response.data['data']), 1)  

