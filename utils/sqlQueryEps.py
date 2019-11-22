from jqdatasdk import *
import jqdatasdk
from jqdatasdk import finance

from utils.Log import Log

log=Log()
def queryCompanyName(companyCode,date='2019-06-30'):
    # 查询公司名称
    q=query(finance.STK_CASHFLOW_STATEMENT_PARENT.company_name,
             ).filter(finance.STK_CASHFLOW_STATEMENT_PARENT.code==companyCode  ,
                        finance.STK_CASHFLOW_STATEMENT_PARENT.end_date==date
                      )
    df=finance.run_query(q)
    # print(df)
    s = str(df.company_name).split()
    log.info("查询公司名称:"+s[1])
    return  s[1]

def queryeps(pe,capital,eps,date):
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
        income.basic_eps,
        # balance.cash_equivalents,
        # cash_flow.goods_sale_and_service_render_cash
    ).filter(
        # valuation.code.in_(indexs)
        valuation.pe_ratio < pe,
        valuation.pe_ratio >= 1,
        valuation.pe_ratio_lyr < valuation.pe_ratio,

        valuation.capitalization < capital*10000,
        income.basic_eps > eps,
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
    log.info("%s每股收益赛选结果:%s"%(date,str(liststock)))
    return liststock


def queryIndividualStock(listStockCode,date,growthRate=None):
    """
     查询个股收益率
    :param listStockCode:
    :param date:
    :param growthRate: 每股收益增长率
    :return:
    """
    res=[]
    for i in range(0,len(listStockCode)):
        q = query(
            income.statDate,
            income.code,
            income.basic_eps,

        ).filter(
            valuation.code==listStockCode[i][1]

        )
        rets = get_fundamentals(q, statDate=date)
        a=str(rets).split()[4:]
        # print("----------:",a)
        # print("rets:",rets)
        if 'Empty' not in str(rets):
            subEps= float(listStockCode[i][2])-float(a[2])
            rateEps=subEps/float(a[2])
            if subEps>0:
                if growthRate:
                    if rateEps > growthRate:
                        # log.info("%s每股收益成长率:%s"%(date,str(rateEps)))
                        rateEpsPer=str(int(rateEps*100))+"%"
                        a.append(rateEpsPer)
                        res.append(a)
                else:
                    res.append(a)


    log.info("%s的股票:%s"%(date, res))
    return res
if __name__ == '__main__':
    jqdatasdk.auth("15316052081", "052081")
    listCode=[['2018-12-31', '603156.XSHG', '3.8024'], ['2018-12-31', '603260.XSHG', '4.19'], ['2018-12-31', '000423.XSHE', '3.1878'], ['2018-12-31', '603799.XSHG', '1.84'], ['2018-12-31', '603858.XSHG', '2.1309'], ['2018-12-31', '002508.XSHE', '1.55'], ['2018-12-31', '600511.XSHG', '1.8313'], ['2018-12-31', '603225.XSHG', '1.69'], ['2018-12-31', '600338.XSHG', '1.3793'], ['2018-12-31', '600260.XSHG', '1.28'], ['2018-12-31', '600486.XSHG', '2.889'], ['2018-12-31', '600729.XSHG', '2.04'], ['2018-12-31', '601689.XSHG', '1.04'], ['2018-12-31', '600323.XSHG', '1.14'], ['2018-12-31', '600859.XSHG', '1.548'], ['2018-12-31', '000636.XSHE', '1.14'], ['2018-12-31', '002818.XSHE', '1.67'], ['2018-12-31', '000676.XSHE', '0.7388'], ['2018-12-31', '002430.XSHE', '0.77'], ['2018-12-31', '000726.XSHE', '0.9'], ['2018-12-31', '002597.XSHE', '1.62'], ['2018-12-31', '000034.XSHE', '0.7834'], ['2018-12-31', '603730.XSHG', '1.36'], ['2018-12-31', '000525.XSHE', '1.0959999999999999'], ['2018-12-31', '600781.XSHG', '1.42'], ['2018-12-31', '002035.XSHE', '0.7748'], ['2018-12-31', '000666.XSHE', '1.08'], ['2018-12-31', '600596.XSHG', '1.8002'], ['2018-12-31', '601900.XSHG', '0.73'], ['2018-12-31', '601311.XSHG', '0.66'], ['2018-12-31', '000951.XSHE', '1.35'], ['2018-12-31', '000042.XSHE', '0.6719'], ['2018-12-31', '603113.XSHG', '1.88'], ['2018-12-31', '002626.XSHE', '1.11'], ['2018-12-31', '002709.XSHE', '1.35'], ['2018-12-31', '002543.XSHE', '0.85'], ['2018-12-31', '600641.XSHG', '1.2091'], ['2018-12-31', '603298.XSHG', '0.88'], ['2018-12-31', '002016.XSHE', '0.9841'], ['2018-12-31', '000501.XSHE', '1.39'], ['2018-12-31', '000048.XSHE', '1.1193'], ['2018-12-31', '600694.XSHG', '3.36'], ['2018-12-31', '600054.XSHG', '0.78'], ['2018-12-31', '600508.XSHG', '0.92'], ['2018-12-31', '300349.XSHE', '1.17'], ['2018-12-31', '002258.XSHE', '1.1019'], ['2018-12-31', '603367.XSHG', '1.11'], ['2018-12-31', '000672.XSHE', '1.81'], ['2018-12-31', '002317.XSHE', '0.54'], ['2018-12-31', '603368.XSHG', '2.04'], ['2018-12-31', '000789.XSHE', '1.8547'], ['2018-12-31', '600230.XSHG', '2.406'], ['2018-12-31', '002327.XSHE', '0.65'], ['2018-12-31', '002048.XSHE', '1.17'], ['2018-12-31', '002293.XSHE', '0.7237'], ['2018-12-31', '600933.XSHG', '0.55'], ['2018-12-31', '603357.XSHG', '1.35'], ['2018-12-31', '600761.XSHG', '0.79'], ['2018-12-31', '603609.XSHG', '0.66'], ['2018-12-31', '603556.XSHG', '0.68'], ['2018-12-31', '002449.XSHE', '0.7204'], ['2018-12-31', '600195.XSHG', '0.6907'], ['2018-12-31', '000818.XSHE', '0.73'], ['2018-12-31', '600897.XSHG', '1.6979'], ['2018-12-31', '000546.XSHE', '0.5245'], ['2018-12-31', '600987.XSHG', '0.96'], ['2018-12-31', '600198.XSHG', '0.6571'], ['2018-12-31', '000065.XSHE', '0.77'], ['2018-12-31', '000926.XSHE', '1.17'], ['2018-12-31', '603980.XSHG', '1.406'], ['2018-12-31', '603055.XSHG', '0.63'], ['2018-12-31', '600197.XSHG', '0.9703'], ['2018-12-31', '000910.XSHE', '1.31'], ['2018-12-31', '600326.XSHG', '0.52'], ['2018-12-31', '603808.XSHG', '1.08'], ['2018-12-31', '603869.XSHG', '1.08'], ['2018-12-31', '601677.XSHG', '0.84'], ['2018-12-31', '300107.XSHE', '1.1996'], ['2018-12-31', '300423.XSHE', '1.65'], ['2018-12-31', '600742.XSHG', '0.97'], ['2018-12-31', '300184.XSHE', '0.5423'], ['2018-12-31', '600720.XSHG', '0.8435'], ['2018-12-31', '600389.XSHG', '1.3202'], ['2018-12-31', '000043.XSHE', '1.2844'], ['2018-12-31', '000639.XSHE', '0.62'], ['2018-12-31', '603898.XSHG', '1.22'], ['2018-12-31', '603599.XSHG', '1.25'], ['2018-12-31', '600636.XSHG', '1.2151'], ['2018-12-31', '600475.XSHG', '0.7496'], ['2018-12-31', '300438.XSHE', '0.95'], ['2018-12-31', '603639.XSHG', '2.19'], ['2018-12-31', '600738.XSHG', '2.023'], ['2018-12-31', '603306.XSHG', '0.9'], ['2018-12-31', '600810.XSHG', '1.47'], ['2018-12-31', '600075.XSHG', '0.51'], ['2018-12-31', '600551.XSHG', '0.6516'], ['2018-12-31', '000822.XSHE', '0.66'], ['2018-12-31', '603839.XSHG', '0.7'], ['2018-12-31', '603167.XSHG', '0.83'], ['2018-12-31', '002101.XSHE', '0.63'], ['2018-12-31', '002756.XSHE', '1.08'], ['2018-12-31', '002068.XSHE', '0.5518'], ['2018-12-31', '601137.XSHG', '0.59'], ['2018-12-31', '600723.XSHG', '0.5529999999999999'], ['2018-12-31', '600668.XSHG', '1.71'], ['2018-12-31', '603900.XSHG', '0.62'], ['2018-12-31', '600114.XSHG', '0.51'], ['2018-12-31', '600826.XSHG', '0.54'], ['2018-12-31', '300132.XSHE', '1.0374'], ['2018-12-31', '603365.XSHG', '1.07'], ['2018-12-31', '002039.XSHE', '1.2043'], ['2018-12-31', '603612.XSHG', '0.6'], ['2018-12-31', '000708.XSHE', '1.135'], ['2018-12-31', '002918.XSHE', '1.53'], ['2018-12-31', '300427.XSHE', '0.65'], ['2018-12-31', '603871.XSHG', '2.485'], ['2018-12-31', '603801.XSHG', '1.7056'], ['2018-12-31', '603458.XSHG', '2.83'], ['2018-12-31', '002391.XSHE', '0.8886'], ['2018-12-31', '600387.XSHG', '0.66'], ['2018-12-31', '603585.XSHG', '1.73'], ['2018-12-31', '002541.XSHE', '0.79'], ['2018-12-31', '603179.XSHG', '1.37'], ['2018-12-31', '002462.XSHE', '1.31'], ['2018-12-31', '600382.XSHG', '0.83'], ['2018-12-31', '002322.XSHE', '0.66'], ['2018-12-31', '000759.XSHE', '0.63'], ['2018-12-31', '000885.XSHE', '1.1735'], ['2018-12-31', '600452.XSHG', '1.56'], ['2018-12-31', '002852.XSHE', '0.76'], ['2018-12-31', '300422.XSHE', '0.66'], ['2018-12-31', '600449.XSHG', '0.8956'], ['2018-12-31', '002612.XSHE', '0.5261'], ['2018-12-31', '600480.XSHG', '0.6'], ['2018-12-31', '603916.XSHG', '0.88'], ['2018-12-31', '603035.XSHG', '1.21'], ['2018-12-31', '603358.XSHG', '0.66'], ['2018-12-31', '603788.XSHG', '1.09'], ['2018-12-31', '000736.XSHE', '1.82'], ['2018-12-31', '000922.XSHE', '0.5689'], ['2018-12-31', '002394.XSHE', '1.21'], ['2018-12-31', '600479.XSHG', '0.6102'], ['2018-12-31', '603686.XSHG', '0.8'], ['2018-12-31', '300121.XSHE', '1.01'], ['2018-12-31', '002561.XSHE', '0.56'], ['2018-12-31', '300272.XSHE', '0.73'], ['2018-12-31', '600995.XSHG', '0.62'], ['2018-12-31', '002208.XSHE', '0.7734'], ['2018-12-31', '002536.XSHE', '0.74'], ['2018-12-31', '002775.XSHE', '0.5265'], ['2018-12-31', '002088.XSHE', '0.85'], ['2018-12-31', '002753.XSHE', '0.8341'], ['2018-12-31', '600328.XSHG', '0.61'], ['2018-12-31', '600716.XSHG', '0.6027'], ['2018-12-31', '603100.XSHG', '0.98'], ['2018-12-31', '603385.XSHG', '0.65'], ['2018-12-31', '600697.XSHG', '1.63'], ['2018-12-31', '002116.XSHE', '0.51'], ['2018-12-31', '600802.XSHG', '0.88'], ['2018-12-31', '600173.XSHG', '0.8'], ['2018-12-31', '603165.XSHG', '1.17'], ['2018-12-31', '603776.XSHG', '0.89'], ['2018-12-31', '603968.XSHG', '0.98'], ['2018-12-31', '002884.XSHE', '1.8'], ['2018-12-31', '300437.XSHE', '1.1314'], ['2018-12-31', '603518.XSHG', '1.58'], ['2018-12-31', '603086.XSHG', '2.24'], ['2018-12-31', '600097.XSHG', '0.58'], ['2018-12-31', '002788.XSHE', '0.94'], ['2018-12-31', '603878.XSHG', '0.99'], ['2018-12-31', '603809.XSHG', '1.078'], ['2018-12-31', '603757.XSHG', '1.43'], ['2018-12-31', '603208.XSHG', '1.89'], ['2018-12-31', '600250.XSHG', '0.72'], ['2018-12-31', '603037.XSHG', '1.21'], ['2018-12-31', '600051.XSHG', '0.8'], ['2018-12-31', '603701.XSHG', '0.78'], ['2018-12-31', '603319.XSHG', '1.2'], ['2018-12-31', '000779.XSHE', '0.624'], ['2018-12-31', '600793.XSHG', '1.6568']]

    a=queryIndividualStock(listCode,'2017')
    # b=queryIndividualStock(a,'2019q1')