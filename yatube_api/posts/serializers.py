from rest_framework import serializers

from .models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор поста."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        read_only_fields = ('author', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор группы."""
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария к посту."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post', 'created')
