# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import pandas as pd
df=dict()
df['m49']= pd.read_csv('m49regin_country.tsv', sep='\t', encoding="utf8")
df['cldr']= pd.read_csv('Unicode_UN.tsv', sep='\t', encoding="utf8")

df['m49']['numeric'] = df['m49']['numeric'] .astype(int)

print (df['cldr'][df['cldr']['numeric'].isnull()])              # missing numeric codes
df['cldr']=df['cldr'][df['cldr']['numeric'].notnull()]     # removing missing values for integer conversion

df['cldr']['numeric'] = df['cldr']['numeric'] .astype(int)

df['_join']=pd.merge(df['m49'], df['cldr'], on='numeric')

def set_compare(x, y):
    set_x = set (x)
    set_y = set (y)
    set_inter = set_x.intersection(set_y)
    set_diffxy = set_x.difference(set_y)
    set_diffyx = set_y.difference(set_x)
   
    return [set_inter, set_diffxy, set_diffyx]

cf = set_compare(df['m49']['numeric'], df['cldr']['numeric'])
#print (cf)
cf_outcomes = [sorted(list(x)) for x in cf]
print (cf_outcomes)
print ([len(x) for x in cf])


dict_numeric_alpha3 = df['cldr'][['numeric', 'countrycode']].set_index('numeric')['countrycode'].to_dict()
dict_numeric_alpha2 = df['cldr'][['numeric', 'countrycode2']].set_index('numeric')['countrycode2'].to_dict()
dict_numeric_name = df['cldr'][['numeric', 'countryname']].set_index('numeric')['countryname'].to_dict()
print ([dict_numeric_alpha3[x] for x in [y for y in cf_outcomes]])
print ([dict_numeric_alpha2[x] for x in cf_outcomes])
print ([dict_numeric_name[x] for x in cf_outcomes])


'''
df_mapping=df['countryname']
df_mapping=df_mapping.reset_index().drop_duplicates(subset='numeric', take_last=False).set_index('numeric')

#df[df.category==df.index]
df=df[df.region!=df.index]

df_country=df[df.economic==False]
df_country.to_csv('m49regin_country.csv', sep='\t', encoding="utf8")

df_cat = df[df.economic==False].groupby(by="region")

df_cat = df_cat.count()['countryname']
df_cat = df_cat[df_cat>1].to_frame()
df_cat.columns=["count"]

df_cat['r_long_d']=[df_mapping['countryname'][x] for x in df_cat.index]

df_cat.sort('r_long_d')

df[df.region=='015']
df[df.region=='029']
df[df.index=='659']
'''
