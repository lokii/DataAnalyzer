#!/usr/bin/python                                                                                                                                                                                                                                              
import sys  
from table_parser import Table

STOP_NORMAL = 0
STOP_ABORT = 1
STOP_EXCEPT = 2

class LivingAnalyzer:
    def __init__(self, table):
        self.__table = table
        self.__living_total = len(table)
        self.__total_duration = self.__table.get_field_sum("live_duration", lambda v : int(v))
        self.__user_total = len(table.unique("ext0"))

        total_stop_list = table.filter_by_value("ext16", [STOP_NORMAL, STOP_ABORT, STOP_EXCEPT], lambda v : int(v))
        self.__stop_normal_table = total_stop_list[STOP_NORMAL] if STOP_NORMAL in total_stop_list else Table([], [])
        self.__stop_abort_table = total_stop_list[STOP_ABORT] if STOP_ABORT in total_stop_list else Table([], [])
        self.__stop_except_table = total_stop_list[STOP_EXCEPT] if STOP_EXCEPT in total_stop_list else Table([], [])

        self.__stop_normal_count = len(self.__stop_normal_table)
        self.__stop_abort_count = len(self.__stop_abort_table)
        self.__stop_except_count = len(self.__stop_except_table)
        self.__not_stop_count = self.__stop_abort_count + self.__stop_except_count
        self.__model_dimension = {
                "正常停播" : self.__table,
                "异常停播" : self.__stop_abort_table + self.__stop_except_table,
                "终端中断停播" : self.__stop_abort_table,
                "终端崩溃停播" : self.__stop_except_table,
                }

    def show_basic_info(self):
        print("总开播数：%d" % self.__living_total)
        print("总开播用户：%d" % self.__user_total)
        print("总开播时长：%d(%.2f 小时)" % (self.__total_duration, self.__total_duration / 3600))
        print("正常停播流：%d(%s)" % (self.__stop_normal_count, format(self.__stop_normal_count / self.__living_total, ".2%")))
        print("异常停播流：%d(%s)，其中终端中断：%d(%s)，终端崩溃：%d(%s)"
                % (self.__not_stop_count, format(self.__not_stop_count / self.__living_total, ".2%"),
                    self.__stop_abort_count, format(self.__stop_abort_count / self.__living_total, ".2%"),
                    self.__stop_except_count, format(self.__stop_except_count / self.__living_total, ".2%")))

    @staticmethod
    def parse_model_proportion(table):
        models = table.split_by_field("md")
        return models

    @staticmethod
    def parse_user_proportion(table):
        users = {}
        users = table.split_by_field("ext0")
        return users
    
    def show_model_proportion(self):
        for (title, table) in self.__model_dimension.items():
            top_n = 10
            models = LivingAnalyzer.parse_model_proportion(table)
            print("%s的机型总数：%d" % (title, len(models)))
            print("%s机型排行(Top %d)：" % (title, top_n))
            print("计次\t分类比\t大盘比\t机型")
            md_sorted = sorted(models.items(), key=lambda d: len(d[1]), reverse = True)
            for (k, v) in md_sorted:
                c = len(v)
                print("%s\t%s\t%s\t%s" % (c, format(c / len(table), ".2%"), format(c / self.__living_total, ".2%"), k))
                top_n -= 1
                if 0 == top_n:
                    break

    def show_push_strategy_proportion(self):
        vt130 = table.filter_by_value("av", ["1.2.1.130"])["1.2.1.130"]
        total130 = len(vt130)
        if total130 > 0:
            push_strategy = (vt130.split_by_field("ext9"))
            #total_stop_except_count = len(vt130.split_by_condition("ext16", lambda v : v == 0, lambda v : int(v))["False"])
            for (k, v) in push_strategy.items():
                strategy_count = len(v)
                print("推流策略%s占比 %s" % (k, format(strategy_count / total130, ".2%")))
                push_stop_result = v.split_by_condition("ext16", lambda v : v == 0, lambda v : int(v))
                push_stop_normal_count = len(push_stop_result["True"])
                push_stop_except_count = len(push_stop_result["False"])
                print(">正常停播占比 %s" % format(push_stop_normal_count / strategy_count, ".2%"))
                print(">>异常停播占比 %s" % format(push_stop_except_count / strategy_count, ".2%"))



    def parse_exception_duration(table, reasons):
        durations = []
        for line in table:
            reason = int(line["ext16"])
            if reason in reasons:
                duration = line["live_duration"]
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
        table = Table.parse_from_file(sys.argv[1])
        table.reset(table.split_by_condition("ext0", lambda v : v == "ext0")["False"]) # 过滤多个 csv 文件拼接后多余的 fileds key

        analyzer = LivingAnalyzer(table)
        analyzer.show_basic_info()
        analyzer.show_model_proportion()
        analyzer.show_push_strategy_proportion()

        '''
        every_day = table.split_by_field("reporttime", lambda v : v[0:8])
        for (daily, t) in every_day.items():
            print("=================== %s ==================" % daily)
            analyzer = LivingAnalyzer(t)
            analyzer.show_basic_info()
            analyzer.show_model_proportion()
        '''
