# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from lxml.html import fromstring, tostring, parse
from io import StringIO, BytesIO

XML_encoding="utf-8"

try:
    tree = parse("appendix-d.html")
except:
    XML_src_url=u'https://www.cia.gov/library/publications/the-world-factbook/appendix/appendix-d.html'

    import requests
    r = requests.get(XML_src_url, stream=True)
    r.raw.decode_content = True

    if not( r.status_code == 200):
        print ("Downloading the data from {0} failed. Plese check Internet connections.".format(XML_src_url))
        exit()

    ##Requests will automatically decode content from the server [as r.text]. ... You can also access the response body as bytes [as r.content].
    XML_src=r.content# r.raw.read()#r.raw#r.text
    #XML_encoding=r.encoding  #'ISO-8859-1'

    import codecs
    with codecs.open("appendix-d.html", "w", XML_encoding) as file:
        file.write(XML_src.decode(XML_encoding))
        
    tree = fromstring(XML_src)




import pandas as pd
import numpy as np

def parse_CIA_appendix(_xpath, _com):
    list_matched = tree.xpath(_xpath)
    list_processed=[]
    for i,t in enumerate(list_matched):
        sel=list_matched[i].cssselect(".category_data")
        list_content=[x.text_content().strip() for x in sel]
        middle3=list(filter(bool,list_content[2].replace("\r","").replace("\n","").split("\t")))
        
        middle3=middle3+[""]*(3-len(middle3))
        
        row=list_content[0:2]+middle3+list_content[3:]
        row=row+[""]*(8-len(row))
        list_processed.append(row)
    df__=pd.DataFrame(list_processed)
    df__.columns=["name","GEC", "ISO2", "ISO", "ISOn", "STANAG", "INTERNET","COMMENT"]
    return df__

## To get data:  CIA appendix
df = parse_CIA_appendix('////*[@id="GetAppendix_D"]//*/tr[td[@class="category_data"]]',"getchildren" )
#print df_basic['comments']['AX']
#print df_basic['comments']['TW']
print (len(df))


#df.to_pickle('CIA.pkl')
df.to_csv('CIA_appendix-d.tsv', sep='\t', encoding="utf8")
