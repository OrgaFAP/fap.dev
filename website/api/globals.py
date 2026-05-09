import datetime
import re


def convert_month(month: str) -> str:
    "take month input and and return it"

    if month == "01":
        return "january"
    if month == "02":
        return "february"
    if month == "03":
        return "march"
    if month == "04":
        return "april"
    if month == "05":
        return "may"
    if month == "06":
        return "june"
    if month == "07":
        return "july"
    if month == "08":
        return "august"
    if month == "09":
        return "september"
    if month == "10":
        return "october"
    if month == "11":
        return "november"
    if month == "12":
        return "december"
    else:
        month = ""

    return month.strip()


def get_month() -> str:
    "Convert the month number -> to string"

    month: str = datetime.datetime.today().strftime("%m")
    if month == "01":
        return "january"
    if month == "02":
        return "february"
    if month == "03":
        return "march"
    if month == "04":
        return "april"
    if month == "05":
        return "may"
    if month == "06":
        return "june"
    if month == "07":
        return "july"
    if month == "08":
        return "august"
    if month == "09":
        return "september"
    if month == "10":
        return "october"
    if month == "11":
        return "november"
    if month == "12":
        return "december"
    else:
        month = ""

    return month.strip()


def get_week() -> dict:
    "Return a dict that represent 2 dates curdate:curdate-1week"

    time_: dict = {}
    today: str = get_today()
    pattern: str = r"(\d){4}-(\d){2}-(\d){2}"
    day_number = re.search(pattern, today).group()  # type: ignore
    day_number2 = re.search(r"(\d){2}$", day_number).group()  # type: ignore
    one_week_less: int = int(day_number2) - 7  # type : ignore
    dd: datetime.date = datetime.datetime.today().strftime("%Y-%m-")  # type: ignore
    final_date: str = f"{dd}{one_week_less}"
    new_today: datetime.date = datetime.datetime.today().strftime("%Y-%m-%d")  # type: ignore
    time_.update({new_today: final_date})

    print(time_[new_today])
    return time_


def get_month_number() -> str:
    "Get the month's number"

    month: str = datetime.datetime.today().strftime("%m")
    return month


def get_today_without_hours() -> str:
    "Return the date of the day"

    today: str = datetime.datetime.today().strftime("%Y-%m-%d")
    return today


def get_today() -> str:
    "Return the date of the day"

    today: str = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    return today


def get_yesterday() -> str:
    "Retur the date of yesterday"

    today_2 = re.search(r"([0-9]{1,4})-([0-9]{2})-([0-9]{2})", get_today()).group()  # type: ignore
    yesterday = re.search(r"[0-9]{2}$", today_2).group()  # type: ignore
    day_yesterday: int = int(yesterday) - 1
    day_today = day_yesterday + 1
    final_yesterday: str = get_today().replace(str(day_today), str(day_yesterday))
    final_yesterday: str = final_yesterday.split()[0]

    return final_yesterday


def get_year() -> str:
    "Get the actual YEAR"

    year: str = datetime.datetime.today().strftime("%Y")
    return year
