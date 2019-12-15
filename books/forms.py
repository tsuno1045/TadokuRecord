from django import forms
import bootstrap_datepicker_plus as datetimepicker
from .models import Book, ReadingRecord


class BookForm(forms.ModelForm):

  class Meta:
    model = Book
    fields = ('title', 'author', 'page_count', 'word_count', 'category',)

class RecordForm(forms.ModelForm):

  class Meta:
    model = ReadingRecord
    fields = ('start_date', 'finish_date', 'read_page_count', 'read_word_count', 'finish_flag', 'memo',)
    widgets = {
      'start_date': datetimepicker.DatePickerInput(
        format='%Y-%m-%d',
        attrs={'readonly': 'true'},
        options={
          'locale': 'ja',
          'dayViewHeaderFormat': 'YYYY年 MMMM',
          'ignoreReadonly': True,
          'allowInputToggle': True,
        }
      ),
      'finish_date': datetimepicker.DatePickerInput(
        format='%Y-%m-%d',
        attrs={'readonly': 'true'},
        options={
          'locale': 'ja',
          'dayViewHeaderFormat': 'YYYY年 MMMM',
          'ignoreReadonly': True,
          'allowInputToggle': True,
        }
      )
    }


class BookWithRecordForm(forms.Form):
  title = forms.CharField(max_length=50, required=True)
  author = forms.CharField(max_length=50, required=False)
  page_count = forms.IntegerField(required=False)
  word_count = forms.IntegerField(required=False)
  category = forms.CharField(max_length=50, required=False)

  memo = forms.CharField(max_length=1000, required=False, widget=forms.Textarea)
  read_page_count = forms.IntegerField(required=False)
  read_word_count = forms.IntegerField(required=False)
  start_date = forms.DateField(
    required=False,
    widget=datetimepicker.DatePickerInput(
      format='%Y-%m-%d',
      attrs={'readonly': 'true'},
      options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
        'ignoreReadonly': True,
        'allowInputToggle': True,
      }
    )
  )
  finish_date = forms.DateField(
    required=False,
    widget=datetimepicker.DatePickerInput(
      format='%Y-%m-%d',
      attrs={'readonly': 'true'},
      options={
        'locale': 'ja',
        'dayViewHeaderFormat': 'YYYY年 MMMM',
        'ignoreReadonly': True,
        'allowInputToggle': True,
      }
    )
  )
  finish_flag = forms.BooleanField(required=False)
