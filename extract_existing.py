import re
import json
import os

html_file = 'Paginadecompañia11.html'
output_file = 'existing_products.json'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Regex to find the products array
# Look for const products = [ ... ];
# This is a bit tricky with full JS parsing but let's try a robust regex matching content between [ and ];
match = re.search(r'const products = \[\s*(\{.*?\})\s*\];', content, re.DOTALL)

# Since the regex might be hard due to nested braces, let's try finding the start and manual parsing
start_marker = 'const products = ['
end_marker = '];'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("Could not find products array")
    exit(1)

# Start searching for the matching closing bracket from start_idx
# efficient bracket counting
open_brackets = 0
found_start = False
end_idx = -1

for i in range(start_idx, len(content)):
    char = content[i]
    if char == '[':
        open_brackets += 1
        found_start = True
    elif char == ']':
        open_brackets -= 1
        if found_start and open_brackets == 0:
            end_idx = i + 1 # Include the ]
            break

if end_idx != -1:
    js_array_str = content[start_idx + len('const products = '):end_idx]
    
    # The content is JavaScript Object, not valid JSON (keys not quoted).
    # We need to convert it to valid JSON to parse it, OR just keep it as a string to write to the new JS file.
    # Keeping it as string is safer to preserve comments etc, but we want to append.
    
    # Actually, we can just save this string.
    with open('existing_products_raw.txt', 'w', encoding='utf-8') as f:
        f.write(js_array_str)
    print("Extracted raw JS array")
else:
    print("Could not find end of array")
