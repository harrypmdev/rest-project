from django.db.models import Count
from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    ordering_fields= [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__folowed__created_at'
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile'
    ]

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')