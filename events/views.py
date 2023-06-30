from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EventSerializer
from rest_framework import permissions
from .models import Event





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
        Get method is for get all Books and user details
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
