# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import pyCountryGroup

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

pyCountryGroup.wp.loc[usual_suspects.keys()]
