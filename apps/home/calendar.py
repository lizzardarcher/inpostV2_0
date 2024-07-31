from calendar import HTMLCalendar
from datetime import date, datetime, timedelta
from itertools import groupby

from django.views.generic import ListView

from .models import Post, PostSchedule
from django.utils.html import conditional_escape as esc
from apps.middleware import current_user


class PostCalendar(HTMLCalendar, ListView):
    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    def formatday(self, date_row):
        """
        Return a day as a table cell.
        """
        week_day = self.cssclasses[date_row.weekday()]
        num_day = int(date_row.day)
        num_month = int(date_row.month)
        num_year = int(date_row.year)
        s = []
        sch = PostSchedule.objects.filter(user=current_user.get_current_user())
        for i in sch:
            if i.schedule.year == num_year and i.schedule.month == num_month and i.schedule.day == num_day:
                s.append((i.post.name, i.schedule.strftime('%H:%M'), i.id, i.schedule.strftime('%Y-%m-%d %H:%M')))
        schedule_data = ''
        for data in sorted(s):
            if data[3] >= datetime.now().strftime('%Y-%m-%d %H:%M'):
                schedule_data += f'<a href="/schedule_update/{data[2]}"><p class="badge badge-warning text-dark">{data[0]} | {data[1]}</p></a><br/>'
            else:
                schedule_data += f'<a href="/schedule_update/{data[2]}"><p class="badge badge-info text-dark">{data[0]} | {data[1]}</p></a><br/>'
        if date_row.month != self.month:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return f'<td class="{week_day}"><a href="/calendar_event_create/{num_year}/{num_month}/{num_day}/"><div style="height:100%;width:100%"  >{num_day}</div></a><br/> ' \
                   f'{schedule_data}</td>'

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(date_row) for date_row in theweek)
        return f'<tr>{s}</tr>'

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="1" cellpadding="1" cellspacing="1" class="month table fixed col-12 col-md-8">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        dates = list(self.itermonthdates(theyear, themonth))
        self.month = themonth
        records = [dates[i:i + 7] for i in range(0, len(dates), 7)]
        for week in records:
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
