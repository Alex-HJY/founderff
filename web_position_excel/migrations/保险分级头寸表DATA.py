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
import pickle

def get_excel_pickle():
    file_path='./web_position_excel/data/baoxian.pkl'
    with open(file_path,'rb') as f:
        data_dict=pickle.loads(f)
    return data_dict


def get_data():
    file_path = './web_position_excel/data/baoxian.pkl'
    with open(file_path, 'rb') as f:
        data_dict = pickle.loads(f.read())
    return data_dict



if __name__ == '__main__':
    get_data()
