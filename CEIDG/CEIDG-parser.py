
# coding: utf-8

# In[8]:

from lxml import etree
from itertools import islice
from sys import argv
from trans import trans


# In[14]:

skipped = 0

pop = ''
with open(argv[1] + '.parsed', 'w') as outF:
    with open(argv[1]) as inF:
        for l in inF:
            if l.strip().endswith('</InformacjaOWpisie>'):
                try:
                    ziom = etree.fromstring(pop + l.strip())
                    pop = ''
                except etree.XMLSyntaxError:
                    skipped += 1
                    continue
            else:
                pop += l.strip()
                continue
            a1 = ziom.find('DaneAdresowe').find('AdresGlownegoMiejscaWykonywaniaDzialalnosci').find('KodPocztowy').text
            if not (len(a1) == 6 and a1[0:2].isdigit() and a1[2] == '-' and a1[3:].isdigit()):
                a1 = None
            a2 = ziom.find('DaneDodatkowe').find('DataRozpoczeciaWykonywaniaDzialalnosciGospodarczej').text
            a3 = ziom.find('DaneDodatkowe').find('KodyPKD').text
            nazwaRaw = unicode(ziom.find('DanePodstawowe').find('Firma').text)
            bezpolskich = trans(nazwaRaw).encode('utf8')
            bezkoncowek = map(lambda x: x if x[-1].isalpha() else x[:-1], bezpolskich.split())
            bezstartow = map(lambda x: x if x[0].isalpha() else x[1:], filter(lambda x: len(x) > 1, bezkoncowek))
            a4 = ' '.join(filter(lambda x: x.isalpha(), bezstartow)).lower()
            try:
                outF.write(','.join(map(str, [a1,a2,a4,a3])) + '\n')
            except UnicodeEncodeError:
                skipped += 1
                continue


# In[ ]:

print skipped, 'lines skipped in file', argv[1]

