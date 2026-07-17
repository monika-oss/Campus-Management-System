import urllib.request
try:
    req = urllib.request.Request("https://campus-management-system-zrh8.onrender.com/faculty/attendance.html", method="HEAD")
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print(response.headers)
except Exception as e:
    print(e)
