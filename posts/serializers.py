from rest_framework import serializers
from posts.models import Post, Review


class PostsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'header', 'average_bill', 'average_rating']


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
