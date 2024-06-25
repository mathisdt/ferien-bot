#!/usr/bin/env python3
import datetime
import locale
import logging
import sys

import ferien
from config import Config

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
                    stream=sys.stdout)

config = Config("console")

bar_width = int(config.bar_width) if config.bar_width else 0
NL = "\n"


def print_message(description: str, days_to_adjust: int):
    print(f"\n{description}:\n============")
    print(
        f'{ferien.get_message(days_to_adjust=days_to_adjust, bar_width=bar_width)}{f"{NL}{NL}{config.footer}" if config.footer else ""}')
    print("============\n")


today = datetime.date.today()
print_message("vorletzter Tag vor Sommerferien", (datetime.date(year=2024, month=6, day=20) - today).days)
print_message("letzter Tag vor Sommerferien", (datetime.date(year=2024, month=6, day=21) - today).days)
print_message("erster Sommerferientag", (datetime.date(year=2024, month=6, day=22) - today).days)
print_message("zweiter Sommerferientag", (datetime.date(year=2024, month=6, day=23) - today).days)
print_message("vorletzter Sommerferientag", (datetime.date(year=2024, month=8, day=3) - today).days)
print_message("letzter Sommerferientag", (datetime.date(year=2024, month=8, day=4) - today).days)
print_message("erster Tag nach Sommerferien", (datetime.date(year=2024, month=8, day=5) - today).days)
print_message("zweiter Tag nach Sommerferien", (datetime.date(year=2024, month=8, day=6) - today).days)
print_message("letzter Tag vor Herbstferien", (datetime.date(year=2024, month=10, day=2) - today).days)
print_message("erster Tag der Herbstferien", (datetime.date(year=2024, month=10, day=3) - today).days)
print_message("letzter Tag der Herbstferien", (datetime.date(year=2024, month=10, day=20) - today).days)
print_message("erster Tag nach Herbstferien", (datetime.date(year=2024, month=10, day=21) - today).days)
print_message("letzter Tag vor Herbstferien (bew. Ferientag)",
              (datetime.date(year=2024, month=10, day=30) - today).days)
print_message("erster Tag Herbstferien (bew. Ferientag)", (datetime.date(year=2024, month=10, day=31) - today).days)
print_message("letzter Tag Herbstferien (bew. Ferientag)", (datetime.date(year=2024, month=11, day=3) - today).days)
print_message("erster Tag nach Herbstferien (bew. Ferientag)", (datetime.date(year=2024, month=11, day=4) - today).days)
