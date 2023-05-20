from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album


class SongView(generics.ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        id = self.kwargs.get("pk")
        get_object_or_404(Album, pk=id)

        return self.queryset.filter(album_id=id)

    def perform_create(self, serializer):
        id = self.kwargs.get("pk")
        get_object_or_404(Album, pk=id)

        serializer.save(album_id=id)
