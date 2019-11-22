from jqdatasdk import *
import jqdatasdk
from jqdatasdk import finance

from utils.Log import Log

log=Log()
def queryNetProfit(pe,capital,netProfit,date):
    """
    :param pe: 市盈率(动),
    :param capital: 总股本(亿),
    :param eps: 每股收益
    :param date:时间
    :return:
    """
    q = query(
        income.statDate,
        income.code,
        income.net_profit,
        valuation.pe_ratio,
        # balance.cash_equivalents,
        # cash_flow.goods_sale_and_service_render_cash
    ).filter(
        # valuation.code.in_(indexs)
        valuation.pe_ratio < pe,
        valuation.pe_ratio > 1,
        valuation.pe_ratio_lyr > valuation.pe_ratio,
        valuation.capitalization < capital*10000,
        income.net_profit >= netProfit*1000000,
    ).order_by(
        # 按市值降序排列
        valuation.market_cap.desc()
    )
    rets = get_fundamentals(q, statDate=date)
    # 删除第一个和最后一个字符"[]"
    f = str(rets._get_values)[1:]
    l = f[:-1]
    # 转换为列表
    b = l.split('\n')
    liststock = []
    # 将列表中的字符串转换成列表
    for i in range(0, len(b)):
        c = b[i].replace('\'', '').replace('[', '').replace(']', '')
        # print(c)
        d = c.split()
        liststock.append(d)
    # print(liststock)
    log.info("%s净利润:%s"%(date,str(liststock)))
    return liststock


def queryNetProfitPer(listStockCode, date, growthRate=None):
    """
     查询个股收益率
    :param listStockCode:
    :param date:
    :param growthRate: 每股收益增长率
    :return:
    """
    res = []
    for i in range(0, len(listStockCode)):
        q = query(
            income.statDate,
            income.code,
            income.net_profit,

        ).filter(
            valuation.code == listStockCode[i][1]

        )
        rets = get_fundamentals(q, statDate=date)
        a = str(rets).split()[4:]
        # print("----------:",a)
        # print("rets:",rets)
        if 'Empty' not in str(rets):
            subNetProfit = float(listStockCode[i][2]) - float(a[2])
            rateNetProfit = subNetProfit / float(a[2])
            if subNetProfit > 0:
                if growthRate:
                    if rateNetProfit > growthRate:
                        rateNetProfitPer = str(int(rateNetProfit * 100)) + "%"
                        a.append(rateNetProfitPer)
                        res.append(a)
                else:
                    res.append(a)

    log.info("%s的股票:%s" % (date, res))
    return res