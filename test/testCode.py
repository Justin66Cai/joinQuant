# coding: utf-8
if __name__ == '__main__':
    import jqsdk
    import time
    presentTime= time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    params = {
        'token':'13f926af96e71677cc7ffc94454c892d',  # 在客户端系统设置中找，字符串格式，例如 'asdf...'
        'algorithmId':6, # 在客户端我的策略中，整数型，例如：1；回测结束后在客户端此ID策略的回测列表中找对应的回测结果
        'baseCapital':1000000,
        'frequency':'day',
        'startTime':'2019-10-05',
        'endTime':'2019-11-06',
        'name':"Test%s"%presentTime,
    }
    jqsdk.run(params)
# from jqdatasdk import *
import jqdata
from jqdata import finance
def initialize(context):
    # run_daily(period, time='every_bar')
    # g.security = '000001.XSHE'
    # 例子
    # 获取 市值表.股票代码，资产负债表.未分配利润
    q = query(finance.STK_COMPANY_INFO).filter(finance.STK_COMPANY_INFO.code == '600276.XSHG').limit(10)
    df = get_fundamentals(q,'2019-10-31')
    print(df)

#
# def period(context):
#     order(g.security, 100)
#     # 打印所有键
#     print(context.portfolio.positions.keys())
#     # 打印所有值
#     print(context.portfolio.positions.values())
#     # 打印g.security的开仓均价
#     print(context.portfolio.positions[g.security].avg_cost)