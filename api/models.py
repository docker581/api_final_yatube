from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    title = models.TextField()
    
    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text[:10]   


class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )

    class Meta:
        models.UniqueConstraint(
            fields=['following', 'user'],
            name='following_user',
        )
    
    def __str__(self):
        return self.following.username
