# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

import os.path, glob

import pandas as pd
import numpy as np

filename_list=[os.path.normpath(x) for x in glob.glob(os.path.join(dir_source, "*."+fn_suffix))]
#['data_src\\Unicode_UN.pkl', 'data_src\\worldbank.pkl']

data=dict()
for i,f in enumerate(filename_list):
#    if i==0:
        df = pd.read_pickle(f)
        data[os.path.splitext(os.path.split(f)[1])[0]]=df
#    else:

## Constructing panel
wp=pd.Panel(data)
##>>> wp.items

dir_db = Config.get("Directory",'outcome')
fn_db = Config.get("output",'filename')
wp.to_pickle(os.path.join(dir_db, fn_db))

for i in wp.items:
    wp[i].index.names=df.index.names
    wp[i].to_csv(".".join([i,'tsv']),sep="\t", encoding="utf8")

##>>> wp.items
##Index([u'Unicode_UN', u'worldbank'], dtype='object')
##>>> wp['worldbank']['r_long']['TWN']
##u'East Asia & Pacific (all income levels)'
##>>> wp['worldbank']['region']['TWN']
##u'EAS'
##>>> wp['Unicode_UN']['r_long']['TWN']
##u'Eastern Asia'
##>>> wp['Unicode_UN']['region']['TWN']
##u'030'
