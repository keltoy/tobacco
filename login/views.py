from django.shortcuts import render
from django.contrib.auth.models import User, Group
from login.serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=False, methods=['post', 'get'])
    def is_admin(self, request):
        user = request.user
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
