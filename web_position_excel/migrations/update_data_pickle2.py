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


def read_settings():

    settings = {'email': 'huangjy@founderff.com',
               'password': 'Abc12345',
               'pop3_server': 'mail.founderff.com',
               'ETF头寸表邮件序号': 8,
               '保险分级投头寸表（带TA数据）邮件序号': 9,
               'ETF100基金净值': 0,
               '保险分级基金净值': 0}

    with open('settings.txt', 'rb') as f:
        for i in f.readlines():
            settings[i.decode().strip().split(':')[0]] = i.decode().strip().split(':')[1].strip()

    print(settings)

    settings['ETF头寸表邮件序号']=int(settings['ETF头寸表邮件序号'])
    settings['保险分级投头寸表（带TA数据）邮件序号']=int(settings['保险分级投头寸表（带TA数据）邮件序号'])
    settings['ETF100基金净值']=float(settings['ETF100基金净值'])
    settings['保险分级基金净值']=float(settings['保险分级基金净值'])

    return settings


settings = read_settings()

def update_baoxian_data(cursor, data1):
    print(data1)
    settings = read_settings()
    data_dict = {
        '保险分级日期': data1['日期'],
        '保险分级银行存款': data1['银行存款'],
        '保险分级证券清算款': data1['证券清算款'],
        '保险分级银行间债券交易': data1['银行间债券交易'],
        '保险分级银行间回购交易': data1['银行间回购交易'],
        '保险分级T日赎回款': data1['T日赎回款'],
        '保险分级T1日赎回款': data1['T+1日赎回款'],
        '保险分级股票红利': data1['股票红利'],
        '保险分级冻结保证金备付金': data1['冻结备付金、保证金'],
        '保险分级冻结信批费': data1['冻结信批费'],
        '保险分级冻结管理费托管费': data1['冻结管理费、托管费'],
        '保险分级冻结预估网下申购款': data1['冻结预估网下申购款'],
        '保险分级TA预确认赎回数据': data1['TA预确认赎回数据'],
        '保险分级交易所回购到期': data1['交易所回购到期'],
        '保险分级银行间回购到期': data1['银行间回购到期'],
        '保险分级T日申购款': data1['T日申购款'],
        '保险分级基金净值': settings['保险分级基金净值'],
                    # get_data_oracle(cursor,
                    #                 "select FZQSZ from    GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A007' and FDATE like to_date('" + yestoday + "','yyyy-mm-dd') and FKMBM like '701基金资产净值%'"),
        '保险分级活期存款保证': 6.01,

    }
    for k, v in data_dict.items():
        if k != '保险分级日期':
            data_dict[k] = Decimal(str(v))

    data_dict['保险分级T日头寸'] = data_dict['保险分级银行存款'] + data_dict['保险分级证券清算款'] + \
                            data_dict['保险分级T日赎回款'] + data_dict['保险分级T1日赎回款'] + data_dict['保险分级TA预确认赎回数据'] + \
                            data_dict['保险分级股票红利'] + data_dict['保险分级冻结保证金备付金'] + data_dict['保险分级冻结管理费托管费'] \
                            + data_dict['保险分级冻结信批费'] + data_dict['保险分级冻结预估网下申购款'] + data_dict['保险分级交易所回购到期'] \
                            + data_dict['保险分级银行间回购到期']

    data_dict['保险分级T1日头寸'] = data_dict['保险分级T日头寸'] + data_dict['保险分级交易所回购到期'] + data_dict['保险分级银行间回购到期'] \
                             + data_dict['保险分级T日申购款']

    data_dict['保险分级T日活期存款正算'] = data_dict['保险分级银行存款'] + data_dict['保险分级证券清算款'] + \
                                data_dict['保险分级T日赎回款'] +data_dict['保险分级交易所回购到期']+ \
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
        if k != '保险分级日期':
            data_dict[k] = format(v, ',.02f')

    with open('./web_position_excel/data/baoxian.pkl', 'wb')as f:
        f.write(pickle.dumps(data_dict))

    return data_dict


def update_ETF100_data(cursor, data2):
    print(data2)
    settings = read_settings()
    data_dict = {
        'ETF100日期': data2['日期'],
        'ETF100银行存款': data2['银行存款'],
        'ETF100清算款': data2['清算款'],
        'ETF100银行间回购交易': data2['银行间回购交易'],
        'ETF100交易间回购交易': data2['交易间回购交易'],
        'ETF100T日赎回款': data2['T日赎回款'],
        'ETF100T1日赎回款': data2['T+1日赎回款'],
        'ETF100债券付息': data2['债券付息'],
        'ETF100冻结保证金备付金': data2['冻结保证金、备付金'],
        'ETF100冻结管理费托管费': data2['冻结管理费、托管费'],
        'ETF100T日头寸': data2['T日头寸'],
        'ETF100交易所回购到期': data2['交易所回购到期'],
        'ETF100银行间债券交易': data2['银行间债券交易'],
        'ETF100银行间回购到期': data2['银行间回购到期'],
        'ETF100T日申购款': data2['T日申购款'],
        'ETF100T1日头寸': data2['T+1日头寸'],

        'ETF100T1日活期存款倒算': 0,
        'ETF100T1日活期存款正算': 0,
        'ETF100基金净值': settings['ETF100基金净值'],
                    # get_data_oracle(cursor,
                    #                   "select FZQSZ from    GZ25.T_TEVALUATIONGZ25 ty where FSETCODE ='A015' and FDATE like to_date('" + yestoday + "','yyyy-mm-dd') and FKMBM like '701基金资产净值%'"),
        'ETF100活期存款保证': 6.01,
        'ETF100至少留活期存款': 0,
        'ETF100日日终活期存款估计': 0,
    }

    for k, v in data_dict.items():
        if k != 'ETF100日期':
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

    data_dict['ETF100T日活期存款预估比例'] = (data_dict['ETF100T1日活期存款正算'] / data_dict['ETF100基金净值'] * 100)
    if data_dict['ETF100T日活期存款预估比例'] <= 6 or data_dict['ETF100T日活期存款预估比例'] >= 9:
        temp = '%   ---！！！ 预警！！！'
    else:
        temp = '% '

    for k, v in data_dict.items():
        if k != 'ETF100日期' :
            data_dict[k] = format(v, ',.02f')
    data_dict['ETF100T日活期存款预估比例']=data_dict['ETF100T日活期存款预估比例'] +temp


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
    from web_position_excel.migrations.getdata_from_mail import get_data
    try:
        db = oracle.connect('FDC/fdc@172.16.109.97:5003/ttapdb01')
    except Exception as e:
        print(e)
        db = ''

    if db != '':
        # create cursor
        cursor = db.cursor()

        # execute sql
        t2, data2 = get_data(settings['ETF头寸表邮件序号'])
        t1, data1 = get_data(settings['保险分级投头寸表（带TA数据）邮件序号'])
        dict1 = update_baoxian_data(cursor, data1)
        dict2 = update_ETF100_data(cursor, data2)

        cursor.close()
        db.close()

        return dict1, dict2
    else:
        return


update_data()
