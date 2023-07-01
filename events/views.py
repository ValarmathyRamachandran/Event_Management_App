from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from accounts.models import User
from .serializers import EventSerializer, TicketSerializer
from rest_framework import permissions
from .models import Event, Ticket
from rest_framework import generics
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
                return Response({ 'message': 'all events displayed successfully','code':200,'data': event_s.data})
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
                data = {"event":event_id, "user":user.id,"quantity":1}
                serializer = TicketSerializer(data=data)  
           
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message':"Ticket for an event was successfully Booked","code":201,"data":"test"})
            return Response({'message':'Invalid credentials','code':400})
        except Exception as e:
            return Response({'message':'OOps! Something went worng,Please try again later','code':416,'error':str(e)})
