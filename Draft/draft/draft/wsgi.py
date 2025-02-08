import os
import sys

# Define the project path
path = "/home/likhith151105/django_projects/Doctor-Patient-Consultation-Site/Draft/draft"

# Ensure the project path is in the system path
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "draft.draft.settings")

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
