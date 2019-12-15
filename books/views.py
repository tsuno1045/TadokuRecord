import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Sum

from .models import Book, ReadingRecord
from .forms import BookForm, RecordForm, BookWithRecordForm
from .mixins import MonthRecordsMixin

@login_required
def book_list(request):
  books = Book.objects.filter(account=request.user)
  return render(request, 'books/book_list.html', {'books': books})

@login_required
def book_detail(request, pk):
  book = get_object_or_404(Book, account=request.user, pk=pk)
  return render(request, 'books/book_detail.html', {'book': book})

@login_required
def author_list(request):
  authors = Book.objects.filter(account=request.user).values('author').order_by('author').distinct()
  return render(request, 'books/author_list.html', {'authors':authors})

@login_required
def author_book_list(request, author):
  author = None if author == 'None' else author
  books = Book.objects.filter(author=author).filter(account=request.user)
  return render(request, 'books/author_book_list.html', {'author':author, 'books': books})

@login_required
def category_book_list(request, category):
  category = None if category == 'None' else category
  books = Book.objects.filter(category=category).filter(account=request.user)
  return render(request, 'books/category_book_list.html', {'category':category, 'books': books})

@login_required
def category_list(request):
  categories = Book.objects.filter(account=request.user).values('category').order_by('category').distinct()
  for category in categories:
    total_page = ReadingRecord.objects.filter(book__account=request.user).filter(book__category=category['category']).filter(finish_flag=True).aggregate(Sum('read_page_count'))
    category['total_page'] = total_page['read_page_count__sum']
    total_word = ReadingRecord.objects.filter(book__account=request.user).filter(book__category=category['category']).filter(finish_flag=True).aggregate(Sum('read_word_count'))
    category['total_word'] = total_word['read_word_count__sum']
  return render(request, 'books/category_list.html', {'categories':categories})

@login_required
def book_new(request):
  if request.method == "POST":
    form = BookForm(request.POST)
    if form.is_valid():
      book = form.save(commit=False)
      book.account = request.user
      book.save()
      return redirect('book_detail', pk=book.pk)
  else:
    form = BookForm()
    return render(request, 'books/book_edit.html', {'form': form})

@login_required
def book_edit(request, pk):
  book = get_object_or_404(Book, account=request.user, pk=pk)
  if request.method == "POST":
    form = BookForm(request.POST, instance=book)
    if form.is_valid():
      book = form.save(commit=False)
      book.account = request.user
      book.save()
      return redirect('book_detail', pk=book.pk)
  else:
    form = BookForm(instance=book)
    return render(request, 'books/book_edit.html', {'form': form})

@login_required
def book_delete(request, pk):
  book = get_object_or_404(Book, account=request.user, pk=pk)
  book.delete()
  return redirect('book_list')

@login_required
def record_new(request, pk):
  book = get_object_or_404(Book, account=request.user, pk=pk)
  if request.method == "POST":
    form = RecordForm(request.POST)
    if form.is_valid():
      record = form.save(commit=False)
      record.book = book
      if record.finish_date != None:
        record.finish_flag = True
      record.save()
      return redirect('book_detail', pk=pk)
  else:
    form = RecordForm(initial={'read_page_count': book.page_count, 'read_word_count': book.word_count})
    return render(request, 'books/record_edit.html', {'form': form})

@login_required
def record_edit(request, pk, record_pk):
  book = get_object_or_404(Book, account=request.user, pk=pk)
  record = get_object_or_404(ReadingRecord, book__account=request.user, pk=record_pk)
  if request.method == "POST":
    form = RecordForm(request.POST, instance=record)
    if form.is_valid():
      record = form.save(commit=False)
      record.book = book
      if record.finish_date != None:
        record.finish_flag = True
      record.save()
      return redirect('book_detail', pk=pk)
  else:
    form = RecordForm(instance=record)
    return render(request, 'books/record_edit.html', {'form': form})

@login_required
def record_delete(request, pk, record_pk):
  record = get_object_or_404(ReadingRecord, book__account=request.user, pk=record_pk)
  record.delete()
  return redirect('book_detail', pk=pk)

@login_required
def book_with_record_new(request):
  form = BookWithRecordForm(request.POST or None)
  if form.is_valid():
    book = Book()
    record = ReadingRecord()

    book.title = form.cleaned_data['title']
    book.author = None if form.cleaned_data['author'] == '' else form.cleaned_data['author']
    book.page_count = form.cleaned_data['page_count']
    book.word_count = form.cleaned_data['word_count']
    book.category = None if form.cleaned_data['category'] == '' else form.cleaned_data['category']

    newbook = Book.objects.create(
      account = request.user,
      title = book.title,
      author = book.author,
      page_count = book.page_count,
      word_count = book.word_count,
      category = book.category,
    )

    record.memo = form.cleaned_data['memo']
    record.read_page_count = form.cleaned_data['read_page_count']
    record.read_word_count = form.cleaned_data['read_word_count']
    record.start_date = form.cleaned_data['start_date']
    record.finish_date = form.cleaned_data['finish_date']
    record.finish_flag = form.cleaned_data['finish_flag']
    if record.finish_date != None:
      record.finish_flag = True

    ReadingRecord.objects.create(
      book = newbook,
      memo = record.memo,
      read_page_count = record.read_page_count,
      read_word_count = record.read_word_count,
      start_date = record.start_date,
      finish_date = record.finish_date,
      finish_flag = record.finish_flag,
    )

    return redirect('book_detail', pk=newbook.pk)
  return render(request, 'books/book_with_record.html', {'form': form})


@login_required
def day_records(request, year, month, day):
  date = datetime.date(year=year, month=month, day=day)
  records = ReadingRecord.objects.filter(book__account=request.user).filter(finish_date=date).order_by('-finish_date')
  return render(request, 'books/day_records.html', {'date':date, 'records': records})


class MonthRecords(LoginRequiredMixin, MonthRecordsMixin, generic.TemplateView):
  template_name = 'books/month_records.html'
  model = ReadingRecord
  date_field = 'finish_date'
  first_weekday = 6
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    calendar_context = self.get_month_calendar()
    context.update(calendar_context)
    context['month_page_count'] = self.month_page_count(context['month_current'])
    context['month_word_count'] = self.month_word_count(context['month_current'])
    context['total_page_count'] = self.total_page_count()
    context['total_word_count'] = self.total_word_count()
    return context

  def month_page_count(self, current_month):
    total_page = ReadingRecord.objects.filter(book__account=self.request.user).filter(finish_date__year=current_month.year, finish_date__month=current_month.month).aggregate(Sum('read_page_count'))
    return total_page['read_page_count__sum']

  def month_word_count(self, current_month):
    total_word = ReadingRecord.objects.filter(book__account=self.request.user).filter(finish_date__year=current_month.year, finish_date__month=current_month.month).aggregate(Sum('read_word_count'))
    return total_word['read_word_count__sum']

  def total_page_count(self):
    total_page = ReadingRecord.objects.filter(book__account=self.request.user).filter(finish_flag=True).aggregate(Sum('read_page_count'))
    return total_page['read_page_count__sum']

  def total_word_count(self):
    total_word = ReadingRecord.objects.filter(book__account=self.request.user).filter(finish_flag=True).aggregate(Sum('read_word_count'))
    return total_word['read_word_count__sum']
