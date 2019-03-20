# coding: utf-8
"""
Created on 2019/3/12,11:20 AM

By Alex_HJY
"""
import matplotlib.pyplot as plt
from django.shortcuts import render
from copy import deepcopy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from dateutil import parser
from datetime import datetime as dt
from dateutil import relativedelta

from web_position_excle.migrations import ETF100联结头寸表DATA
from web_position_excle.migrations import 保险分级头寸表DATA
from web_position_excle.migrations.update_excle import update_data

plt.rcParams['font.sans-serif'] = ['STHeiti']
plt.rcParams['axes.unicode_minus'] = False


def index(request):
    update_data()
    dict0 = {'today': dt.now().date().__str__(),
             'day': dt.now().day,
             'T1': (dt.now()+relativedelta.relativedelta(days=1)).day}
    dict1 = 保险分级头寸表DATA.get_data()
    dict2 = ETF100联结头寸表DATA.get_data()
    dict0.update(dict1)
    dict0.update(dict2)
    return render(request, 'index.html', dict0)
