# ============================================================
#  Smart Campus Management - Minimalist Professional PPT
#  Theme: Clean, Less Text, Perfect Alignment
# ============================================================

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Paths ────────────────────────────────────────────────────
SS_DIR      = os.path.join(os.path.dirname(__file__), "ppt_screenshots")
OUTPUT_PATH = r"C:\Users\preet\OneDrive\Desktop\Smart_Campus_Clean_Presentation.pptx"

# ── Color Palette ─────────────────────────────────────────────
BG_WHITE    = RGBColor(255, 255, 255)
BG_LIGHT    = RGBColor(248, 250, 252)
TEXT_DARK   = RGBColor(15, 23, 42)
TEXT_MUTED  = RGBColor(71, 85, 105)
ACCENT_BLUE = RGBColor(37, 99, 235)
ACCENT_GOLD = RGBColor(212, 175, 55)
DIVIDER     = RGBColor(226, 232, 240)
SHADOW_CLR  = RGBColor(203, 213, 225)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ── Helpers ───────────────────────────────────────────────────
def rect(slide, l, t, w, h, fill=None, line=None, lw=Pt(0), shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid() if fill else s.fill.background()
    if fill: s.fill.fore_color.rgb = fill
    s.line.fill.background()
    if line:
        s.line.color.rgb = line
        s.line.width = lw
    return s

def text(slide, txt, l, t, w, h, size=Pt(14), bold=False, color=TEXT_DARK, align=PP_ALIGN.LEFT, font="Segoe UI Light"):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = True
    p = tb.text_frame.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = txt
    r.font.size = size
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = font
    return tb

def ss(name):
    p = os.path.join(SS_DIR, name)
    return p if os.path.exists(p) else None

def add_header(s, title, slide_num):
    # Top Accent Lines
    rect(s, 0, 0, 13.33, 0.08, fill=ACCENT_BLUE)
    rect(s, 0, 0.08, 13.33, 0.04, fill=ACCENT_GOLD)
    
    # Title
    text(s, title, 0.6, 0.35, 12, 0.6, size=Pt(32), bold=True, color=TEXT_DARK, font="Segoe UI")
    
    # Bottom Footer
    rect(s, 0.6, 7.1, 12.13, 0.02, fill=DIVIDER)
    text(s, "Smart Campus Management & Student Analytics", 0.6, 7.15, 6, 0.3, size=Pt(10), color=TEXT_MUTED, font="Segoe UI")
    text(s, f"Prime Vector | Slide {slide_num}", 6, 7.15, 6.7, 0.3, size=Pt(10), color=TEXT_MUTED, align=PP_ALIGN.RIGHT, font="Segoe UI")

def clean_split_slide(num, step_title, bullet_points, img_file):
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, 13.33, 7.5, fill=BG_WHITE)
    add_header(s, step_title, num)
    
    # EXACT LEFT ALIGNMENT: x=0.6, width=4.8
    y = 1.6
    for pt in bullet_points:
        # Title of the bullet
        text(s, pt['title'], 0.6, y, 4.8, 0.4, size=Pt(18), bold=True, color=ACCENT_BLUE, font="Segoe UI")
        y += 0.4
        # Description (very short)
        text(s, pt['desc'], 0.6, y, 4.8, 0.6, size=Pt(15), color=TEXT_MUTED, font="Segoe UI")
        y += 0.8  # Fixed spacing between items

    # EXACT RIGHT ALIGNMENT: Image strictly placed in a specific box
    # Box coordinates: x=5.8, y=1.2, width=7.0, height=5.5
    img_x, img_y, img_w, img_h = 5.8, 1.3, 7.0, 5.3
    
    # Add a clean professional shadow/border block behind the image
    rect(s, img_x+0.05, img_y+0.05, img_w, img_h, fill=SHADOW_CLR)
    rect(s, img_x, img_y, img_w, img_h, fill=BG_WHITE, line=DIVIDER, lw=Pt(1.5))

    path = ss(img_file)
    if path:
        # We constrain the image to fit exactly inside the white block with a tiny margin
        margin = 0.05
        s.shapes.add_picture(path, Inches(img_x + margin), Inches(img_y + margin), 
                             Inches(img_w - 2*margin), Inches(img_h - 2*margin))
    else:
        text(s, f"Screenshot missing:\n{img_file}", img_x, img_y+2, img_w, 1.0, 
             size=Pt(16), color=TEXT_MUTED, align=PP_ALIGN.CENTER)

    return s


# ============================================================
#  1. TITLE SLIDE (Ultra Minimal)
# ============================================================
s1 = prs.slides.add_slide(BLANK)
rect(s1, 0, 0, 13.33, 7.5, fill=BG_WHITE)

rect(s1, 0, 0, 0.3, 7.5, fill=ACCENT_BLUE)
rect(s1, 0.3, 0, 0.08, 7.5, fill=ACCENT_GOLD)

text(s1, "PROJECT ALLOCATION", 1.0, 2.3, 10, 0.5, size=Pt(14), bold=True, color=ACCENT_GOLD, font="Segoe UI")
text(s1, "Smart Campus Management", 1.0, 2.6, 10, 0.8, size=Pt(48), bold=True, color=TEXT_DARK, font="Segoe UI")
text(s1, "& Student Analytics Platform", 1.0, 3.4, 10, 0.8, size=Pt(48), bold=True, color=TEXT_DARK, font="Segoe UI")

rect(s1, 1.05, 4.4, 1.5, 0.03, fill=ACCENT_BLUE)

text(s1, "Full Stack Web Development Major Project", 1.0, 4.6, 8, 0.5, size=Pt(18), color=TEXT_MUTED, font="Segoe UI")
text(s1, "Submitted to: Prime Vector", 1.0, 5.4, 8, 0.4, size=Pt(14), bold=True, color=TEXT_DARK, font="Segoe UI")
text(s1, "Developed by: Preethi", 1.0, 5.8, 8, 0.4, size=Pt(14), color=TEXT_MUTED, font="Segoe UI")

# ============================================================
#  2. PROJECT SCOPE (No Images)
# ============================================================
s2 = prs.slides.add_slide(BLANK)
rect(s2, 0, 0, 13.33, 7.5, fill=BG_WHITE)
add_header(s2, "Project Scope & Tech Stack", 2)

y = 1.6
text(s2, "Core Objective", 0.6, y, 12, 0.4, size=Pt(20), bold=True, color=ACCENT_BLUE, font="Segoe UI")
y += 0.4
text(s2, "To digitize and centralize campus administration, replacing paper-based workflows with a real-time, role-based digital platform.", 0.6, y, 12, 0.5, size=Pt(16), color=TEXT_MUTED, font="Segoe UI")

y += 1.0
text(s2, "Technology Stack", 0.6, y, 12, 0.4, size=Pt(20), bold=True, color=ACCENT_BLUE, font="Segoe UI")
y += 0.5

# Tech Stack boxes
techs = [
    ("Frontend UI", "HTML5, CSS3, JavaScript, Tailwind CSS"),
    ("Backend API", "Python, Django REST Framework, JWT Auth"),
    ("Database", "PostgreSQL (Production), SQLite (Dev)"),
    ("Deployment", "Vercel (Client) & Render.com (Server)")
]
for i, (title, desc) in enumerate(techs):
    x_pos = 0.6 + (i % 2) * 6.0
    y_pos = y + (i // 2) * 1.2
    rect(s2, x_pos, y_pos, 5.5, 0.9, fill=BG_LIGHT, line=DIVIDER, lw=Pt(1))
    rect(s2, x_pos, y_pos, 0.1, 0.9, fill=ACCENT_GOLD)
    text(s2, title, x_pos+0.3, y_pos+0.1, 5.0, 0.3, size=Pt(16), bold=True, color=TEXT_DARK, font="Segoe UI")
    text(s2, desc, x_pos+0.3, y_pos+0.45, 5.0, 0.3, size=Pt(13), color=TEXT_MUTED, font="Segoe UI")

# ============================================================
#  3. COMPLETE APPLICATION WORKFLOW
# ============================================================
s3 = prs.slides.add_slide(BLANK)
rect(s3, 0, 0, 13.33, 7.5, fill=BG_WHITE)
add_header(s3, "Complete Application Workflow", 3)

y_base = 1.6

# We'll create 3 distinct columns for Admin, Faculty, and Student flows
rect(s3, 0.6, y_base, 3.8, 5.0, fill=BG_LIGHT, line=DIVIDER, lw=Pt(1))
rect(s3, 0.6, y_base, 3.8, 0.08, fill=ACCENT_BLUE)
text(s3, "Admin Flow", 0.8, y_base + 0.2, 3.4, 0.4, size=Pt(20), bold=True, color=TEXT_DARK, font="Segoe UI")
admin_flow = [
    "Manage all user accounts",
    "Monitor global leave requests",
    "Upload semester exam marks",
    "Broadcast campus announcements"
]
ay = y_base + 0.9
for pt in admin_flow:
    text(s3, f"▪ {pt}", 0.8, ay, 3.4, 0.4, size=Pt(14), color=TEXT_MUTED, font="Segoe UI")
    ay += 0.55

rect(s3, 4.76, y_base, 3.8, 5.0, fill=BG_LIGHT, line=DIVIDER, lw=Pt(1))
rect(s3, 4.76, y_base, 3.8, 0.08, fill=ACCENT_GOLD)
text(s3, "Faculty Flow", 4.96, y_base + 0.2, 3.4, 0.4, size=Pt(20), bold=True, color=TEXT_DARK, font="Segoe UI")
faculty_flow = [
    "Select class and date",
    "Mark daily student attendance",
    "Review student leave applications",
    "Approve / Reject leave requests"
]
fy = y_base + 0.9
for pt in faculty_flow:
    text(s3, f"▪ {pt}", 4.96, fy, 3.4, 0.4, size=Pt(14), color=TEXT_MUTED, font="Segoe UI")
    fy += 0.55

rect(s3, 8.93, y_base, 3.8, 5.0, fill=BG_LIGHT, line=DIVIDER, lw=Pt(1))
rect(s3, 8.93, y_base, 3.8, 0.08, fill=ACCENT_BLUE)
text(s3, "Student Flow", 9.13, y_base + 0.2, 3.4, 0.4, size=Pt(20), bold=True, color=TEXT_DARK, font="Segoe UI")
student_flow = [
    "Login to personal dashboard",
    "View live attendance percentage",
    "Apply for medical/casual leave",
    "Check semester exam results"
]
sy = y_base + 0.9
for pt in student_flow:
    text(s3, f"▪ {pt}", 9.13, sy, 3.4, 0.4, size=Pt(14), color=TEXT_MUTED, font="Segoe UI")
    sy += 0.55

# ============================================================
#  SLIDES 4 - 13 (Clean Split Slides)
# ============================================================

clean_split_slide(4, "UI/UX & Frontend Design", [
    {"title": "Modern Aesthetics", "desc": "Implemented a clean, glassmorphism-inspired UI using Tailwind CSS."},
    {"title": "Responsive Layout", "desc": "Interfaces adapt seamlessly across desktop, tablet, and mobile devices."},
    {"title": "Client-Side Routing", "desc": "Smooth navigation transitions using JavaScript DOM manipulation."},
], "01_login.png")

clean_split_slide(5, "Admin Control Center", [
    {"title": "Global Overview", "desc": "Administrators gain instant statistical insights into campus operations."},
    {"title": "Live Data Aggregation", "desc": "KPI cards display Total Students, Faculty, and Global Pending Leaves in real-time."},
    {"title": "Centralized Management", "desc": "Full access to User Management, Results generation, and Announcements."},
], "02_admin_dashboard.png")

clean_split_slide(6, "Student Record Management", [
    {"title": "Complete Lifecycle", "desc": "Full CRUD capabilities (Create, Read, Update, Delete) for student data."},
    {"title": "Secure Provisioning", "desc": "System automatically generates secure login credentials upon student creation."},
    {"title": "Advanced Filtering", "desc": "Instant search mechanisms by Roll Number and Department."},
], "03_admin_students.png")

clean_split_slide(7, "Faculty: Attendance Tracking", [
    {"title": "Daily Marking", "desc": "Faculty can rapidly mark attendance using dynamic student rosters."},
    {"title": "Status Toggles", "desc": "One-click options for Present, Absent, Leave, or On-Duty (OD)."},
    {"title": "Data Integrity", "desc": "Backend validation strictly prevents duplicate or future-dated entries."},
], "09_faculty_attendance.png")

clean_split_slide(8, "Digital Leave Workflow", [
    {"title": "1. Submission", "desc": "Students submit leave requests specifying duration and reason digitally."},
    {"title": "2. Faculty Review", "desc": "Requests instantly route to the Faculty dashboard for Approval/Rejection."},
    {"title": "3. Status Updates", "desc": "Students receive real-time UI updates indicating their application status."},
], "10_faculty_leave.png")

clean_split_slide(9, "Examination & Result Processing", [
    {"title": "Secure Grading", "desc": "Administrators upload subject marks securely via the result portal."},
    {"title": "Automated Calculation", "desc": "System algorithm computes Grade Letters and precise GPA/CGPA."},
    {"title": "Targeted Publishing", "desc": "Finalized grades are dispatched exclusively to the authenticated student's portal."},
], "06_admin_results.png")

clean_split_slide(10, "Student Performance Analytics", [
    {"title": "Personalized Dashboard", "desc": "Students log in to a personalized, data-driven analytical view."},
    {"title": "Real-Time Percentage", "desc": "Live calculation of cumulative attendance percentage."},
    {"title": "Threshold Warnings", "desc": "Dynamic visual indicators highlight if attendance falls below 75%."},
], "11_student_dashboard.png")

clean_split_slide(11, "Notification System", [
    {"title": "Digital Announcements", "desc": "Instantly replaces traditional, physical campus notice boards."},
    {"title": "Campus-Wide Broadcasts", "desc": "Administrators publish notices that appear on all relevant dashboards."},
    {"title": "Critical Updates", "desc": "Ensures exam schedules and holidays are communicated immediately."},
], "07_admin_announce.png")

# ============================================================
#  12. CONCLUSION
# ============================================================
s12 = prs.slides.add_slide(BLANK)
rect(s12, 0, 0, 13.33, 7.5, fill=BG_WHITE)
rect(s12, 0, 0, 13.33, 0.08, fill=ACCENT_BLUE)
rect(s12, 0, 0.08, 13.33, 0.04, fill=ACCENT_GOLD)

text(s12, "Project Completion Summary", 1.0, 1.5, 11, 0.8, size=Pt(40), bold=True, color=TEXT_DARK, font="Segoe UI")
rect(s12, 1.0, 2.5, 3.0, 0.02, fill=DIVIDER)

y = 3.0
for item in [
    "Delivered all requirements specified in the Prime Vector mandate.",
    "Engineered a secure, scalable RESTful API with PostgreSQL.",
    "Developed a highly responsive, modern user interface.",
    "Successfully deployed live via Vercel (Frontend) and Render (Backend)."
]:
    rect(s12, 1.0, y+0.1, 0.2, 0.2, fill=ACCENT_BLUE)
    text(s12, item, 1.4, y, 10, 0.4, size=Pt(18), color=TEXT_MUTED, font="Segoe UI")
    y += 0.7

text(s12, "Thank You", 1.0, 6.0, 11, 0.6, size=Pt(28), bold=True, color=ACCENT_GOLD, font="Segoe UI")
text(s12, "12", 12.7, 7.1, 0.5, 0.35, size=Pt(12), color=TEXT_MUTED, align=PP_ALIGN.RIGHT)

# ============================================================
#  SAVE
# ============================================================
prs.save(OUTPUT_PATH)
print(f"Minimalist PPT saved to: {OUTPUT_PATH}")
