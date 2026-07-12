import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_campus.settings")
sys.path.append(r"c:\Users\preet\OneDrive\Desktop\Campus_Management\backend")
django.setup()

from django.test import Client
c = Client()
try:
    # Need to simulate authentication or permission if required
    # But let's just see what error it throws first
    res = c.get('/api/faculty/1/today_classes/')
    print("Status:", res.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
