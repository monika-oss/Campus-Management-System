import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(url, data=None, headers=None, method=None):
    if headers is None:
        headers = {}
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
        
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            return response.status, json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        res_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(res_body) if res_body else {"error": res_body}
        except json.JSONDecodeError:
            return e.code, {"error": "Not JSON", "content": res_body}

# 1. Login as Faculty
status, fac_res = make_request(f"{BASE_URL}/auth/login/", data={"email": "rekha@gmail.com", "password": "password123"})
if status == 200:
    faculty_token = fac_res.get("access_token")
    print("[+] Faculty login successful")
else:
    print("[-] Faculty login failed:", fac_res)
    exit()

# 2. Add Result (Faculty)
headers = {"Authorization": f"Bearer {faculty_token}"}
result_payload = {
    "student": 1,
    "subject": 1,
    "semester": 1,
    "academic_year": "2026-2027",
    "marks_obtained": 85,
    "max_marks": 100,
    "is_published": False
}
status, add_res = make_request(f"{BASE_URL}/results/", data=result_payload, headers=headers)
if status == 201:
    print("[+] Faculty added result successfully (Draft)")
elif status == 400:
    print("[-] Result might already exist or bad request:", add_res)
else:
    print("[-] Failed to add result:", add_res)

# 3. Login as Student (Before publish, should not see the result)
status, stu_res = make_request(f"{BASE_URL}/auth/login/", data={"email": "maha@gmail.com", "password": "password123"})
if status == 200:
    student_token = stu_res.get("access_token")
    student_id = stu_res.get("user", {}).get("student_id", 1)
    print("[+] Student login successful")
else:
    print("[-] Student login failed")
    exit()

student_headers = {"Authorization": f"Bearer {student_token}"}
status, get_res = make_request(f"{BASE_URL}/students/{student_id}/results/", headers=student_headers, method="GET")
if status == 200:
    print("[+] Student results (Before Publish):", len(get_res), "records")
else:
    print("[-] Failed to get student results:", get_res)

# 4. Login as Admin
status, admin_res = make_request(f"{BASE_URL}/auth/login/", data={"email": "admin@example.com", "password": "password123"})
if status == 200:
    admin_token = admin_res.get("access_token")
    print("[+] Admin login successful")
else:
    print("[-] Admin login failed")
    exit()

# 5. Publish Results
admin_headers = {"Authorization": f"Bearer {admin_token}"}
status, pub_res = make_request(f"{BASE_URL}/results/publish/", data={}, headers=admin_headers)
if status == 200:
    print("[+] Admin published results successfully")
else:
    print("[-] Admin failed to publish:", pub_res)

# 6. Student Check Again
status, get_after = make_request(f"{BASE_URL}/students/{student_id}/results/", headers=student_headers, method="GET")
if status == 200:
    print("[+] Student results (After Publish):", len(get_after), "records")
else:
    print("[-] Failed to get student results after:", get_after)
