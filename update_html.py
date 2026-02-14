import os

html_file = 'index.html'
backup_file = 'index.html.bak'

# Create backup
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as bk:
        bk.write(content)

lines = content.split('\n')
new_lines = []
skip = False
script_tag_seen = False

# We want to insert <script src="products.js"></script> before the <script> tag that contains 'const products'
# But 'const products' is inside a <script>.
# We can just look for 'const products = [' and replace the preceding <script> or just insert it before.

processed_products = False

for i, line in enumerate(lines):
    if 'const products = [' in line:
        skip = True
        processed_products = True
        continue
    
    if skip:
        if '];' in line:
            skip = False
        continue
        
    # Check for the script tag that likely starts the logic block (line 1327 approximately)
    # The view_file showed:
    # 1326:     <!-- Logic -->
    # 1327:     <script>
    if '<script>' in line and not processed_products:
        # Check if this is the relevant script tag?
        # There might be other script tags.
        # But this one is near 'const products'.
        # Since we are iterating and haven't hit 'const products' yet, and we know 'const products' is inside a script tag...
        # Wait, if we are line by line, 'const products' is AFTER <script>.
        # So when we hit <script>, we don't know yet if 'const products' follows.
        
        # Heuristic: The file has comment <!-- Logic --> before it.
        # Or we can just insert it at the very end of head or just before this specific script tag.
        pass

    new_lines.append(line)

# Now, we removed 'const products = [ ... ];'.
# We need to inject the script tag.
# Let's do it by replacing <!-- Logic --> with <!-- Logic -->\n<script src="products.js"></script>
# This checks for the comment line 1326.

final_lines = []
for line in new_lines:
    if '<!-- Logic -->' in line:
        final_lines.append(line)
        final_lines.append('    <script src="products.js"></script>')
    else:
        final_lines.append(line)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print("Successfully updated HTML.")
