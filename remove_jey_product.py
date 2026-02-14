import re

FILE_PATH = 'products.js'

print(f"Removing Jey Medical from {FILE_PATH}...")

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to remove the product object where brand is 'Jey Medical'
# Regex for the object: { ... brand: 'Jey Medical' ... }
# Since my previous script appended it at the end, it should be easy to find.
# But let's be robust and filter lines.

# Option 2: Read file, parse text blocks? 
# The file is large.
# Let's simple regex replace the specific block I added?
# It looked like:
#    {
#        id: 4762,
#        category: 'medical-supply',
#        brand: 'Jey Medical',
# ...
#    }

# Let's try filtering the list of objects.
# Actually, since I appended it, I can just read the whole file and define a regex that matches the object.

pattern = re.compile(r',\s*\{\s*id:\s*\d+,\s*category:\s*[\'"]medical-supply[\'"],\s*brand:\s*[\'"]Jey Medical[\'"].*?\}\s*(?=\]|$)', re.DOTALL)

# Try to find and remove it.
new_content, count = pattern.subn('', content)

if count > 0:
    print(f"Removed {count} Jey Medical entries.")
    
    # Fix potential trailing comma issue if I removed the last item
    # If the new content ends with ", ]", replace with " ]"
    # Actually, Javascript allows trailing commas in arrays.
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print("No Jey Medical entries found matching the pattern. Trying looser check.")
    
    # Fallback: Line based filtering?
    lines = content.split('\n')
    new_lines = []
    skip = False
    removed = 0
    
    for line in lines:
        if "brand: 'Jey Medical'" in line:
            # This line belongs to the object we want to delete.
            # But we are in a loop line by line.
            # We need to know start/end of object.
            # This is risky without context.
            pass
            
    # Let's try a simpler regex that just finds the 'Jey Medical' brand line and the surrounding braces?
    # No, that's dangerous.
    
    # Alternative: The block I wrote was very specific.
    #    {
    #        id: \d+,
    #        category: 'medical-supply',
    #        brand: 'Jey Medical',
    #        title: 'Medical Supply Catalog',
    #        price: 0.00,
    #        desc: 'Comprehensive range of medical supplies distributed by Jey Medical.',
    #        specs: \['Distributor', 'Medical Equipment', 'Supplies'\],
    #        img: 'FOTOS/LOGO JEY MEDICAL.png'
    #    }
    
    # Let's exact match the unique parts
    if "brand: 'Jey Medical'" in content:
        print("Found text 'Jey Medical', doing manual block removal.")
        # Find index
        idx = content.find("brand: 'Jey Medical'")
        # Find start of object (look back for {)
        start_obj = content.rfind('{', 0, idx)
        # Find end of object (look forward for })
        end_obj = content.find('}', idx) + 1
        
        # Check if there is a comma before or after
        # If it was appended, likely comma before.
        
        # Remove from start_obj to end_obj
        # Also clean up comma if needed.
        
        # Be careful not to break array structure.
        snippet = content[start_obj:end_obj]
        print(f"Removing snippet: {snippet}")
        
        # Check preceding comma
        pre_idx = start_obj - 1
        while pre_content := content[pre_idx].isspace():
            pre_idx -= 1
        
        # If char at pre_idx is ',', remove it too?
        # Only if we aren't breaking the list.
        # Safest: remove the object, see if syntax holds (JS allow trailing comma).
        
        # Actually, let's just remove the block and let the syntax check verify.
        # But if it was the last item, checks might fail if we leave a comma before `]`.
        # (Though most engine allow `[a, b, ]`)
        
        new_content = content[:start_obj] + content[end_obj:]
        
        # Clean up empty lines or stranded commas?
        # A simple `node -c` check after will confirm.
        
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Removed manually found block.")
    else:
        print("Could not find Jey Medical in file.")

