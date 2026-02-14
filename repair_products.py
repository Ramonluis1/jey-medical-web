import re

FILE_PATH = 'products.js'

print(f"Repairing {FILE_PATH}...")

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

repaired_count = 0
# Regex to find the corrupted lines and capture the good URL
# Pattern seen: "img": "FOTOS/logo.pngimg: 'https://...'"
# capture the indentation and the https url
url_pattern = re.compile(r"(https?://[^'\"\s]+)")

cleaned_lines = []

for line in lines:
    if "FOTOS/logo.png" in line and "http" in line:
        # This is a corrupted line
        match = url_pattern.search(line)
        if match:
            url = match.group(1)
            # determine indentation
            indent = line[:len(line) - len(line.lstrip())]
            
            # check for comma at end of original line (it might be messy)
            # safer to just add a comma if it's not the last item?
            # In array of objects, usually comma is good.
            # But the last property in an object doesn't strictly need it, but allows it.
            # The line usually ends with a comma if it's not the last prop.
            # However, looking at the grep output, some ended with `'"` (closing matching quote of the mess).
            
            # Let's simple format:
            # "img": "URL",
            # We'll assume comma is safer to include than exclude in a list?
            # Or check if next line is `}`?
            # We can't easily check next line here without index.
            # But standard JS style in this file seems to use commas.
            
            new_line = f'{indent}"img": "{url}",\n'
            cleaned_lines.append(new_line)
            repaired_count += 1
        else:
            # Couldn't extract URL? Keep it but warn? 
            # Or maybe it's just a heavily broken line.
            print(f"Skipping unfixable line: {line.strip()}")
            cleaned_lines.append(line)
    else:
        cleaned_lines.append(line)

print(f"Repaired {repaired_count} lines.")

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.writelines(cleaned_lines)
