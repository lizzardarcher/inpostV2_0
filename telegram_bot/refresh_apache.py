import os
from time import sleep


while True:
    os.system('apachectl -k graceful')
    sleep(300)
    exit()