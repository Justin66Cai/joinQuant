from jqdatasdk import *
import jqdatasdk
from jqdatasdk import finance
from  utils.sqlQueryEps import *
import pandas as pd
import numpy as np
from utils.sqlQueryNetProfit import *


def queryStockLittleNetProfitReport():
    #     净利润
    #     :param pe_ratio: 市盈率(动),
    #     :param capitalization: 总股本(亿),
    #     :param net_profit: 净利润
    #     :param np_parent_company_owners: 归属于母公司股东的净利润
    #     :param statDate:时间
    pe_ratio=10
    capitalization=10
    net_profit=5
    statDate='2019q3'
    dictStockName={}
    growthRate=0.3
    q3=queryNetProfit(pe_ratio, capitalization, net_profit, date='2019q3')
    q2 = queryNetProfitPer(q3, '2018q3',growthRate)
    q1 = queryNetProfitPer(q2, '2017q3',growthRate)
    for i in range(0, len(q1)):
        res = queryCompanyName(q1[i][1])
        dictStockName[res] = q1[i]
    dictStockName['stratDate'] = statDate
    print(dictStockName)
    return dictStockName

def queryStockLittlePannnualReport():
    #     每股收益
    #     :param pe_ratio: 市盈率(动),
    #     :param capitalization: 总股本(亿),
    #     :param basic_eps: 每股收益
    #     :param statDate:时间
    pe_ratio=20
    capitalization=10
    basic_eps=0.1
    statDate='2019q2'
    # 成长率
    growthRate=0.25
    dictStockName={}

    # 赛选过去3年3个季度
    for j in range(1,4):
        stockInfo = {}
        q3=queryeps(pe_ratio, capitalization, basic_eps, date='2019q%s'%j)
        q2 = queryIndividualStock(q3, '2018q%s'%j,growthRate)
        q1 = queryIndividualStock(q2, '2017q%s'%j,growthRate)
        # 将每只票子查询对应的名称
        for i in range(0,len(q1)):
            res=queryCompanyName(q1[i][1])
            stockInfo[res]=q1[i]
        dictStockName['Q%s'%j] = stockInfo
    print(dictStockName)
    return dictStockName

# rets = [get_fundamentals(q, statDate='2019q'+str(i)) for i in range(1, 4)]
if __name__ == '__main__':
    jqdatasdk.auth("15316052081", "052081")
    yearReport=str(queryStockLittlePannnualReport())
    # monthReport=str(queryStockLittleNetProfitReport())
    f = open('test.txt', 'a')
    f.write('\r')
    f.write(yearReport)
    f.close()