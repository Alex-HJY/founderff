# coding: utf-8
"""
Created on 2019/3/13,10:41 AM

By Alex_HJY
"""
from copy import deepcopy

import numpy as np
import pandas as pd

from datetime import timedelta
from dateutil import parser
from datetime import datetime
from dateutil import relativedelta
import cx_Oracle as oracle
from decimal import Decimal
import pickle
import sys
import codecs

today = (datetime.now().date() - relativedelta.relativedelta(days=1)).__str__()
today = '2019-3-12'
yestoday = '2019-3-11'
tomorrow = '2019-3-13'
print(today)

def update_baoxian_data(cursor):

    data_dict = {
        '保险分级银行存款': get_data_oracle(cursor,
                                    "select FZQCB from GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A007' and FDATE like to_date ('" + yestoday + "','yyyy-mm-dd') and FKMBM ='1002'"),
        '保险分级证券清算款': get_data_oracle(cursor,
                                     "select FZQCB from GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A007' and FDATE like to_date ('" + yestoday + "','yyyy-mm-dd') and FKMBM ='3003'"),
        '保险分级银行间债券交易': 0,
        '保险分级银行间回购交易': 0,
        '保险分级T日赎回款': -get_data_oracle(cursor,
                                      "select sum(FBBAL) from  GZ25.T_FCWVCH ty where FSETCODE ='A007' and FDATE like to_date ('" + today + "','yyyy-mm-dd') and FVCHZY like '%赎回%款项' and FJD like 'J'"),
        '保险分级T1日赎回款': -get_data_oracle(cursor,
                                       "select sum(FBBAL) from  GZ25.T_FCWVCH ty where FSETCODE ='A007' and FDATE like to_date ('" + tomorrow + "','yyyy-mm-dd') and FVCHZY like '%赎回%款项' and FJD like 'J'"),
        '保险分级股票红利': 0,
        '保险分级冻结保证金备付金': 0,
        '保险分级冻结信批费': 0,
        '保险分级冻结管理费托管费': 0,
        '保险分级冻结预估网下申购款': 0,
        '保险分级TA预确认赎回数据'  :-6326100.00,
        '保险分级交易所回购到期': 0,
        '保险分级银行间回购到期': 0,
        '保险分级T日申购款': get_data_oracle(cursor,
                                     "select FBBAL from    GZ25.T_FCWVCH ty where FSETCODE ='A007' and FDATE like to_date ('" + today + "','yyyy-mm-dd') and FVCHZY like '%申购款项%' and FJD like 'J'"),
        '保险分级基金净值': get_data_oracle(cursor,
                                    "select FZQSZ from    GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A007' and FDATE like to_date('" + yestoday + "','yyyy-mm-dd') and FKMBM like '701基金资产净值%'"),
        '保险分级活期存款保证': 6.01,

    }
    for k, v in data_dict.items():
        data_dict[k] = Decimal(str(v))

    data_dict['保险分级T日头寸'] = data_dict['保险分级银行存款'] + data_dict['保险分级证券清算款'] + \
                            data_dict['保险分级T日赎回款'] + data_dict['保险分级T1日赎回款'] + data_dict['保险分级TA预确认赎回数据'] + \
                            data_dict['保险分级股票红利'] + data_dict['保险分级冻结保证金备付金'] + data_dict['保险分级冻结管理费托管费'] \
                            + data_dict['保险分级冻结信批费'] + data_dict['保险分级冻结预估网下申购款'] + data_dict['保险分级交易所回购到期'] \
                            + data_dict['保险分级银行间回购到期']

    data_dict['保险分级T1日头寸'] = data_dict['保险分级T日头寸'] + data_dict['保险分级交易所回购到期'] + data_dict['保险分级银行间回购到期'] \
                             + data_dict['保险分级T日申购款']

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

    # data_dict['保险分级TA预确认赎回数据']= data_dict['保险分级T日活期存款正算'] - data_dict['保险分级T1日头寸'] - data_dict['保险分级冻结信批费'] \
    #                             - data_dict['保险分级冻结管理费托管费'] - data_dict['保险分级冻结预估网下申购款']

    data_dict['保险分级至少留活期存款'] = data_dict['保险分级基金净值'] * data_dict['保险分级活期存款保证'] / Decimal('100')

    data_dict['保险分级日日终活期存款估计'] = data_dict['保险分级T1日活期存款正算']

    data_dict['保险分级需要卖出'] = data_dict['保险分级至少留活期存款'] - data_dict['保险分级日日终活期存款估计']

    for k, v in data_dict.items():
        data_dict[k] = format(v, ',.02f')

    with open('./web_position_excel/data/baoxian.pkl', 'wb')as f:
        f.write(pickle.dumps(data_dict))

    return data_dict


def update_ETF100_data(cursor):
    data_dict = {
        'ETF100银行存款':get_data_oracle(cursor,
                                    "select FZQCB from GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A015' and FDATE like to_date ('" + yestoday + "','yyyy-mm-dd') and FKMBM ='1002'"),
        'ETF100清算款':get_data_oracle(cursor,
                                     "select FZQCB from GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A015' and FDATE like to_date ('" + yestoday + "','yyyy-mm-dd') and FKMBM ='3003'"),
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
        'ETF100基金净值': get_data_oracle(cursor,
                                    "select FZQSZ from    GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A015' and FDATE like to_date('" + yestoday + "','yyyy-mm-dd') and FKMBM like '701基金资产净值%'"),
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

    with open('./web_position_excel/data/ETF100.pkl', 'wb')as f:
        f.write(pickle.dumps(data_dict))

    return data_dict


def get_data_oracle(cursor, ss):
    cursor.execute(ss)
    data = cursor.fetchall()
    if len(data) != 0:
        return data[0][0]
    else:
        return 0


def update_data():
    import os
    os.environ["NLS_LANG"] = ".AL32UTF8"
    # connect oracle database

    try:
        db = oracle.connect('FDC/fdc@172.16.109.97:5003/ttapdb01')
    except Exception as e:
        print(e)
        db = ''

    if db != '':
        # create cursor
        cursor = db.cursor()

        # execute sql

        dict1 = update_baoxian_data(cursor)
        dict2 = update_ETF100_data(cursor)
        cursor.close()
        db.close()

        return dict1, dict2
    else:
        return


update_data()
