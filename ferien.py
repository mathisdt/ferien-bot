import logging
from datetime import date, datetime, timedelta

import requests

from config import Config


def _calculate_percentage_of_completed_days(data, today, bar_width=25):
    summer_holidays = _get_summer_holidays(data)
    for i in range(0, len(summer_holidays) - 1):
        if not summer_holidays[i][1] < today < summer_holidays[i + 1][0]:
            continue
        days_completed_in_schoolyear = (today - summer_holidays[i][1]).days
        days_in_schoolyear = (summer_holidays[i + 1][0] - summer_holidays[i][1]).days
        if days_completed_in_schoolyear < days_in_schoolyear:
            percentage = days_completed_in_schoolyear / days_in_schoolyear
            return _create_loading_bar_with_percentage(percentage, bar_width)
    return _create_loading_bar_with_percentage(1, bar_width)


def _create_loading_bar_with_percentage(progress, width=25):
    progress = max(0, min(1, progress))

    # Definieren Sie die Zeichen für den Ladebalken
    bar_filled = '█'
    bar_empty = '░'

    # Berechnen Sie die Anzahl der gefüllten und leeren Blöcke basierend auf dem Fortschritt
    filled_blocks = int(width * progress)
    empty_blocks = width - filled_blocks

    # Erstellen Sie die Zeichenkette für den Ladebalken
    bar = bar_filled * filled_blocks + bar_empty * empty_blocks

    # Erstellen Sie die Darstellung des Ladebalkens
    loading_bar = f'{bar}\n'
    loading_bar += f"{round(progress * 100, 1)} % des Schuljahres sind geschafft."

    return loading_bar


def _get_summer_holidays(holiday_data):
    intervalls = []
    for holiday in holiday_data:
        if "sommerferien" in holiday['name'].lower():
            intervalls.append([holiday['start_date'], holiday['end_date']])
    return intervalls


def get_message(days_to_adjust: int = 0, bar_width: int = 0):
    config = Config("ferien")
    today = date.today() + timedelta(days=days_to_adjust)
    logging.debug(f"datum={today}")

    school_response = requests.get(f'https://ferien-api.de/api/v1/holidays/{config.land_kuerzel}')
    school_data = school_response.json()
    legal_response = requests.get(f'https://feiertage-api.de/api/?jahr={today.year}&nur_land={config.land_kuerzel}')
    legal_data = legal_response.json()
    legal_holidays = [datetime.strptime(legal_data[legal_holiday]['datum'], '%Y-%m-%d').date()
                      for legal_holiday in legal_data]

    # include adjacent legal holidays and weekends and pre-parse the dates for later:
    for item in school_data:
        holidays_start = item['start']
        holidays_start_date = datetime.strptime(holidays_start, '%Y-%m-%d').date()
        holidays_end = item['end']
        holidays_end_date = datetime.strptime(holidays_end, '%Y-%m-%d').date()
        while holidays_start_date.weekday() in (0, 6) or (holidays_start_date - timedelta(days=1)) in legal_holidays:
            holidays_start_date = holidays_start_date - timedelta(days=1)
        while holidays_end_date.weekday() in (4, 5) or holidays_end_date + timedelta(days=1) in legal_holidays:
            holidays_end_date = holidays_end_date + timedelta(days=1)
        item['start_date'] = holidays_start_date
        item['end_date'] = holidays_end_date

    # find next holidays
    for item in school_data:
        holidays_start_date = item['start_date']
        holidays_end_date = item['end_date']

        days_to_holidays_start = (holidays_start_date - today).days
        days_to_holidays_end = (holidays_end_date - today).days
        logging.debug(
            f"msg: {holidays_start_date} {holidays_end_date} {days_to_holidays_start} {days_to_holidays_end} {item['name']}")
        holidays_name = item['name'].split(" ")[0].capitalize()

        if not bar_width and config.bar_width:
            bar_width = int(config.bar_width)
        elif not bar_width:
            bar_width = 25

        if days_to_holidays_start <= 0 <= days_to_holidays_end:
            text = f"Yippie! Es sind {holidays_name} in Niedersachsen!\n\n"
            text += _calculate_percentage_of_completed_days(school_data, today, bar_width)
            return text
        elif days_to_holidays_start > 0 and days_to_holidays_end > 0:
            text = f'Noch {days_to_holidays_start} Tag{"e" if days_to_holidays_start != 1 else ""} bis zu den {holidays_name} in Niedersachsen.\n\n'
            text += _calculate_percentage_of_completed_days(school_data, today, bar_width)
            return text
