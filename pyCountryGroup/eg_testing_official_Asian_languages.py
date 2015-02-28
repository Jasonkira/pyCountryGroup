# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import pyCountryGroup
import pyCountrySize
import pandas as pd

#print pyCountryGroup.wp['Unicode_UN']
#print pyCountryGroup.wp['worldbank']

df_tl=pd.read_csv("territory_language.tsv", sep="\t",encoding='utf8')

def ifAsian(x):
    #print x,
    if isinstance(x, basestring) and  "Asia" in x:
        return True
    else:
        return False

# Categorization
df_tl['un_r']=[pyCountryGroup.un_r_long.get(x,None) for x in df_tl['ISO']]
df_tl['Asian']=[ifAsian(x) for x in df_tl['un_r']]

# Selecting
d=df_tl.copy()


sliced=d[(d.officialStatus=="official") & (d.Asian==True)]
summary_gl=sliced.sort(['IPop'], ascending=[0])[[u'type', u'ISO',u'c_code', u'l_name',u'LP', u'IPop', u'PPPGDP']]#, u'c', u'un_r', u'Asian'
summary_l=summary_gl.groupby(u'type').sum()
summary_l_ranked=summary_l.rank(ascending =False)#.sort("IPop")

for i in summary_l.columns:
    summary_l[i+"_rank"] = summary_l_ranked[i]
    summary_l[i+'_perc_Asia'] = 100*summary_l[i]/summary_l.sum()[i]
    summary_l[i+'_perc_World'] = 100*summary_l[i]/eval("pyCountrySize."+i+".sum()")

dict_languagename=d[['type','l_name']].set_index('type').drop_duplicates()['l_name']
summary_l["Language"]=[dict_languagename[x] for x in summary_l.index]

summary_l.reset_index().sort("IPop_rank").to_csv("ranked_IPop_Asian.tsv", sep="\t", float_format='%4.4f', encoding='utf8',  index_label=False, index=False)

## Not Official as a contrast
sliced=d[(d.officialStatus!="official") & (d.Asian==True)]
summary_gl=sliced.sort(['IPop'], ascending=[0])[[u'type', u'ISO',u'c_code', u'l_name',u'LP', u'IPop', u'PPPGDP']]#, u'c', u'un_r', u'Asian'
summary_l=summary_gl.groupby(u'type').sum()
summary_l_ranked=summary_l.rank(ascending =False)#.sort("IPop")

for i in summary_l.columns:
    summary_l[i+"_rank"] = summary_l_ranked[i]
    summary_l[i+'_perc_Asia'] = 100*summary_l[i]/summary_l.sum()[i]
    summary_l[i+'_perc_World'] = 100*summary_l[i]/eval("pyCountrySize."+i+".sum()")

dict_languagename=d[['type','l_name']].set_index('type').drop_duplicates()['l_name']
summary_l["Language"]=[dict_languagename[x] for x in summary_l.index]

summary_l.reset_index().sort("IPop_rank").to_csv("ranked_IPop_Asian_non_official.tsv", sep="\t", float_format='%4.4f', encoding='utf8',  index_label=False, index=False)



## NOT Asian as a contrast

sliced=d[(d.officialStatus=="official") & (d.Asian==False)]
summary_gl=sliced.sort(['IPop'], ascending=[0])[[u'type', u'ISO',u'c_code', u'l_name',u'LP', u'IPop', u'PPPGDP']]#, u'c', u'un_r', u'Asian'
summary_l=summary_gl.groupby(u'type').sum()
summary_l_ranked=summary_l.rank(ascending =False)#.sort("IPop")

for i in summary_l.columns:
    summary_l[i+"_rank"] = summary_l_ranked[i]
    summary_l[i+'_perc_Asia(Not)'] = 100*summary_l[i]/summary_l.sum()[i]
    summary_l[i+'_perc_World'] = 100*summary_l[i]/eval("pyCountrySize."+i+".sum()")

dict_languagename=d[['type','l_name']].set_index('type').drop_duplicates()['l_name']
summary_l["Language"]=[dict_languagename[x] for x in summary_l.index]

summary_l.reset_index().sort("IPop_rank").to_csv("ranked_IPop_Asian_not.tsv", sep="\t", float_format='%4.4f', encoding='utf8',  index_label=False, index=False)


## Not Official as a contrast
sliced=d[(d.officialStatus!="official") & (d.Asian==False)]
summary_gl=sliced.sort(['IPop'], ascending=[0])[[u'type', u'ISO',u'c_code', u'l_name',u'LP', u'IPop', u'PPPGDP']]#, u'c', u'un_r', u'Asian'
summary_l=summary_gl.groupby(u'type').sum()
summary_l_ranked=summary_l.rank(ascending =False)#.sort("IPop")

for i in summary_l.columns:
    summary_l[i+"_rank"] = summary_l_ranked[i]
    summary_l[i+'_perc_Asia(Not)'] = 100*summary_l[i]/summary_l.sum()[i]
    summary_l[i+'_perc_World'] = 100*summary_l[i]/eval("pyCountrySize."+i+".sum()")

dict_languagename=d[['type','l_name']].set_index('type').drop_duplicates()['l_name']
summary_l["Language"]=[dict_languagename[x] for x in summary_l.index]

summary_l.reset_index().sort("IPop_rank").to_csv("ranked_IPop_Asian_not_non_official.tsv", sep="\t", float_format='%4.4f', encoding='utf8',  index_label=False, index=False)
