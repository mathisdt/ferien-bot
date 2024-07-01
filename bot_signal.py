#!/usr/bin/env python3
import locale
import logging
import re
import sys

from pydbus import SystemBus

import ferien
from config import Config

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
                    stream=sys.stdout)

config = Config("signal")

bus = SystemBus()
sender = re.sub(r'[^0-9]', '', config.sender)
signal = bus.get('org.asamk.Signal', object_path=f'/org/asamk/Signal/_{sender}')

bar_width = int(config.bar_width) if config.bar_width else 0
NL = "\n"
msg = f'{ferien.get_message(bar_width=bar_width)}{f"{NL}{NL}{config.footer}" if config.footer else ""}'

if config.recipients:
    recipients = config.recipient.split("|")
    try:
        signal.sendMessage(msg, [], recipients)
    except:
        # sometimes DBus doesn't find/use the right signature,
        # so we try again with single recipients instead of an array
        for recipient in recipients:
            signal.sendMessage(msg, [], recipient.trim())

if config.groups:
    my_groups = signal.listGroups()
    target_groups = config.groups.split("|")
    for my_group in my_groups:
        if my_group[2] in target_groups:
            signal.sendGroupMessage(msg, [], my_group[1])
