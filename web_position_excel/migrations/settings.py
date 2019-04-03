# coding: utf-8




setting = {'email': 'huangjy@founderff.com',
           'password': 'Abc12345',
           'pop3_server': 'mail.founderff.com',
           'ETF头寸表邮件序号': 8,
           '保险分级投头寸表（带TA数据）邮件序号': 9,
           'ETF100基金净值': 0,
           '保险分级基金净值': 0}

with open('../../settings.txt','rb') as f:
    for i in f.readlines():
        setting[i.decode().strip().split(':')[0]]=   i.decode().strip().split(':')[1]