#-*- coding: UTF-8 -*-

import sys  

CSV_SPLIT = ','
DEBUG = False

class Table:
    # Parse Table from data source file such as *.csv
    @staticmethod
    def parse_from_file(file_path, sp = CSV_SPLIT):
        fd = open(file_path)                                                                                                                                                                                                                                 
        first_line = fd.readline()
        keys = first_line.split(sp)
        fields_total = len(keys)
        raw_table = []
        for line in fd:
            items = {}
            fields = line.split(sp)
            fields_num = len(fields)
            if (fields_num != fields_total):
                print("Fields not match: %s" % line)
                continue
            for index in range(fields_num):
                items[keys[index]] = fields[index]
            raw_table.append(items)
        return Table(raw_table) 

    def __init__(self, raw_table):
        self.__raw_table = tuple(raw_table)
        if DEBUG:
            print("Fields: %s" % self.fields())
            print("Fields total: %d" % self.fields_total())
            print("Lines total: %d" % self.lines_total())

    def __iter__(self):
        for i in self.__raw_table:
            yield i

    def __len__(self):
        return len(self.__raw_table) if None != self.__raw_table else 0

    def __add__(self, other):
        return Table(self.__raw_table + other.__raw_table)

    def raw_table(self):
        return self.__raw_table

    def reset(self, raw_table):
        if None != raw_table and self.__raw_table != raw_table:
            self.__raw_table = tuple(raw_table)
        return self.__raw_table

    def lines_total(self):
        return len(self.__raw_table) if None != self.__raw_table else 0

    def fields_total(self):
        return len(self.__raw_table[0]) if self.lines_total() > 0 else 0

    def fields(self):
        return list(self.__raw_table[0].keys()) if self.lines_total() > 0 else []

    # Split table by column values
    def split_by_values(self, field, values, type_convert = None):
        results = {}
        for line in self.__raw_table:
            v = line[field]
            try:
                if None != type_convert:
                    v = type_convert(line[field])
            except:
                print("Error occurred when handle '%s'!" % (line[field]))
            else:
                if v in values:
                    if v in results:
                        results[v].append(line)
                    else:
                        results[v] = [line]
        for (k, v) in results.items():
            results[k] = Table(v)
        return results

    # Split table by condition
    def split_by_condition(self, field, condition, type_convert = None):
        results = {"True" : [], "False" : []}
        for line in self.__raw_table:
            v = line[field]
            try:
                if None != type_convert:
                    v = type_convert(line[field])
                if condition(v):
                    results["True"].append(line)
                else:
                    results["False"].append(line)
            except:
                print("Error occurred when handle line!")

        return {"True" : Table(results["True"]), "False" : Table(results["False"])}
    
    def unique(self, field):
        uniq = {}
        for line in self.__raw_table:
            key = line[field]
            if key not in uniq:
                uniq[key] = line
        return Table(list(uniq.values()))

if __name__ == "__main__":
    if len(sys.argv) == 1:                                                                                                                                                                                                                                     
        print("Usage:")                                                                                                                                                                                                                                        
        print("%s data_source_file" % sys.argv[0])                                                                                                                                                                                                           
    else:                                                                                                                                                                                                                                                      
        table = Table.parse_from_file(sys.argv[1])
        print(table.raw_table())
