from django.contrib import admin
from .models import Book, ReadingRecord


class ReadingRecordInline(admin.TabularInline):
  model = ReadingRecord
  extra = 3


class BookAdmin(admin.ModelAdmin):
  inlines = [ReadingRecordInline]


admin.site.register(Book, BookAdmin)
admin.site.register(ReadingRecord)
