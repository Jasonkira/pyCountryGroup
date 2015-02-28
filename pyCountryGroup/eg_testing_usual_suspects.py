# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import pyCountryGroup
import pandas as pd

# A list of countries that are often missing from the major datasets
usual_suspects={"PSE": "Palestinian Territories",\
                "TWN": "TAIWAN",\
                "SSD": "South Sudan",\
                #http://www.iso.org/iso/home/news_index/news_archive/news.htm?refid=Ref1456
                "XKS": "Kosovo",\
                #https://www.cia.gov/library/publications/the-world-factbook/appendix/appendix-d.html
                }
usual_suspects_less={"MAC": "Macau SAR China",\
                "HKG": "Hong Kong SAR China",\
                }

print pyCountryGroup.wp['Unicode_UN'].loc[usual_suspects.keys()]
print pyCountryGroup.wp['worldbank'].loc[usual_suspects.keys()]

## Amend the missing data
#>>> pyCountryGroup.wp['Unicode_UN']['countryname']['ISR']
#u'Israel'
Serbia_un=pyCountryGroup.wp['Unicode_UN'][pyCountryGroup.wp['Unicode_UN']['countryname']=="Serbia"][['r_long','region']]
Israel=pyCountryGroup.wp['worldbank'][pyCountryGroup.wp['worldbank']['countryname']==u'Israel'][['r_long','region']]
Serbia_wb=pyCountryGroup.wp['worldbank'][pyCountryGroup.wp['worldbank']['countryname']=="Serbia"][['r_long','region']]

amend_un={"XKS":{"countrycode2":"XK",\
              "countryname":"Kosovo",\
              "region":Serbia_un['region'].values[0],
              "r_long":Serbia_un['r_long'].values[0],
              }\
       }
amend_wb={"PSE":{\
              "countryname":"Palestinian Territories",\
              "region":Israel['region'].values[0],
              "r_long":Israel['r_long'].values[0],
              },\
          "XKS":{\
              "countryname":"Kosovo",\
              "region":Serbia_wb['region'].values[0],
              "r_long":Serbia_wb['r_long'].values[0],
              },\
       }
amend={'Unicode_UN':amend_un,'worldbank':amend_wb}

ddf=dict()
for cur in amend.keys():
    df=pyCountryGroup.wp[cur]
    print "before",len(df)
    df_amend=pd.DataFrame(amend[cur]).transpose()
    df=df.append(df_amend)
    df=df.drop_duplicates(take_last=True)
    print "after",len(df)
    ddf[cur]=df

pyCountryGroup.wp=pd.Panel(ddf)

#Now fixed...

print pyCountryGroup.wp['Unicode_UN'].loc[usual_suspects.keys()]
print pyCountryGroup.wp['worldbank'].loc[usual_suspects.keys()]

exit()
#for a in amend.keys():
#    for attrib in amend[a].keys():
    #pyCountryGroup.wp[cur][attrib][a]
