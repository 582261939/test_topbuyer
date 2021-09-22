import openpyxl


class OpenExcel:

    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.ex = openpyxl.load_workbook(file_path)
        self.sheet = self.ex[sheet_name]

    def red_data(self):
        srl = list(self.sheet.rows)
        title = [i.value for i in srl[0]]
        data_list = []
        for item in srl[1:]:
            data = [i.value for i in item]
            dict_data = dict(zip(title, data))
            data_list.append(dict_data)
        return data_list

    def writ_data(self, row, column, value):
        self.sheet.cell(row=row, column=column, value=value)
        self.ex.save(self.file_path)

