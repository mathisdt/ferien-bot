#!/usr/bin/env python3
import locale
import logging
import sys

import ferien
from config import Config

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
                    stream=sys.stdout)

config = Config("console")

days_to_adjust = 0
if len(sys.argv) >= 2:
    days_to_adjust = int(sys.argv[1])

bar_width = int(config.bar_width) if config.bar_width else 0
NL = "\n"
print(f'{ferien.get_message(days_to_adjust=days_to_adjust, bar_width=bar_width)}{f"{NL}{NL}{config.footer}" if config.footer else ""}')
