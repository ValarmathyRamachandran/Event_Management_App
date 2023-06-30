from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django.views.decorators.csrf import csrf_exempt



class EventsApiView(APIView):
    def post(self, request):
        """
        method is used to Add events by admin
        """
        try:
            # if request.user:
            event = EventSerializer(data=request.data)
            event.is_valid(raise_exception=True)
            event.save()
            return Response({'message': 'Event was successfully created','code':200,'data': event.data})
            #return Response({'message': "Only Admin can perform this action",'code':400})
        except Exception as e:
            return Response({'message': "Error creating event",'code':500,'error': str(e)})
