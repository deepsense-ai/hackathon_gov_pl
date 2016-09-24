
# coding: utf-8

# USAGE: python this.py YYYY\ MM
# Downloads all records from CEIDG

from settings import APIKEY


# In[2]:

from itertools import islice
from sys import argv
from socket import error as SocketError


# In[5]:

import suds
from lxml import etree


# In[6]:

WSDLFILE = 'https://datastore.ceidg.gov.pl/CEIDG.DataStore/services/DataStoreProvider.svc?wsdl'


# In[7]:

# create client
client = suds.client.Client(WSDLFILE, timeout=3600)


# In[8]:

def dawajludzi(rok = 2016, miesiac = 1):
    for year in [rok]:
        for month in [miesiac]:
            for day in reversed(range(1, 32, 7)):
                for dlen in reversed(range(7)):
                    try:
                        datefrom = '%.4d-%.2d-%.2d' % (year, month, day)
                        dateto = '%.4d-%.2d-%.2d' % (year, month, day+dlen)
                        for x in range(10):
                            try:
                                result = client.service.GetMigrationDataExtendedInfo(AuthToken=APIKEY, DateFrom=datefrom, DateTo=dateto)
                                break
                            except SocketError:
                                print "Socket Error, retrying for the {}th time".format(x+1)
                                pass
                        else:
                            print "10 tries failed for", year, month, day, '-', day + dlen
                        for el in etree.fromstring(result):
                            yield el
                        break
                    except suds.WebFault:
                        pass


# In[ ]:

args = argv[1].split()


# In[16]:

with open('gotten/ceidg%.4d-%.2d.xmlx' % (int(args[0]), int(args[1])), "w") as outF:
    for el in dawajludzi(int(args[0]), int(args[1])):
        outF.write(etree.tostring(el))
        outF.write('\n')


# In[ ]:

print "Success!", argv[1]

