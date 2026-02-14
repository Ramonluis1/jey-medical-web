import openpyxl

EXCEL_FILE = 'Productos de Dynarex.xlsx'
TARGET_SKUS = ['36288', '36292', '36285']

print("Loading workbook...")
wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
sheet = wb.active
print("Workbook loaded.")

found = {}

for row in sheet.iter_rows(min_row=2, values_only=True):
    sku = str(row[0]).strip() if row[0] else None
    if sku in TARGET_SKUS:
        url = row[2]
        print(f"SKU: {sku} | URL: {url}")
