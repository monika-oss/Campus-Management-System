import glob, re

css_code = '''
/* ---------------- Ant Design Table ---------------- */
.ant-table-wrapper {
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #f0f0f0;
    overflow: hidden;
}
.ant-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    text-align: left;
}
.ant-table thead > tr > th {
    background: #fafafa !important;
    color: rgba(0, 0, 0, 0.85) !important;
    font-weight: 600 !important;
    padding: 16px !important;
    border-bottom: 1px solid #f0f0f0 !important;
    font-size: 14px !important;
    text-transform: none !important;
    letter-spacing: normal !important;
}
.ant-table tbody > tr > td {
    padding: 16px !important;
    border-bottom: 1px solid #f0f0f0 !important;
    color: rgba(0, 0, 0, 0.88) !important;
    font-size: 14px !important;
    transition: background 0.3s;
}
.ant-table tbody > tr {
    transition: background 0.3s;
}
.ant-table tbody > tr:hover > td {
    background: #fafafa !important;
}
.ant-table tbody > tr:last-child > td {
    border-bottom: none !important;
}
'''

# append to premium-theme.css
css_path = 'c:/Users/preet/OneDrive/Desktop/Campus_Management/frontend/css/premium-theme.css'
with open(css_path, 'r', encoding='utf-8') as f:
    existing = f.read()
if 'ant-table-wrapper' not in existing:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(css_code)

for f in glob.glob('c:/Users/preet/OneDrive/Desktop/Campus_Management/frontend/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original = content
    
    # We will replace all <table class="..."> with <table class="ant-table">
    content = re.sub(r'<table\s+class="[^"]+"', '<table class="ant-table"', content)
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Applied ant-table in {f}')
