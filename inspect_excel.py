import openpyxl

wb = openpyxl.load_workbook('Productos de Dynarex.xlsx')
sheet = wb.active

print("--- ROWS 1-5 ---")
for i, row in enumerate(sheet.iter_rows(max_row=5, values_only=True)):
    print(f"Row {i+1}: {row}")
