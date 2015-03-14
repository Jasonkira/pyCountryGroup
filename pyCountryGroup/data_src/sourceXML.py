# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from lxml import etree
from io import StringIO, BytesIO

tree=etree.parse("sourceXML.xml")


import pandas as pd
import numpy as np

def parse_generic(_xpath, _com):
    list_matched = tree.xpath(_xpath)
    list_processed=[]
    for i,t in enumerate(list_matched):
        data_dict=dict(zip(t.keys(),t.values()))
        if _com=="getnext":
            data_dict['comments']=unicode(t.getnext().text.strip())
        else:
            if _com=="getchildren":
                data_dict['comments']=unicode(t.getchildren()[0].text.strip())
        #debug
        if i==0:
            print "Debug:",data_dict
        list_processed.append(data_dict)
    df__=pd.DataFrame(list_processed)
    return df__

## To get data:  c_name gdp literacyPercent population
df = parse_generic('//country/country',"nothing" )
#print df_basic['comments']['AX']
#print df_basic['comments']['TW']
print len(df)

df_d=pd.read_csv('CIA_appendix-d.csv', sep='\t' , encoding="utf8" )#, na_values="-", keep_default_na=False

df_i=df_d[df_d.GEC!="-"].copy()
    
d=dict(zip(df.fips,df.Region))


df_i["r_long"]=[d.get(x, None) for x in df_i.GEC]
#set(df_i.r_long)
#set(['Europe', 'Oceania', 'East Asia', 'Central America', 'Africa', 'South America',\
#None, 'North America', 'Antarctica', 'Middle East', 'Central Asia', 'South Asia'])

# eur https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_eur.html
# aus https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_aus.html
# eas https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_eas.html
# cam https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_cam.html
# afr https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_afr.html
# soa https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_soa.html
# noa https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_noa.html
# ant https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_ant.html
# mde https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_mde.html
# cas https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_cas.html
# sas https://www.cia.gov/library/publications/the-world-factbook/wfbExt/region_sas.html

d_rev={'Europe':"eur", 'Oceania':"aus", 'East Asia':"eas", 'Central America':"cam",\
       'Africa':"afr", 'South America':"soa", 'North America':"noa", 'Antarctica':"ant",\
       'Middle East':"mde", 'Central Asia':"cas", 'South Asia':"sas"}

df_i["region"]=[d_rev.get(x, None) for x in df_i.r_long]
df_i= df_i[df_i['ISO2']!="-"]
df_i= df_i[pd.notnull(df_i['ISO'])]
df_output=df_i[['ISO','r_long',"region"]].copy()
df_output.columns=['countrycode','r_long',"region"]
# Remove duplicate index PSE
df_output=df_output.drop_duplicates()

df_output=df_output[df_output.countrycode!=None]

df_output=df_output.set_index("countrycode")


df_output.to_pickle('CIA.pkl')
