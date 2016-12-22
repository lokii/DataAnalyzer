#-*- coding: UTF-8 -*-

import sys  

CSV_SPLIT = ','
DEBUG = False

class Table:
    # Parse Table from data source file such as *.csv
    @staticmethod
    def parse_from_file(file_path, sp = CSV_SPLIT):
        fd = open(file_path)                                                                                                                                                                                                                                 
        first_line = fd.readline().strip('\n')
        keys = first_line.split(sp)
        fields_total = len(keys)
        raw_table = []
        for line in fd:
            fields = line.strip('\n').split(sp)
            fields_num = len(fields)
            if (fields_num != fields_total):
                print("Fields not match: %s" % line)
                continue
            raw_table.append(fields)
        return Table(keys, raw_table) 

    def __init__(self, field_keys, raw_table):
        self.__fields_name = field_keys
        self.__raw_table = raw_table
        self.__fields_index = self.__create_field_index_cache()
        if DEBUG:
            print("Fields: %s" % self.fields())
            print("Fields total: %d" % self.fields_total())
            print("Lines total: %d" % self.lines_total())

    def __iter__(self):
        keys = self.__fields_name
        for line in self.__raw_table:
            yield dict(zip(keys, line))

    def __len__(self):
        return len(self.__raw_table) if None != self.__raw_table else 0

    def __add__(self, other):
        if self.fields() == other.fields():
            return Table(self.fields(), self.__raw_table + other.__raw_table)
        else:
            return self

    def __str__(self):
        return str(self.__raw_table)

    def __create_field_index_cache(self):
        fields_index = {}
        for key in self.__fields_name:
            fields_index[key] = self.__fields_name.index(key)
        return fields_index

    def raw_table(self):
        return self.__raw_table

    def reset(self, table):
        if None != table and self != table:
            self.__fields_name = table.__fields_name
            self.__raw_table = table.__raw_table
            self.__fields_index = table.__fields_index

    def lines_total(self):
        return len(self.__raw_table) if None != self.__raw_table else 0

    def fields_total(self):
        return len(self.fields())

    def fields(self):
        return self.__fields_name if None != self.__fields_name else []

    def get_field(self, line, field):
        index = self.__fields_index[field]
        return line[index]

    # Split table by column values
    def filter_by_value(self, field, values, convertor = None):
        results = {}
        index = self.__fields_index[field]
        for line in self.__raw_table:
            v = line[index]
            try:
                if None != convertor:
                    v = convertor(line[index])
            except:
                print("Error occurred when handle '%s'!" % (line[index]))
            else:
                if v in values:
                    if v in results:
                        results[v].append(line)
                    else:
                        results[v] = [line]
        for (k, v) in results.items():
            results[k] = Table(self.fields(), v)
        return results

    # Split table by condition
    def split_by_condition(self, field, condition, convertor = None):
        results = {"True" : [], "False" : []}
        index = self.__fields_index[field]
        for line in self.__raw_table:
            v = line[index]
            try:
                if None != convertor:
                    v = convertor(line[index])
                if condition(v):
                    results["True"].append(line)
                else:
                    results["False"].append(line)
            except:
                print("Error occurred when handle line!")

        return {"True" : Table(self.fields(), results["True"]), "False" : Table(self.fields(), results["False"])}

    def operation_in_field(self, field, operator, convertor = None):
        if None == operator or None == field:
            return None
        index = self.__fields_index[field]
        for line in self.__raw_table:
            try:
                v = line[index] if None == convertor else convertor(line[index])
                line[index] = operator(v)
            except:
                print("Error occurred in operation: %s" % str(operator))

        return result

    def unique(self, field):
        index = self.__fields_index[field]
        uniq = {}
        for line in self.__raw_table:
            key = line[index]
            if key not in uniq:
                uniq[key] = line
        return Table(self.fields(), list(uniq.values()))

    def sort(self, field, reverse = False):
        index = self.__fields_index[field]
        self.__raw_table.sort(index, reverse)

if __name__ == "__main__":
    if len(sys.argv) == 1:                                                                                                                                                                                                                                     
        print("Usage:")                                                                                                                                                                                                                                        
        print("%s data_source_file" % sys.argv[0])                                                                                                                                                                                                           
    else:                                                                                                                                                                                                                                                      
        table = Table.parse_from_file(sys.argv[1])
        print(table.raw_table())
