from django.db import models


class FAQ(models.Model):
    question = models.CharField(max_length=256)
    answer = models.TextField()


class FeedBack(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    question = models.TextField()
