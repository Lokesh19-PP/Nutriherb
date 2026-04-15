import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project folder to the path so Django can find its settings
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriherb.settings')

application = get_wsgi_application()
app = application
