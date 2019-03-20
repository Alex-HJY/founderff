# coding: utf-8
"""
Created on 2019/3/13,10:25 AM

By Alex_HJY
"""
from copy import deepcopy

import numpy as np
import pandas as pd
from datetime import timedelta
from dateutil import parser
from datetime import datetime
from decimal import Decimal
from dateutil import relativedelta




def get_excel_df():
    return pd.read_excel('web_position_excle/data/头寸表.xlsx', encoding='utf-8-sig')


def get_data():
    df = get_excel_df()
    print(df)
    data_dict = {
        'ETF100银行存款': 3168681.57,
        'ETF100清算款': -1290298.17,
        'ETF100银行间回购交易': 0,
        'ETF100交易间回购交易': 0,
        'ETF100T日赎回款': -682644.01,
        'ETF100T1日赎回款': -1513704.24,
        'ETF100债券付息': 0,
        'ETF100冻结保证金备付金': 0,
        'ETF100冻结管理费托管费': 0,
        'ETF100T日头寸': -317964.85,
        'ETF100交易所回购到期': 0,
        'ETF100银行间债券交易': 0,
        'ETF100银行间回购到期': 0,
        'ETF100T日申购款': 286318.41,
        'ETF100T1日头寸': -31646.44,

        'ETF100T1日活期存款倒算': 0,
        'ETF100T1日活期存款正算': 0,
        'ETF100基金净值': 28807973.93,
        'ETF100活期存款保证': 6.01,
        'ETF100至少留活期存款': 0,
        'ETF100日日终活期存款估计': 0,
    }

    for k, v in data_dict.items():
        data_dict[k] = Decimal(str(v))

    data_dict['ETF100T日活期存款倒算'] = data_dict['ETF100T1日头寸'] - data_dict['ETF100T1日赎回款']
    data_dict['ETF100T日活期存款正算'] = data_dict['ETF100银行存款'] + data_dict['ETF100清算款'] + data_dict['ETF100T日赎回款'] + \
                                  data_dict['ETF100T日申购款']
    data_dict['ETF100T1日活期存款倒算'] = data_dict['ETF100T1日头寸'] - data_dict['ETF100冻结管理费托管费']
    data_dict['ETF100T1日活期存款正算'] = data_dict['ETF100银行存款'] + data_dict['ETF100清算款'] + data_dict['ETF100T日赎回款'] + \
                                   data_dict['ETF100T1日赎回款'] + data_dict['ETF100债券付息'] + data_dict['ETF100冻结保证金备付金'] + \
                                   data_dict['ETF100交易所回购到期'] + data_dict['ETF100银行间债券交易'] + data_dict[
                                       'ETF100银行间回购到期'] + \
                                   data_dict['ETF100T日申购款']
    data_dict['ETF100至少留活期存款'] = data_dict['ETF100基金净值'] * data_dict['ETF100活期存款保证'] / Decimal('100')

    data_dict['ETF100日日终活期存款估计'] = data_dict['ETF100T1日活期存款正算']

    data_dict['ETF100需要卖出'] = data_dict['ETF100至少留活期存款'] - data_dict['ETF100日日终活期存款估计']

    for k, v in data_dict.items():
        data_dict[k] = format(v, ',.02f')

    return data_dict

if __name__ == '__main__':
    get_data()
