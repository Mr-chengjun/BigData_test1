# -*- coding: utf-8 -*-

"""

    版本:     1.0
    日期:     2018/10
    文件名:    config.py
    功能：     配置文件

"""
import os

#指定数据集路径
dataset_path = '../data_folder/kongqi_data'

#结果保存路径
output_path = '../data_folder/output_folder'
if not os.path.exists(output_path):
    os.makedirs(output_path)

#公共列
common_cols = ['year','month']

# 每个城市对应的文件名及所需分析的列名
# 以字典形式保存，如：{城市：(文件名, 列名)}
data_config_dict = {'beijing': ('BeijingPM20100101_20151231.csv',
                                ['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan','PM_US Post']),
                    'chengdu': ('ChengduPM20100101_20151231.csv',
                                ['PM_Caotangsi', 'PM_Shahepu','PM_US Post']),
                    'guangzhou': ('GuangzhouPM20100101_20151231.csv',
                                  ['PM_City Station', 'PM_5th Middle School','PM_US Post']),
                    'shanghai': ('ShanghaiPM20100101_20151231.csv',
                                 ['PM_Jingan', 'PM_Xuhui','PM_US Post']),
                    'shenyang': ('ShenyangPM20100101_20151231.csv',
                                 ['PM_Taiyuanjie', 'PM_Xiaoheyan','PM_US Post'])
                    }
