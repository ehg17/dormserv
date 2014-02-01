from cal.models import Entry
from datetime import date, time, timedelta
import datetime


def handle(year, month, day, def_orders):
    start_date = datetime.date(year, month, day)
    list_of_dates = []
    for i in range(0,7):
        k = start_date + datetime.timedelta(days=i)
        list_of_dates.append(k)
    list_of_times = []
    deliv_times = [(7,45),(8,00),(8,15),(8,30),(8,45),(9,00),(9,15),(9,30),(9,45),(10,00),(10,15),(10,30)]
    for time in deliv_times:
        k = datetime.time(time[0], time[1])
        list_of_times.append(k)
    for d in list_of_dates:
        for t in list_of_times:
            e = Entry(start_time=t, date=d, deliveries_avail=def_orders)
            e.save()
    date_str = str(year) + "-" + str(month) + "-" + str(date)
    print "Successfully populated"

if __name__ == "__main__":
    handle(2014, 01, 27, 4)