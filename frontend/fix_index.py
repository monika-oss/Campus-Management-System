import os

path = r"c:\Users\preet\OneDrive\Desktop\Campus_Management\frontend\index.html"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

content = content.replace("setIntervaldocument.addEventListener('DOMContentLoaded', () => {", "setInterval(() => {")
content = content.replace("setTimeoutdocument.addEventListener('DOMContentLoaded', () => {", "setTimeout(() => {")
content = content.replace("tl.calldocument.addEventListener('DOMContentLoaded', () => {", "tl.call(() => {")

if content != original:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed index.html!")
else:
    print("No changes made.")
