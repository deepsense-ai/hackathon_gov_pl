
# coding: utf-8

# In[29]:

from lxml import etree
from itertools import islice
from sys import argv#YOLO


# In[43]:

with open(argv[1] + '.parsed', 'w') as outF:
    with open(argv[1]) as inF:
        for l in inF:
            try:
                ziom = etree.fromstring(l)
            except etree.XMLSyntaxError:
                continue
            a1=    ziom.find('DaneAdresowe').find('AdresGlownegoMiejscaWykonywaniaDzialalnosci').find('KodPocztowy').text
            a2=    ziom.find('DaneDodatkowe').find('DataRozpoczeciaWykonywaniaDzialalnosciGospodarczej').text
            a3=   ziom.find('DaneDodatkowe').find('KodyPKD').text
            outF.write(a1 + ',' + a2 + ',' + a3 + '\n')

