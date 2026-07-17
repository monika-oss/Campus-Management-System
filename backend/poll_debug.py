import urllib.request
import json
import time

while True:
    try:
        req = urllib.request.Request("https://campus-management-system-zrh8.onrender.com/api/faculty/debug_leaves/")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("Leaves:", data)
            break
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Not deployed yet, waiting 5 seconds...")
            time.sleep(5)
        else:
            print("HTTPError:", e.code)
            break
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
