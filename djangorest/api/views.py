# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import generics, permissions
# from rest_framework import permissions

from .serializers import BucketlistSerializer, UserSerializer
from .models import Bucketlist
from .permissions import IsOwner

# Create your views here.

class CreateView(generics.ListCreateAPIView):
	queryset = Bucketlist.objects.all()
	serializer_class = BucketlistSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwner)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Bucketlist.objects.all()
	serializer_class = BucketlistSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwner)

class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer