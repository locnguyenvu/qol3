from datetime import datetime
from qol3.holiday import Holiday, save


def set(name: str, start_at: str, end_at: str):
    date_format = "%Y-%m-%d"
    try:
        start_date = datetime.strptime(start_at, date_format)
        end_date = datetime.strptime(end_at, date_format)
        holiday = Holiday(name, start_date.strftime(date_format), end_date.strftime(date_format))
        save(holiday)
    except ValueError as e:
        print("Error:", e)
    pass


def list():
    today = datetime.now().strftime("%Y-%m-%d")
    holidays = Holiday.query.filter(Holiday.start_at >= today).all()

    for ho in holidays:
        print(ho.name, ho.start_at, ho.end_at)
