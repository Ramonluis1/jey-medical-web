with open('missing_images.txt', 'r') as f:
    lines = f.readlines()
    for line in lines[:5]:
        print(line.strip())
