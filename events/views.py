from datetime import datetime
from selectors import EVENT_WRITE
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from accounts.models import User
from .serializers import EventSerializer, TicketSerializer
from rest_framework import permissions
from .models import Event, Ticket
from accounts.views import User
from events.serializers import EventSerializer


class EventsApiView(APIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """
        method is used to Add events by admin
        """
        try:
            if request.user.is_admin:
                event = EventSerializer(data=request.data)
                event.is_valid(raise_exception=True)
                event.save()
                return Response({'message': 'Event was successfully created','code':200,'data': event.data})
            return Response({'message': "Only Admin can perform this action",'code':400})
        except Exception as e:
            return Response({'message': "Error creating event",'code':500,'error': str(e)})
        

    def get(self, request):
        """
        Get method is used to get all events and user details
        """
        try:
            user = request.user
            if user.is_admin:
                all_events = Event.objects.all()
                event_s = EventSerializer(all_events, many=True)
                return Response({ 'message': 'all events displayed successfully','code':200,'data': event_s.data})
            return Response({'message':'Only Admin can perform this action','code':400})
        except Exception as e:
            return Response({'message':'OOps! Something went worng,Please try again later','code':416,'error':str(e)})

    def patch(self, request, pk):
        """
        Update method is used to update events by id
        """
        user = request.user
        try:
            if user.is_admin:
                event = Event.objects.get(pk=pk)
                event = EventSerializer(event, request.data, partial=True)
                event.is_valid(raise_exception=True)
                event.save()
                return Response({'message':'events were updated successfully','code':200,'data':event.data})
            return Response({'message':'Invalid Entry','code':400})
        except Exception as e:
            return Response({'message':'OOps! Something went worng,Please try again later','code':416,'error':str(e)})


    def delete(self, request, pk):
        """
        Delete method is used to delete event by id
        """
        user = request.user
        try:
            if user.is_admin:
                event = Event.objects.get(pk=pk)
                event.is_delete = True
                event.save()
                return Response({'message':'events were deleted successfully','code':200,'data':event.is_delete})
            return Response({'message':'Only Admin have the access to delete it','code':400})
        except Exception as e:
            return Response({'message':'OOps! Something went worng,Please try again later','code':416,'error':str(e)})

class EventSummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get summary of events for admin users.
        """
        try:
            user = request.user
            if user.is_admin:
                total_events = Event.objects.count()
                total_users = User.objects.count()
                return Response({'message': 'Event summary view displayed successfully','code': 200,
                'data': {'total_events': total_events, 'total_users': total_users}})
            return Response({'message': 'Only Admin can perform this action', 'code': 400})
        except Exception as e:
            return Response({'message': 'Oops! Something went wrong. Please try again later', 'code': 416, 'error': str(e)})

class ListEvents(APIView):
    def get(self, request):
        try:
            user = request.user
            if user:
                all_events = Event.objects.all()
                event_s = EventSerializer(all_events, many=True)
                return Response({ 'message': 'List of events displayed successfully','code':200,'data': event_s.data})
            return Response({'message':'Invalid Entry','code':400})
        except Exception as e:
            return Response({'message':'OOps! Something went worng,Please try again later','code':416,'error':str(e)})

class BookTicketAPIView(APIView):
    serializer_class = TicketSerializer
    def post(self, request):
        try:
            user = request.user
            if user:
                event_id = request.data.get('event_id')
                event = Event.objects.get(pk=event_id)

                 # Check if the booking window is open
                current_time = datetime.now()
                if current_time < event.booking_start_time or current_time > event.booking_end_time:
                    return Response({'message': 'Booking is closed for this event', 'code': 400})

                # Check if the user has already booked tickets for an event
                if Ticket.objects.filter(event_id=event_id, user=user).exists():
                    return Response({'message': 'You have already booked Tickets for this event', 'code': 400})
                
                # Check if the user will exceed the maximum seats
                total_tickets = Ticket.objects.filter(event=event).count()
                if total_tickets >= EVENT_WRITE.max_seats:
                    return Response({'message': 'Maximum seats reached for this event', 'code': 400})


                data = {"event":event_id, "user":user.id,"quantity":1}
                serializer = TicketSerializer(data=data)  
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message':"Ticket for an event was successfully Booked","code":201,"data":serializer.data})
            return Response({'message':'Invalid credentials','code':400})
        except Exception as e:
            return Response({'message':'OOps! Something went worng,Please try again later','code':416,'error':str(e)})


    def get(self, request):
        try:
            user = request.user
            if user:
                user = request.user
                tickets = Ticket.objects.filter(user=user)
                serializer = TicketSerializer(tickets, many=True)
                return Response({'message': 'Tickets displayed successfully', 'code': 200, 'data': serializer.data})
            return Response({'message':'Invalid credentials','code':400})
        except Exception as e:
            return Response({'message': 'An error occurred while retrieving booked events. Please try again later.', 'code': 500, 'error': str(e)})


class BookedEventsAPIView(APIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            tickets = Ticket.objects.filter(user=user)
            event_ids = tickets.values_list('event_id', flat=True)

            events = Event.objects.filter(id__in=event_ids).order_by('start_date')
            serializer = EventSerializer(events, many=True)
            return Response({'message': 'Registered events retrieved successfully', 'code': 200, 'data': serializer.data})
        except Exception as e:
            return Response({'message': 'Error: Unable to retrieve booked events. Please check your network connection and try again.', 'code': 500, 'error': str(e)})


class CancelTicketAPIView(APIView):
    def post(self, request):
        try:
            ticket_id = request.data.get('ticket_id')

            if not ticket_id:
                return Response({'message': 'Ticket ID is required', 'code': 400})

            ticket = Ticket.objects.get(pk=ticket_id)

            # Check if the ticket belongs to the requesting user
            if ticket.user != request.user:
                return Response({'message': 'You are not authorized to cancel this ticket', 'code': 401})

            # Check if the ticket is already cancelled
            if ticket.is_cancelled:
                return Response({'message': 'This ticket has already been cancelled', 'code': 400})

            ticket.is_cancelled = True
            ticket.save()

            return Response({'message': 'Ticket cancellation successful', 'code': 200})

        except Ticket.DoesNotExist:
            return Response({'message': 'Ticket not found', 'code': 404})

        except Exception as e:
            return Response({'message': 'Invalid Entry. Please try again later.', 'code': 500, 'error': str(e)})