import requests

# login as admin or faculty
url_login = "https://campus-management-system-zrh8.onrender.com/api/auth/login/"
res_login = requests.post(url_login, json={"email": "admin@smartcampus.com", "password": "adminpassword123"})
if res_login.status_code == 200:
    token = res_login.json().get('access') or res_login.json().get('token')
    headers = {"Authorization": f"Bearer {token}"}
    
    url_students = "https://campus-management-system-zrh8.onrender.com/api/faculty/1/students/?date=2026-07-17&period=1&department=2"
    res_students = requests.get(url_students, headers=headers)
    print("Students Status:", res_students.status_code)
    students = res_students.json()
    for s in students:
        if s.get('roll_number') == 'REG2026EEE003':
            print("Maha:", s)
        if s.get('roll_number') == 'REG2026EEE001':
            print("Yogesh:", s)
else:
    print("Login failed:", res_login.status_code, res_login.text)
