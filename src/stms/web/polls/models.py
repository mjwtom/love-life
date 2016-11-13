from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class Quesion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    content = HTMLField()


class Choice(models.Model):
    question = models.ForeignKey(Quesion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
