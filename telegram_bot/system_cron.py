import os
import time


def crutching():
    os.system('chmod 777 -R /var/www/html/inpost/core/static/media/')

while True:
    try:
        crutching()
        time.sleep(60)
    except:
        time.sleep(60)