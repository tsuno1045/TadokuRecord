from django.urls import path
from . import views

urlpatterns = [
    path('', views.MonthRecords.as_view(), name='month_records'),
    path('calendar/<int:year>/<int:month>/', views.MonthRecords.as_view(), name='month_records'),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.day_records, name='day_records'),
    path('book/list/', views.book_list, name='book_list'),
    path('book/new/', views.book_new, name='book_new'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('book/<int:pk>/record/', views.record_new, name='record_new'),
    path('book/<int:pk>/record/<int:record_pk>/edit/', views.record_edit, name='record_edit'),
    path('book/<int:pk>/record/<int:record_pk>/delete/', views.record_delete, name='record_delete'),
    path('author/list/', views.author_list, name='author_list'),
    path('author/booklist/<author>/', views.author_book_list, name='author_book_list'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/booklist/<category>/', views.category_book_list, name='category_book_list'),
    path('bookwithrecord/new/', views.book_with_record_new, name='book_with_record_new'),
    
]
