from django.db import models
from mainapp.managers.news_manager import NewsManager


class News(models.Model):
    objects = NewsManager()

    title = models.CharField(max_length=256, verbose_name='Title')
    preamble = models.CharField(max_length=1024, blank=True, null=True, verbose_name='P reamble')
    body = models.TextField(blank=False, null=False, verbose_name='Body')
    body_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Date of creating', editable=False)
    update_date = models.DateTimeField(auto_now=True, verbose_name='Date of editing', editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()


class SubNews(models.Model):
    body = models.TextField(blank=True, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
