# adaken/lib/get_date.py
from datetime import datetime, timezone, timedelta
import calendar
from typing import List, Dict

JST = timezone(timedelta(hours=9))

def get_month_ranges(start_year):
    ranges = []

    for month in range(1, 13):
        first_day = f"{start_year}-{month:02d}-01T00:00:00"

        last_day = calendar.monthrange(start_year, month)[1]
        last_day = f"{start_year}-{month:02d}-{last_day:02d}T23:59:59"

        ranges.append({
            "first_day": first_day,
            "last_day": last_day
        })

    return ranges