from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

AMT_SIGN_TITLE = 30


class Group(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Наименование', unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title[:AMT_SIGN_TITLE]


class Post(models.Model):
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа'
    )

    class Meta:
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:AMT_SIGN_TITLE]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    text = models.TextField('Текст')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:AMT_SIGN_TITLE]
