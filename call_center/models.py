from django.db import models


class Comment(models.Model):
    text = models.TextField(blank=True, null=True)


class Status(models.Model):
    COMMENT_CHOICES = (
        ('status_1', 'Статус 1'),
        ('status_2', 'Статус 2'),
        ('status_3', 'Статус 3'),
    )
    title = models.CharField(choices=COMMENT_CHOICES, default='status_1', verbose_name='Статус')
