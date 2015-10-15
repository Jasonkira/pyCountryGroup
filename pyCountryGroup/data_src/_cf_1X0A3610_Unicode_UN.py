# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import pandas as pd
df=dict()
df['beltway']= pd.read_csv('1X0A36I0.tsv', sep='\t', encoding="utf8")
df['cldr']= pd.read_csv('Unicode_UN.tsv', sep='\t', encoding="utf8")
file_output = '1X0A36I0_beltway_coded.tsv'

dict_numeric_alpha3 = df['cldr'][['numeric', 'countrycode']].set_index('numeric')['countrycode'].to_dict()
dict_numeric_alpha2 = df['cldr'][['numeric', 'countrycode2']].set_index('numeric')['countrycode2'].to_dict()
dict_alpha3_alpha2 = df['cldr'][['countrycode', 'countrycode2']].set_index('countrycode')['countrycode2'].to_dict()
dict_numeric_name = df['cldr'][['numeric', 'countryname']].set_index('numeric')['countryname'].to_dict()
dict_name_numeric = df['cldr'][['countryname', 'numeric']].set_index('countryname')['numeric'].to_dict()
dict_name_alpha3 = df['cldr'][['countryname', 'countrycode']].set_index('countryname')['countrycode'].to_dict()

import difflib

alpha3=[]
for x in df['beltway']['country_name'].values:
    if x in dict_name_alpha3.keys():
        ccode=dict_name_alpha3.get(x)
        print (ccode, end='\t')
        alpha3.append(ccode)
    else:
        print ('\nPerfect match failed for '+x)
        xx = difflib.get_close_matches(x,dict_name_alpha3.keys())
        print ('...{}'.format([i for i in xx]))
        print ('...{}'.format([dict_name_alpha3.get(i) for i in xx]))
        corrected = input("...Please enter the corrected alpha3 country code:")
        alpha3.append(corrected)

df['beltway']['countrycode2'] = alpha3
df['beltway']['countrycode'] = [dict_alpha3_alpha2.get(x,'') for x in alpha3]
df['beltway'][['countrycode', 'countrycode2', 'country_name', 'url_profile']].to_csv(file_output, sep='\t', encoding="utf8", index=False)

print (">> output to {}".format(file_output))
