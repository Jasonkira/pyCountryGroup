# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from lxml.html import fromstring, tostring, parse
from io import StringIO, BytesIO

XML_encoding="ISO-8859-1"

try:
    tree = parse("m49regin.html")
except:
    XML_src_url=u'http://unstats.un.org/unsd/methods/m49/m49regin.htm'

    import requests
    r = requests.get(XML_src_url, stream=True)
    r.raw.decode_content = True

    if not( r.status_code == 200):
        print ("Downloading the data from {0} failed. Plese check Internet connections.".format(XML_src_url))
        exit()

    ##Requests will automatica冖lly decode content from the server [as r.text]. ... You can also access the response body as bytes [as r.content].
    XML_src=r.content# r.raw.read()#r.raw#r.text
    print(XML_encoding)

    import codecs
    with codecs.open("m49regin.html", "w", XML_encoding) as file:
        file.write(XML_src.decode(XML_encoding))

    #from lxml.html.clean import clean_html
    #XML_src = clean_html(XML_src)

    XML_src = str(XML_src).replace("Saint-Barth&eacute;lemy</p></td>\r\n        </tr>","Saint-Barth&eacute;lemy</p></td>\r\n        </tr><tr>")


    #from BeautifulSoup import BeautifulSoup

    #soup = BeautifulSoup(XML_src)
    #tree = soup.prettify()

    #import xml.etree.ElementTree as ET
    #tree = ET.fromstring(XML_src)

        
    tree = fromstring(XML_src)



import pandas as pd
import numpy as np

def parse_UN_m49region(_xpath):
    return df__

## To get data:  UN m49
_xpath='''//*/table[2]/tbody/tr/td[3]/table[4]/tbody/tr'''

_xpath='''//*/table[2]//*/td[3]/table[4]//tr'''




list_matched = tree.xpath(_xpath)
list_processed=[]
category_current=""
flag_economic_regions = False

for i,t in enumerate(list_matched):
    sel=list_matched[i].findall
    item_code = list_matched[i].findall("td")[0].text_content().strip()
    item_content = list_matched[i].findall("td")[1].text_content().strip().split('\r\n')[0].strip()

    try:
        category_or_not=len(list(list_matched[i].findall("td")[1].iterfind(".//b")))
        #print (category_or_not)
    except:
        category_or_not=False

    if category_or_not:
        category_current = item_code


    if item_content=="Developing regions":
        category_current = "developing"
    
    if item_content=="Developed regions":
        category_current = "developed"
        

    if "excluding" in item_content:
        flag_excluding=True
    else:
        flag_excluding=False

    if item_content=="Developed and developing regions c/":
        flag_economic_regions=True



    item_content = item_content.replace("  "," ")  #China,  Hong Kong Special Administrative Region

    row = (item_code, item_content, category_current, flag_economic_regions, flag_excluding)

    #print ("{},".format((i,item_code)), end='\t')
    if item_code=='659':
        print(row)
    #print (row)

    if item_code=='' and item_content=='':
        pass
    else:
        list_processed.append(row)
    '''
    list_processed.append(row)
    '''




df__=pd.DataFrame(list_processed)
df__.columns=["numeric", "countryname", "region", "economic", "excluding"]

df = df__[1:].set_index("numeric")


#df = parse_UN_m49region('////*//table[2]//tbody//tr//td[3]//table[4]//tbody//tr')


#print df_basic['comments']['AX']
#print df_basic['comments']['TW']
print (len(df))

df.to_csv('m49regin.tsv', sep='\t', encoding="utf8")

df_mapping=df['countryname']
df_mapping=df_mapping.reset_index().drop_duplicates(subset='numeric', take_last=False).set_index('numeric')

#df[df.category==df.index]
df=df[df.region!=df.index]

df_country=df[df.economic==False]
df_country.to_csv('m49regin_country.tsv', sep='\t', encoding="utf8")

df_cat = df[df.economic==False].groupby(by="region")

df_cat = df_cat.count()['countryname']
df_cat = df_cat[df_cat>1].to_frame()
df_cat.columns=["count"]

df_cat['r_long_d']=[df_mapping['countryname'][x] for x in df_cat.index]

df_cat.sort('r_long_d')

df[df.region=='015']
df[df.region=='029']
df[df.index=='659']
