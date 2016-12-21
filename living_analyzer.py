#!/usr/bin/python                                                                                                                                                                                                                                              
import sys  
from table_parser import TableParser

def parse_basic_info(parser):
    table = parser.table()
    total = len(table)
    print("总开播数：%d" % total)

    total_duration = 0
    for row in table:
        total_duration += int(row["live_duration"])

    print("总开播时长：%d 秒(%.2f 小时)" % (total_duration, total_duration / 3600))
    print("平均开播时长：%d 秒" % (total_duration / total))

def parse_exception_stream(parser):
    total = parser.table_lines_total()
    sub_tables = parser.split_table_by_values("ext16", [0, 1, 2], lambda v : int(v))
    normal_stop = len(sub_tables[0])
    app_abort = len(sub_tables[1])
    app_exception = len(sub_tables[2])
    exception_stop = app_exception + app_abort
    print("正常停播流：%d(%s)" % (normal_stop, format(normal_stop / total, ".2%")))
    print("异常停播流：%d(%s)，其中终端中断：%d(%s)，终端崩溃：%d(%s)" % (exception_stop, format(exception_stop / total, ".2%"), app_abort, format(app_abort / total, ".2%"), app_exception, format(app_exception / total, ".2%")))

def parse_exception_model(parser, reasons):
    table = parser.table()
    total = len(table)
    models = {}
    for row in table:
        reason = int(row["ext16"])
        if reason in reasons:
            model = row["md"]
            if model in models:
                models[row["md"]] += 1
            else:
                models[row["md"]] = 1
    top_n = 20
    print("机型排行(Top %d)：" % top_n)
    print("计次\t机型")
    md_sorted = sorted(models.items(), key=lambda d: d[1], reverse = True)
    for (k, v) in md_sorted:
        print("%s\t%s" % (v, k))
        top_n -= 1
        if 0 == top_n:
            break

def parse_exception_duration(parser, reasons):
    table = parser.table()
    total = len(table)
    durations = []
    for row in table:
        reason = int(row["ext16"])
        if reason in reasons:
            duration = row["live_duration"]
            durations.append(int(duration))
    top_n = 20
    print("时长排行(Top %d)：" % top_n)
    print("开播时长（秒）")
    durations.sort(reverse = True)
    for d in durations:
        print("%d" % d)
        top_n -= 1
        if 0 == top_n:
            break

if __name__ == "__main__":
    if len(sys.argv) == 1:                                                                                                                                                                                                                                     
        print("Usage:")                                                                                                                                                                                                                                        
        print("%s data_source_file" % sys.argv[0])                                                                                                                                                                                                           
    else:                                                                                                                                                                                                                                                      
        parser = TableParser(sys.argv[1])
        parse_basic_info(parser)
        parse_exception_stream(parser)
        parse_exception_model(parser, [1, 2])
        parse_exception_duration(parser, [1])
        #split_table_by_values(table, "ext16", [1, 2], lambda v : int(v))
        #print(split_table_by_condition(table, "ext16", lambda v : v == 2, lambda v : int(v)))
