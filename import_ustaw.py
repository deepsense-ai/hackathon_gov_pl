import requests
import numpy as np
from bs4 import BeautifulSoup
import re


ptrn_last_record = re.compile('.*>\d+-(\d+)</a>.*')
ptrn_old_pdf_links = re.compile('.*href="(/DU/\d+/s/\d+/\d+)".*')


def list_of_pdfs_after2012(year):
    url = 'http://dziennikustaw.gov.pl'
    url_year = '{}/DU/{}'.format(url, year)
    du = requests.get(url_year).text
    soup = BeautifulSoup(du, 'html.parser')
    last_records = str(soup.find_all('a', {'class': 'PapBold'})[0])
    last_record = int(ptrn_last_record.findall(last_records)[0])
    
    pdfs = []
    for record in range(last_record):
        pdf = '{url}/du/{year}/{record}/D{year}{record:07d}01.pdf'.format(
            url=url,
            year=year,
            record=record)
        pdfs.append(pdf)
    return pdfs


def list_of_pdfs_before2012(year):
    url = 'http://dziennikustaw.gov.pl'
    url_year = '{}/DU/{}'.format(url, year)
    du = requests.get(url_year).text
    soup = BeautifulSoup(du, 'html.parser')
    
    links = soup.find_all('a')
    links = [str(link) for link in links]
    links = [link for link in links if 'DU' in link]
    links = '\n'.join(links)
    links = ptrn_old_pdf_links.findall(links)

    pdfs = []
    for record in links:
        _, _, _, _, id0, id1 = record.split('/')
        pdf = '{url}/du/{year}/s/{id0}/{id1}/D{year}{id0:03d}{id1:04d}01.pdf'.format(
            url=url,
            year=year,
            record=record,
            id0=int(id0),
            id1=int(id1),)
        pdfs.append(pdf)
    return pdfs


for year in np.arange(2012, 2017):
    print year
    with open('ustawy/{}'.format(year), 'w') as f:
        f.write('\n'.join(list_of_pdfs_after2012(year)))


for year in np.arange(1989, 2012):
    print year
    with open('ustawy/{}'.format(year), 'w') as f:
        f.write('\n'.join(list_of_pdfs_before2012(year)))
