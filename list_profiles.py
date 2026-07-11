import openpyxl
wb = openpyxl.load_workbook('dog_facts_7.3.2026.xlsx')
ws = wb['deep_dive_profiles']
print('All breed names in deep_dive_profiles:')
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0]:
        print(f'  {repr(row[0])}')
