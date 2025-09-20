from pathlib import Path
from openpyxl import Workbook
import re

psp_dir = Path("../PSPs")

files = list(psp_dir.glob("PSP-*.md"))

def psp_number(file_path):
    match = re.search(r"PSP-(\d+)\.md", file_path.name)
    return int(match.group(1)) if match else 0

files.sort(key=psp_number)

wb = Workbook()
ws = wb.active
ws.title = "PSPs"

ws.append(["PSP #", "Title"])

dash_pattern = re.compile(r"\s*[—–\-―]\s*")

for file in files:
    with file.open("r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        if first_line.startswith("# PSP"):
            parts = dash_pattern.split(first_line, maxsplit=1)
            if len(parts) == 2:
                number_part = parts[0].strip()
                title = parts[1].strip()
                number = number_part.split()[1]
                ws.append([number, title])

wb.save("PSPs.xlsx")
print("Excel is generated!")
