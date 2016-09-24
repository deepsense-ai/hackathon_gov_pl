
# coding: utf-8

# In[ ]:

from lxml import etree
from itertools import islice
from sys import argv


# In[ ]:

with open(argv[1] + '.parsed', 'w') as outF:
    with open(argv[1]) as inF:
        for l in inF:
            try:
                ziom = etree.fromstring(l)
            except etree.XMLSyntaxError:
                continue
            a1 = ziom.find('DaneAdresowe').find('AdresGlownegoMiejscaWykonywaniaDzialalnosci').find('KodPocztowy').text
            a2 = ziom.find('DaneDodatkowe').find('DataRozpoczeciaWykonywaniaDzialalnosciGospodarczej').text
            a3 = ziom.find('DaneDodatkowe').find('KodyPKD').text
            outF.write(str(a1) + ',' + str(a2) + ',' + str(a3) + '\n')


# In[ ]:



