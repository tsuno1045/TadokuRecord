from django.db import models
from django.conf import settings
from django.utils import timezone


class Book(models.Model):
  account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  author = models.CharField(max_length=50, blank=True, null=True)
  title = models.CharField(max_length=50)
  page_count = models.PositiveSmallIntegerField(blank=True, null=True)
  word_count = models.PositiveSmallIntegerField(blank=True, null=True)
  category = models.CharField(max_length=50, blank=True, null=True)

  def __str__(self):
      return self.title
  

class ReadingRecord(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_record')
  memo = models.TextField(blank=True, null=True)
  read_page_count = models.PositiveSmallIntegerField(blank=True, null=True)
  read_word_count = models.PositiveSmallIntegerField(blank=True, null=True)
  start_date = models.DateField(blank=True, null=True)
  finish_date = models.DateField(blank=True, null=True)
  finish_flag = models.BooleanField(default=False)



