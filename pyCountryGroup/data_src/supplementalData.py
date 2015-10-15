# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
URL_source = u'http://unicode.org/repos/cldr/trunk/common/supplemental/supplementalData.xml'
encoding_source = "utf-8"

import os
URL_path, downloaded_source = os.path.split(URL_source)
file_output = downloaded_source.split(os.extsep)[0]+".tsv"

## Definitions of variables and their xpaths ##


## Using requests to download and lxml to parse
from lxml.html import fromstring, tostring, parse, etree
from io import StringIO, BytesIO

try:
    tree = etree.parse(downloaded_source) #etree.parse was used to parse xml
except:
    XML_encoding=encoding_source
    XML_src_url=URL_source

    import requests
    r = requests.get(XML_src_url, stream=True)
    r.raw.decode_content = True

    if not(r.status_code == 200):
        print ("Downloading the data from {} failed. Plese check Internet connections.".format(XML_src_url))
        exit()

    XML_src=r.content# r.raw.read()#r.raw#r.text
    print (r.encoding)
    #XML_encoding=r.encoding     #'ISO-8859-1'
    print (encoding_source)

    import codecs
    with codecs.open(downloaded_source, "w", XML_encoding) as file:
        file.write(XML_src.decode(XML_encoding))
        
    tree = fromstring(XML_src)  



import pandas as pd
import numpy as np

def parse_generic(_xpath, _com):
    list_matched = tree.xpath(_xpath)
    list_processed=[]
    for i,t in enumerate(list_matched):
        data_dict=dict(zip(t.keys(),t.values()))
        if _com=="getnext":
            data_dict['comments'] = t.getnext().text.strip() #unicode(t.getnext().text.strip())
        else:
            if _com=="getchildren":
                data_dict['comments'] = t.getchildren()[0].text.strip() #unicode(t.getchildren()[0].text.strip())
        #debug
        if i==0:
            print ("Debug:{}".format(data_dict))
        list_processed.append(data_dict)
    df__=pd.DataFrame(list_processed)
    return df__

## To get data:  c_name gdp literacyPercent population
df_basic = parse_generic('//territoryInfo/territory',"getchildren" ).set_index('type')
#print df_basic['comments']['AX']
#print df_basic['comments']['TW']
print (len(df_basic))

## To get data: UN categorization
df_containment_UN= parse_generic('//territoryContainment/group[not(@grouping="true")]', "getnext")

categorization_UN=dict()
map_left=[x.split(" ") for x in list(df_containment_UN.contains)]
map_right=list(df_containment_UN.comments.replace("Southern Europe, XK not in UN data","Southern Europe") ) #.type
map_right_type=list(df_containment_UN.type) #.type
for i,left in enumerate(map_left):
    for item_left in left:
        if pd.isnull(map_right_type[i]) or pd.isnull(map_right[i]):
            categorization_UN[item_left]={"code":map_right_type[i] , "cat": map_right[i] }
        else:
            categorization_UN[item_left]={"code":map_right_type[i] , "cat": map_right[i] }
        
#print categorization_UN['TW']
df_cat_UN=pd.DataFrame(categorization_UN).transpose()
print (len(df_cat_UN))


## To get data: Code mapping
df_mapping=parse_generic('//codeMappings/territoryCodes',"" )
df_mapping23=df_mapping.set_index('type')['alpha3']
df_mapping32=df_mapping.set_index('alpha3')['type']
df_mappingn2=df_mapping.set_index('numeric')['type']
df_mappingn2=df_mapping.set_index('numeric')['type']
df_mapping2n=df_mapping.set_index('type')['numeric']
df_mapping3n=df_mapping.set_index('alpha3')['numeric']

## Constructing working integrated dataframe
df=df_basic.copy()
df['alpha3']=[df_mapping23[x] for x in df.index]
df['numeric']=[df_mapping2n[x] for x in df.index]
df['cat_UN']=[df_cat_UN["code"].get(x, np.nan) for x in df.index]
df['categorization_UN']=[df_cat_UN["cat"].get(x, np.nan) for x in df.index]

df=df.reset_index()


## UN higher category just under the World
under_the_World_UN=df_cat_UN[df_cat_UN.cat=="World"].index
df_cat_UN[df_cat_UN.code.isin(under_the_World_UN)].index

##>>> list(df.columns)
##['typ2','comments', 'gdp', 'literacyPercent', 'population', 'alpha3', 'numeric', 'cat_UN', 'categorization_UN']
df.columns=['countrycode2','countryname', 'gdp', 'literacyPercent', 'population', 'countrycode', 'numeric', 'region', 'r_long_d']


## Dealing with those without ISO alpha_3 http://www.fact-index.com/i/is/iso_3166_1_alpha_2.html
##>>> df[pd.isnull(df.countrycode)]
##    countrycode2      countryname          gdp literacyPercent population  \
##65            EA  Ceuta & Melilla   4364000000            97.7     150000   
##104           IC   Canary Islands  61060000000            97.7    2098590 
df.loc[pd.isnull(df.countrycode),'countrycode']="_"+df[pd.isnull(df.countrycode)]['countrycode2']


##
fileds_selected_categories=['countrycode', 'countryname', 'countrycode2', 'numeric', 'region', 'r_long', 'r_long_d']

df['r_long']=[df_cat_UN[df_cat_UN.code.isin(under_the_World_UN)]['cat'].get(x, None) for x in df['region'] ]

df=df[fileds_selected_categories].set_index("countrycode")

df.to_pickle('Unicode_UN.pkl')
df.to_csv('Unicode_UN.tsv', sep='\t', encoding="utf8")

#print df["countryname"]["ALA"]
df_cat = df.groupby(by="r_long_d")
df_cat = df_cat.count()['region']


#df[df.r_long_d=='Northern Africa']
