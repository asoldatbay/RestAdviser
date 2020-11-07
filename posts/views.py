from rest_framework import generics
from posts.serializers import (
    PostDetailSerializer,
    PostsListSerializer,
    ReviewDetailSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from posts.models import Post
from posts.permissons import IsOwner
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (
        IsAuthenticated,
    )


class PostsListView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    permission_classes = (
        IsAuthenticated,
    )
    queryset = Post.objects.all()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    permission_classes = (
        IsOwner,
        IsAdminUser,
    )


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = (
        IsAuthenticated,
    )


class AllUserPostsView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    queryset = Post.objects.all()
    permission_classes = (
        IsAuthenticated,
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SearchView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = Post.objects.all()
    permission_classes = (
        AllowAny,
    )
    filter_fields = {
        'average_bill': ['gte', 'lte'],
        'average_rating': ['gte'],
    }
