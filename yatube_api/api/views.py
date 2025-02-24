from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """Получаем посты."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого поста запрещено!'
            )
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление чужого поста запрещено!'
            )
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Получаем группы."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Получаем комментарии."""

    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого комментария запрещено!'
            )
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление чужого комментария запрещено!'
            )
        instance.delete()
