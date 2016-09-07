from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import User
from api.serializers import UserTrackerSerializer

class UserTracker(APIView):

    def get_user(self, email):
        return User.objects.get_or_create(email=email)

    def post(self, request):
        serializer = UserTrackerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) and serializer.tracker_does_not_already_exist():
            serializer.create_tracker()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request):
        serializer = UserTrackerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.delete_tracker()
            return Response(serializer.data, status=status.HTTP_200_OK)
