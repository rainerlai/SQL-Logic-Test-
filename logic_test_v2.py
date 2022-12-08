
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 11:38:55 2022

@author: Rainer
"""

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

#%%
'Grouping of Data'

hits = collections.defaultdict(int)
alerts_model = collections.defaultdict(int)
alerts_customer_id = collections.defaultdict(int)
alerts_customer_type = collections.defaultdict(int)
rule_threshold = collections.defaultdict(int)

model_counter = collections.defaultdict(int)
#model_threshold = collections.defaultdict(int)


def calculate(row):
    
    rule_name = row['Rule_name']
    customer_type = row['Customer type']
    week_num = row['Week Number']
    customer_id = row['Customer ID']
    
    model_name = rules[(rules['Rule name'] == rule_name) & (rules['Customer type'] == customer_type)]['Full Model Name']
    model_threshold = rules[(rules['Rule name'] == rule_name) & (rules['Customer type'] == customer_type)]['Threshold']
    
    score_add = rules[(rules['Rule name'] == rule_name) & (rules['Customer type'] == customer_type)]['Score']
    
    #Calculate Total Hits based on rule_name and customer_type
    hits[rule_name] += 1
    hits[customer_type] += 1
    
    for i in model_name:
        model_threshold = rules[(rules['Full Model Name'] == i)]['Threshold']
        model_counter[i] += score_add
       # if model_counter[i] in model_counter:
       #     if model_counter[i] >= model_threshold:
       #         alerts_model[i,week_num] += 1
            
                                
    
    print(f'rule_name = {rule_name} ,customer_type = {customer_type}, week_num = {week_num}, customer_id = {customer_id}, model_name = {model_name}, model_threshold = {model_threshold}, score = {score_add}')
    print(model_counter)
    #Alerts
    ##rule_threshold[rule_name] += score_add
    ##model_threshold[model_name] += score_add
    
    #if model_threshold[model_name] >= model_threshold:
    #    model_threshold[model_name] = 0
    #    alerts_model[(model_name,week_num)] += 1
    #    alerts_customer_id[customer_id] += 1
    #    alerts_customer_type[customer_type] += 1
        
    

    #hits[model_name] += 1
    
    #return pd.Series([hits[rule_name], hits[model_name]],
    #                 index=['rule name hits', 'model name hits'])

frame = monitor.apply(calculate, axis=1)

#frame = pd.concat([rules, monitor.apply(calculate, axis=1)], axis=1)

set1 = rules[(rules['Rule name'] == 'R01') & (rules['Customer type'] == 'Individual')]['Full Model Name']

for i in set1:
    print (i)

#By Customer Type
#monitor_custype = monitor.groupby('Customer ID').sum()



#rules.loc[rules['Rule name'] == 'R11']


#for index, row in monitoring_hits.iterrows():
#    week_track = 'start'
#    if row['Week_Number'] == 'start':
#        week_track = row['Week_Number']
#        rules.loc[row['Rule_name'],['Hits']] + 1 
        
        
    #elif row['Week Number'] == week_track:
        
        
    
    #print(index, row['Rule_name'])




