"""
WSGI config for hanmei project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys


from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hanmei.settings')
os.environ["DJANGO_SETTINGS_MODULE"] = "hanmei.settings"
sys.path.append('/home/website/HMEID')
sys.path.append('/home/website/HMEID/hanmei')

application = get_wsgi_application()
