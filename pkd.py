import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
from trans import trans


with open('pkd.txt', 'r') as f:
    text = f.read().split('\n')

text

ptrn = re.compile('.+\s+(\d{2}\.\d)\s+(.*)')

codes = []
for line in text:
    line = trans(str(line))
    matches = ptrn.findall(line)
    if len(matches) > 0:
        pkd, desc = matches[0][-2:]
        desc = (str(desc).lower()
                         .replace('"', '')                         
                         .replace('<b>', '')
                         .replace('</b>', ''))
        codes.append((pkd, desc))
len(codes)

codes = pd.DataFrame(codes, columns=['pkd', 'opis'])
codes.to_csv('pkd.csv', index=False, sep='|')
