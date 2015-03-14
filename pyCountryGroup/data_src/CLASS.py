# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import os.path
import pandas as pd
import numpy as np

## Loading the XLS source file
sheets={"le":"List of economies",\
        "grps":"Groups",\
        }
#        "d":"Data"}
ddf=dict()
for k in sheets.keys():
    df = pd.io.excel.read_excel("CLASS.XLS", \
                                na_values=["NaN",""], sheetname=sheets[k],\
                                keep_default_na=False)
    ddf[k]=df
    

## "le":"List of economies"  rename column names

ddf['le'].columns=list(ddf['le'].loc[3:3].values)
df=ddf['le'].loc[5:,:].dropna(axis=1,how="all").copy()
df.columns=[str(x).lower().replace(" ","_")  for x in list(df.columns)]

mapping_name2code=dict(zip(df.economy.values,df.code.values))
#mapping_name2code['Lithuania']    LTU


##
#an error in the original file  Lithuania should be 	LTU
#LVA	Latvia
#LVA	Lithuania

#>>> ddf['grps'].columns
#Index([u'GroupCode', u'GroupName', u'CountryCode', u'CountryName'], dtype='object')
ddf['grps'].columns=[x.lower().replace(" ","_")  for x in list(ddf['grps'].columns)]
#Index([u'groupcode', u'groupname', u'countrycode', u'countryname'], dtype='object')
df_grps=ddf['grps'].copy().drop_duplicates()
df.columns=[str(x).lower().replace(" ","_")  for x in list(df.columns)]

list_categories=[u'region', u'income_group', u'lending_category', u'other']

df_grps['code']=[mapping_name2code.get(x, np.nan) for x in df_grps.countryname.values]

## Listing the problematic entries
print df_grps.loc[df_grps['code']!=df_grps['countrycode']][['code','countrycode']].drop_duplicates()

##>>> df_grps.loc[df_grps['code']!=df_grps['countrycode']][['code','countrycode']].drop_duplicates()
##    code countrycode
##100  NaN         TWN
##118  LTU         LVA----> should be LTU
##239  NaN         CIV
##295  NaN         STP
##320  NaN         CUW
list_to_correct=df_grps.loc[(df_grps['code']!=df_grps['countrycode']) & (df_grps['countrycode']=="LVA")].index
for i in list_to_correct:
    df_grps.loc[i]['countrycode']=u"LTU"
df_grps.drop('code', axis=1, inplace=True)


## TEST
print df_grps.loc[(df_grps['countrycode']=="TWN")]

## Summary
grouped=df_grps.groupby(by="groupcode", axis=0, sort=True)
print grouped.count()
grouped.get_group('EAS')

## Construciting a new one
df=pd.DataFrame(df_grps.groupby(['countrycode']).first()[u'countryname'].copy())

df_mapping = df_grps.groupby(['groupcode']).first()[u'groupname'].reset_index()
mapping_group2groupname=dict(zip(df_mapping.groupcode.values,df_mapping.groupname.values))
mapping_groupname2group=dict(zip(df_mapping.groupname.values,df_mapping.groupcode.values))

# five regions (all income levels) + 2 regions North America and South Asia
         
list_cat=[x for x in mapping_group2groupname.keys() if \
          ("(all income levels)" in mapping_group2groupname[x]) or\
          (mapping_group2groupname[x]=="North America") or\
          (mapping_group2groupname[x]=="South Asia") 
          ]

dict_w=dict()                             
for cat in list_cat:
    for l in list(grouped.get_group(cat).countrycode):
        dict_w[l]=cat
                             
df["region"]=[dict_w.get(x,np.nan) for x in df.index]
#測試漏掉的
df[pd.isnull(df.region)]
print len(dict_w)


# add long description
df["r_long"]=[mapping_group2groupname[x] for x in df["region"]]


list_cat=[u'LIC', u'LMC', u'UMC', u'LMY', u'NOC', u'OEC']  #u'HIC', MIC

dict_w=dict()                             
for cat in list_cat:
    for l in list(grouped.get_group(cat).countrycode):
        dict_w[l]=cat
        
df["incomelevel"]=[dict_w.get(x,np.nan) for x in df.index]
#測試漏掉的
df[pd.isnull(df.incomelevel)]
print len(dict_w)


# add long description
df["i_long"]=[mapping_group2groupname[x] for x in df["incomelevel"]]


##print df.loc['HKG',:]
##countryname    Hong Kong SAR, China
##region                          EAS
##incomelevel                     NOC
##r_long         East Asia & Pacific (all income levels)
##i_long                            High income: nonOECD
##Name: HKG, dtype: object


## Removing labels " (all income levels)"
df["r_long"]=[x.replace("(all income levels)","").strip() for x in df["r_long"]]

## Exporting to pkl
df.to_pickle("worldbank.pkl")

## Testing with the number of countries in the same region where Hong Kong is
list_target=list(df[df.region==df['region']['HKG']].countryname)
print "There are {0} countries in the region of {1} or {2} ".format(len(list_target),df['region']['HKG'],df['r_long']['HKG'])
# There are 37 countries in the region of EAS or East Asia & Pacific

# Note. Taiwan is added back by including the second spreadsheet where grouping informaiton for Taiwan is provided
