import requests

try:
    res = requests.get("https://campus-management-system-zrh8.onrender.com/api/faculty/debug_ods/", timeout=10)
    print(res.status_code)
    print(res.text)
except Exception as e:
    print("Error:", e)
