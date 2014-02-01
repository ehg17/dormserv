from cal.models import Entry
from datetime import date, time, timedelta
import datetime


def handle():
    for e in Entry.objects.all():
        e.delete()

    print "Successfully deleted"

if __name__ == "__main__":
    handle()