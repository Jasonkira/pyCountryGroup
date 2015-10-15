# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
URL_source = u'http://china-trade-research.hktdc.com/business-news/article/One-Belt-One-Road/The-Belt-and-Road-Initiative-Country-Profiles/obor/en/1/1X000000/1X0A36I0.htm'
encoding_source = "utf-8"

import os
URL_path, downloaded_source = os.path.split(URL_source)
file_output = downloaded_source.split(os.extsep)[0]+".tsv"

## Definitions of variables and their xpaths ##
list_xpaths = [ '''//*[@id="article-content"]/wiser_content/div/div/div/div/figure/a/img/@title''',
                '''//*[@id="article-content"]/wiser_content/div/div/div/div/figure/a/@href''',
              ]

list_variable_names = [
                '''country_name''',
                '''url_profile''',
              ]


## Using requests to download and lxml to parse
from lxml.html import fromstring, tostring, parse
from io import StringIO, BytesIO


try:
    tree = parse(downloaded_source)
except:
    XML_encoding=encoding_source
    XML_src_url = URL_source
    import requests
    r = requests.get(XML_src_url, stream=True)
    r.raw.decode_content = True

    if not( r.status_code == 200):
        print ("Downloading the data from {0} failed. Plese check Internet connections.".format(XML_src_url))
        exit()

    XML_src=r.content # r.raw.read()#r.raw#r.text
    #XML_encoding=r.encoding
    print(XML_encoding)

    import codecs
    with codecs.open(downloaded_source, "w", XML_encoding) as file:
        file.write(XML_src.decode(XML_encoding))

        
    tree = fromstring(XML_src)

data=[]
for i,_xpath in enumerate(list_xpaths):
    data.append(tree.xpath(list_xpaths[i])) 


import pandas as pd
import numpy as np


df = pd.DataFrame(data)
df = df.T  ## transpose 
df.columns=list_variable_names


## Cleaning data ##
df['country_name']
df_cleaned = df.assign(country_name=[x.replace("Picture: ","") for x in df.country_name])
df = df_cleaned[list_variable_names]

## Exporting to csv ##
df.to_csv(file_output, sep='\t', encoding="utf8", index=False)

