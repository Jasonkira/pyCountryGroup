# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas as pd
import os

__all__ = ["iso","iso2","ison","wb_cname","un_cname",\
           "wb_r_long","un_r_long", "un_r_long_detail", "wb_region", "un_region",\
           "wb_i_long","wb_incomelevel","beltroad","beltroad_region","meta","wp"]
__all__ = [str(u) for u in __all__]
_ROOT = os.path.abspath(os.path.dirname(__file__))


from os.path import basename, join, splitext
wp=pd.read_pickle(os.path.join(_ROOT, "cat.pkl"))

iso=wp['Unicode_UN'].index
iso2=wp['Unicode_UN']['countrycode2']
ison=wp['Unicode_UN']['numeric']

wb_cname=wp['worldbank']['countryname']
un_cname=wp['Unicode_UN']['countryname']

wb_r_long=wp['worldbank']['r_long']
un_r_long=wp['Unicode_UN']['r_long']      #UN region just under the world
un_r_long_detail=wp['Unicode_UN']['r_long_d']
cia_r_long=wp['CIA']['r_long']
wb_region=wp['worldbank']['region']
un_region=wp['Unicode_UN']['region']
cia_region=wp['CIA']['region']

wb_i_long=wp['worldbank']['i_long']
wb_incomelevel=wp['worldbank']['incomelevel']

beltroad = wp["BeltRoad"]["inBeltRoad"]
beltroad_region = wp["BeltRoad"]["inBeltRoad_region"]

meta={'iso': "Country Code (ISO 3166-1 alpha-3)",\
      'iso2': "Country Code (ISO 3166-1 alpha-2)",\
      'ison': "Country Code (ISO 3166-1 numeric-3)",\
      'wb_cname': "Country Name (World Bank)",\
      'un_cname': "Country Name (Unicode)",\
      'wb_r_long': "Geographic Categorization (World Bank)",\
      'un_r_long': "Geographic Categorization (Unicode)",\
      'wb_region': "Geographic Categorization Code (World Bank)",\
      'un_region': "Geographic Categorization Code (UN)",\
      'wb_i_long': "Income Level (World Bank)", \
      'wb_incomelevel': "Income Level Code (World Bank)", \
      'beltroad': "Part of China’s Belt and Road Initiative (HKTDC)", \
      'beltroad_region': "Regions of China’s Belt and Road Initiative (HKTDC)", \
      }

