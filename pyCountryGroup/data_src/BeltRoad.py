# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import pandas as pd
import logging

df=dict()
df['BeltRoad_'] =pd.read_csv('1X0A36I0_BeltRoad_coded.tsv', sep='\t' , encoding="utf8" )#, na_values="-", keep_default_na=False
df['cldr'] = pd.read_csv('Unicode_UN.tsv', sep='\t', encoding="utf8")
file_output = 'BeltRoad.tsv'

df['BeltRoad'] = df['cldr'].copy()


def ifinBeltRoad(x):
    if x in df['BeltRoad_'].countrycode.values:
        return True
    else:
        return False

df['BeltRoad']['inBeltRoad'] = [ifinBeltRoad(c) for c in df['BeltRoad'].countrycode]

dict_url=df['BeltRoad_'][["countrycode","url_profile"]].set_index(["countrycode"])["url_profile"].to_dict()

df['BeltRoad']['inBeltRoad_url'] = [dict_url.get(c,None) for c in df['BeltRoad'].countrycode]

df_out=df['BeltRoad']

df_out=df_out.set_index(["countrycode"])
# df_out[df_out.inBeltRoad==True]

df_out.to_csv(file_output, sep='\t', encoding="utf8")
file_output = file_output.replace (".tsv",".pkl")
df_out.to_pickle(file_output)


