
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
import calendar
import collections

#%%
'Create dataframes for each data table in Input Data Sheet'

df0 = pd.read_excel('Logic_SQL_Test.xlsx',sheet_name='Input data', usecols="A,B", header = 1)
models = df0[0:13]
model_dict = dict(zip(models['Model name'], models['Threshold'].apply(int)))


df1 = pd.read_excel('Logic_SQL_Test.xlsx',sheet_name='Input data', usecols="D:G", header = 1)
rules = df1[0:28]
rules = rules.rename(columns={'Model name.1':'Model Name'})
#list_of_rules['type'] = list_of_rules['Customer type'].apply(lambda x: '_INV' if x == 'Individual' else '_CP')
rules['Full Model Name'] = rules['Model Name'] + rules['Customer type'].apply(lambda x: '_INV' if x == 'Individual' else '_CP')
rules['Threshold'] = rules['Full Model Name'].map(model_dict)
rules = rules[['Full Model Name','Customer type','Rule name','Score','Threshold']]
rules['Hits'] = 0
rules['Alerts'] = 0


df2 = pd.read_excel('Logic_SQL_Test.xlsx',sheet_name='Input data', usecols="I:L", header = 1)
monitor = df2[0:5425]
monitor = monitor.rename(columns={'(No column name)':'Date'})
monitor['Date'] = pd.to_datetime(monitor['Date'])
monitor['day of week'] = monitor['Date'].dt.day_name()
monitor['Week Number'] = monitor['Date'].dt.week
monitor = monitor.rename(columns={'Customer type.1':'Customer type'})

