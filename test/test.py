import datetime

from jqboson.api.settings import set_benchmark
from jqdatasdk import *
import jqdatasdk
import talib as tb
from jqlib.technical_analysis import *
import numpy as np
import pandas as pd
import pandas as pd
import numpy as np
import talib as tb
import datetime
import time
# 导入技术分析库
# security_list:股票列表
#             check_date：要查询数据的日期
#             SHORT：统计的天数 SHORT
#             LONG：统计的天数 LONG
#             MID：统计的天数 MID
#             unit：统计周期，默认为 '1d'
#             include_now：是否包含当前周期，默认为 True
def get_macd(stock_list, check_date=None, unit='1d', include_now=False):
    """
    MACD计算函数，返回一个嵌套字典，Key是股票代码，Value是一个字典，不包括当前时间段的值
    stock_list：可以指定单只股票，也可以是股票列表
    check_date: 获取MACD值的日期，注意未来数据值
    unit：支持分钟 xm、天 xd、周 xw 时间段的数据
    include_now: 是否包含当前时间段的bar
    """
    macd_list = {}
    if isinstance(check_date,str):
        check_date = datetime.datetime.strptime(check_date, "%Y-%m-%d %H:%M:%S")

    '''如果股票代码是个字符串而不是一个列表，进行转换'''
    if isinstance(stock_list,str):
        stock_list = [stock_list]

    for stock in stock_list:
        '''获取指定日期之前的300个收盘价信息'''
        array = get_bars(security=stock,
                         count=500,
                         unit=unit,
                         fields=['close'],
                         include_now=include_now,
                         end_dt=check_date,
                         fq_ref_date=check_date)
        close_list = array['close']

        '''求出用300个数据推算出的dif/dea/macd集合'''
        dif, dea, macd = tb.MACD(close_list,
                                 fastperiod=12,
                                 slowperiod=26,
                                 signalperiod=9)

        '''得到最近一个交易时间段的dif/dea/macd'''
        last_dif = dif[-1]
        last_dea = dea[-1]
        last_macd = macd[-1]

        '''字典包装，用于返回'''
        macd_dic = (last_dif, last_dea, last_macd*2)
        macd_list[stock] = macd_dic

    return macd_list

re_value = get_macd(['002024.XSHE', '000001.XSHE'], check_date=datetime.datetime.now(),unit='1d', include_now=False)
dif, dea, macd = re_value['002024.XSHE']
print(dif, dea, macd)