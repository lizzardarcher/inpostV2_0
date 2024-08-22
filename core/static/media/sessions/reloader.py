import datetime
import json
import logging
import os
import asyncio
import string
import random
import sys
import traceback
from pathlib import Path
from time import sleep

import pyrogram
from pyrogram import Client

from django.core.files import File
import django
from pyrogram.enums import ParseMode

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.spamer.models import GeneralSettings

while True:
    if GeneralSettings.objects.filter(id=1)[0].is_reload_spam_needed:
        os.system('systemctl restart spamer.service')
        # os.system('systemctl restart autoanswering.service')
        GeneralSettings.objects.filter(id=1).update(is_reload_spam_needed=False)
    sleep(10)