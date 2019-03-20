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
from dateutil import relativedelta
from decimal import Decimal


def get_excel_df():
    return pd.read_excel('web_position_excle/data/头寸表.xlsx', encoding='utf-8-sig')


def get_data():
    df = get_excel_df()
    print(df)
    data_dict = {
        '保险分级银行存款': 95049944.40,
        '保险分级证券清算款': -34646412.69,
        '保险分级银行间债券交易': 0,
        '保险分级银行间回购交易': 0,
        '保险分级T日赎回款': -6581415.79,
        '保险分级T1日赎回款': -15450117.18,
        '保险分级TA预确认赎回数据': -6326100,
        '保险分级股票红利': 0,
        '保险分级冻结保证金备付金': 0,
        '保险分级冻结信批费': 0,
        '保险分级冻结管理费托管费': 0,
        '保险分级冻结预估网下申购款': 0,

        '保险分级交易所回购到期': 0,
        '保险分级银行间回购到期': 0,
        '保险分级T日申购款': 10564316.88,
        '保险分级T1日头寸': 42610215.62,

        '保险分级基金净值': 568685607.62,
        '保险分级活期存款保证': 6.01,

    }
    for k, v in data_dict.items():
        data_dict[k] = Decimal(str(v))

    data_dict['保险分级T日头寸'] = data_dict['保险分级银行存款'] + data_dict['保险分级证券清算款'] + \
                            data_dict['保险分级T日赎回款'] + data_dict['保险分级T1日赎回款'] + data_dict['保险分级TA预确认赎回数据'] + \
                            data_dict['保险分级股票红利'] + data_dict['保险分级冻结保证金备付金'] + data_dict['保险分级冻结管理费托管费'] \
                            + data_dict['保险分级冻结信批费'] + data_dict['保险分级冻结预估网下申购款'] + data_dict['保险分级交易所回购到期'] \
                            + data_dict['保险分级银行间回购到期']

    data_dict['保险分级T日活期存款正算'] = data_dict['保险分级银行存款'] + data_dict['保险分级证券清算款'] + \
                                data_dict['保险分级T日赎回款'] + \
                                data_dict['保险分级股票红利'] + data_dict['保险分级冻结保证金备付金'] + \
                                + data_dict['保险分级银行间回购到期'] + data_dict['保险分级T日申购款']

    data_dict['保险分级T日活期存款倒算'] = data_dict['保险分级T1日头寸'] - data_dict['保险分级冻结预估网下申购款'] - data_dict['保险分级冻结管理费托管费'] \
                                - (data_dict['保险分级T1日赎回款'] + data_dict['保险分级TA预确认赎回数据'])

    data_dict['保险分级T1日活期存款倒算'] = data_dict['保险分级T1日头寸'] - data_dict['保险分级冻结预估网下申购款'] - data_dict['保险分级冻结管理费托管费'] \
                                 - (data_dict['保险分级冻结信批费'] + data_dict['保险分级TA预确认赎回数据'])

    data_dict['保险分级T1日活期存款正算'] = data_dict['保险分级银行存款'] + data_dict['保险分级证券清算款'] + \
                                 data_dict['保险分级T日赎回款'] + data_dict['保险分级T1日赎回款'] + \
                                 data_dict['保险分级股票红利'] + data_dict['保险分级冻结保证金备付金'] + \
                                 + data_dict['保险分级银行间回购到期'] + data_dict['保险分级交易所回购到期'] + data_dict['保险分级T日申购款']

    data_dict['保险分级至少留活期存款'] = data_dict['保险分级基金净值'] * data_dict['保险分级活期存款保证'] / Decimal('100')

    data_dict['保险分级日日终活期存款估计'] = data_dict['保险分级T1日活期存款正算']

    data_dict['保险分级需要卖出'] = data_dict['保险分级至少留活期存款'] - data_dict['保险分级日日终活期存款估计']

    for k, v in data_dict.items():
        data_dict[k] = format(v, ',.02f')

    return data_dict


if __name__ == '__main__':
    get_data()
