import os
import sys

# GitHub repo ka name 'my' hai
path = '/home/Edutrack/my'

if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newpro.settings')

# Rest of the file...

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newpro.settings')

application = get_wsgi_application()
