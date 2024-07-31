# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# sys.path.append('/var/www/html/inpost/vnv/lib/python3.8/site-packages')
# sys.path.append('/var/www/html/inpost')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
