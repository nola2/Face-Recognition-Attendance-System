import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
from pathlib import Path
from datetime import datetime

def output(filename, sheet, num, name, present):
    folder_path = Path('firebase/attendance_files')
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / f"{filename}_{datetime.now().date()}.xls"

    if file_path.exists():
        rb = open_workbook(file_path)
        book = copy(rb)
        sh = book.get_sheet(0)
    else:
        book = xlwt.Workbook()
        sh = book.add_sheet(sheet)

        sh.write(0, 0, "Date")
        sh.write(0, 1, str(datetime.now().date()))
        sh.write(1, 0, "Name")
        sh.write(1, 1, "Status")

    row = num + 2
    sh.write(row, 0, name)
    sh.write(row, 1, present)

    book.save(file_path)
    return str(file_path)
