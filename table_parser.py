#-*- coding: UTF-8 -*-

import sys  

CSV_SPLIT = ','

class TableParser:
    def __init__(self, file_path, split = CSV_SPLIT):
        self._fd = open(file_path)                                                                                                                                                                                                                                 
        self._table = self.parse_data_source(self._fd, split)

    def table(self):
        return self._table

    def table_lines_total(self):
        return len(self._table)

    def table_fields_total(self):
        return len(self._table)

    # Parse table from data source file such as *.csv
    def parse_data_source(self, fd, split):
        first = fd.readline()
        keys = first.split(split)
        cols_total = len(keys)
        table = []
        for line in fd:
            row = {}
            cols = line.split(CSV_SPLIT)
            cols_num = len(cols)
            if (cols_num != cols_total):
                print("Fields not match: %s" % line)
                continue
            for index in range(cols_num):
                row[keys[index]] = cols[index]
            table.append(row)
        print("Fields total: %d" % cols_total)
        print("Lines total: %d" % len(table))
        return table 

    # Split table by column values
    def split_table_by_values(self, col_name, values, type_convert):
        results = {}
        for row in self._table:
            v = type_convert(row[col_name])
            if v in values:
                if v in results:
                    results[v].append(row)
                else:
                    results[v] = [row]
        return results

    # Split table by condition
    def split_table_by_condition(self, col_name, condition, type_convert):
        results = {}
        for row in self._table:
            v = type_convert(row[col_name])
            if condition(v):
                if v in results:
                    results[v].append(row)
                else:
                    results[v] = [row]
        return results


if __name__ == "__main__":
    if len(sys.argv) == 1:                                                                                                                                                                                                                                     
        print("Usage:")                                                                                                                                                                                                                                        
        print("%s data_source_file" % sys.argv[0])                                                                                                                                                                                                           
    else:                                                                                                                                                                                                                                                      
        parser = TableParser(sys.argv[1])
        print(parser._table)
