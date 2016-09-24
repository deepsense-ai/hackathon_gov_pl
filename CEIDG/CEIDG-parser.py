
# coding: utf-8

# In[8]:

from lxml import etree
from itertools import islice
from sys import argv
from trans import trans


# In[14]:

skipped = 0
with open(argv[1] + '.parsed', 'w') as outF:
    with open(argv[1]) as inF:
        for l in inF:
            try:
                ziom = etree.fromstring(l)
            except etree.XMLSyntaxError:
                skipped += 1
                continue
            a1 = ziom.find('DaneAdresowe').find('AdresGlownegoMiejscaWykonywaniaDzialalnosci').find('KodPocztowy').text
            a2 = ziom.find('DaneDodatkowe').find('DataRozpoczeciaWykonywaniaDzialalnosciGospodarczej').text
            a3 = ziom.find('DaneDodatkowe').find('KodyPKD').text
            nazwaRaw = unicode(ziom.find('DanePodstawowe').find('Firma').text)
            bezpolskich = trans(nazwaRaw).encode('utf8')
            a4 = ' '.join(filter(lambda x: x.isalpha(), map(lambda x: x if x[-1].isalpha() else x[:-1], bezpolskich.split()))).lower()
            try:
                outF.write(','.join(map(str, [a1,a2,a4,a3])) + '\n')
            except UnicodeEncodeError:
                skipped += 1
                continue


# In[ ]:

print skipped, 'lines skipped'

