import calendar
from collections import deque
import datetime
import itertools


class BaseCalendarMixin:
  first_weekday = 0 #0=monday, ... , 6=sunday
  week_names = ['月', '火', '水', '木', '金', '土', '日'] 

  def setup_calendar(self):
    self._calendar = calendar.Calendar(self.first_weekday)

  def get_week_names(self):
    week_names = deque(self.week_names)
    week_names.rotate(-self.first_weekday)
    return week_names


class MonthCalendarMixin(BaseCalendarMixin):

  def get_previous_month(self, date):
    if date.month == 1:
      return date.replace(year=date.year-1, month=12, day=1)
    else:
      return date.replace(month=date.month-1, day=1)

  def get_next_month(self, date):
    if date.month == 12:
      return date.replace(year=date.year+1, month=1, day=1)
    else:
      return date.replace(month=date.month+1, day=1)

  def get_month_days(self, date):
    return self._calendar.monthdatescalendar(date.year, date.month)

  def get_current_month(self):
    month = self.kwargs.get('month')
    year = self.kwargs.get('year')
    if month and year:
      month = datetime.date(year=int(year), month=int(month), day=1)
    else:
      month = datetime.date.today().replace(day=1)
    return month

  def get_month_calendar(self):
    self.setup_calendar()
    current_month = self.get_current_month()
    calendar_data = {
      'now': datetime.date.today(),
      'month_days': self.get_month_days(current_month),
      'month_current': current_month,
      'month_previous': self.get_previous_month(current_month),
      'month_next': self.get_next_month(current_month),
      'week_names': self.get_week_names(),
    }
    return calendar_data


class MonthRecordsMixin(MonthCalendarMixin):

  def get_month_records(self, start, end, days):
    lookup = {
      '{}__range'.format(self.date_field): (start, end)
    }
    queryset = self.model.objects.filter(book__account=self.request.user).filter(**lookup)

    day_records = {day: [{"date_page_count":0},{"date_word_count":0}] for week in days for day in week}
    for record in queryset:
      record_date = getattr(record, self.date_field)
      day_records[record_date].append(record)
      if record.read_page_count:
        day_records[record_date][0]["date_page_count"] += int(record.read_page_count)
      if record.read_word_count:
        day_records[record_date][1]["date_word_count"] += int(record.read_word_count)
      
    size = len(day_records)
    return [{key: day_records[key] for key in itertools.islice(day_records, i, i+7)} for i in range(0, size, 7)]

  def get_month_calendar(self):
    calendar_context = super().get_month_calendar()
    month_days = calendar_context['month_days']
    month_first = month_days[0][0]
    month_last = month_days[-1][-1]
    calendar_context['month_day_records'] = self.get_month_records(
      month_first,
      month_last,
      month_days
    )
    return calendar_context
