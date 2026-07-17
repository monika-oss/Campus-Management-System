import urllib.request
try:
    with urllib.request.urlopen("https://campus-management-system-zrh8.onrender.com/api/students/departments/") as response:
        print(response.getcode())
except Exception as e:
    print(e)
