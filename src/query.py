from openpyxl import load_workbook
from openpyxl import Workbook

class Query:
    def __init__(self, query):
       self.query = query
       self.query_expansion_list = []

    def query_expand(self, query_expand_impl):
        self.query_expansion_list = query_expand_impl.expand(self.query)

    def print_query_expansion(self):
        print(self.query_expansion_list)

class QueryExpandImpl:
    def __init__(self, query_expand_workbook_path):
        self.query_expand_backend_dict = {}
        self.build_backend(query_expand_workbook_path)

    def build_backend(self, query_expand_workbook_path):
        query_expand_workbook = load_workbook(filename = query_expand_workbook_path, read_only = True, data_only = True)
        query_expand_sheet = query_expand_workbook["关键词组"]
        for rows in query_expand_sheet.iter_rows(values_only = True):
            query = rows[0]
            if query:
                query = query.replace(" ", "")
                query_expansion_list = self.cell_tuple_to_list(rows)
                self.query_expand_backend_dict[query] = query_expansion_list
    
    def cell_tuple_to_list(self, cell_tuple):
        cell_list = []
        for cell in cell_tuple:
            if cell:
                cell = cell.replace(" ", "")
                cell_list.append(cell)
        return cell_list

    def expand(self, query):
        if query in self.query_expand_backend_dict:
            return self.query_expand_backend_dict[query]
        return query

    

        
