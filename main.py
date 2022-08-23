from bs4 import BeautifulSoup
import sys
import urllib.request
import xml.etree.ElementTree as ET

url = 'https://kworb.net/charts/apple_s/ng.html'
#original_stdout = sys.stdout
with urllib.request.urlopen(url) as webPageResponse:
    outputHtml = webPageResponse.read()
    # print(outputHtml)

beaut = BeautifulSoup(outputHtml, 'lxml')
# for div in beaut.table.tr.td.find_all(True):
#     print(div)
k = beaut.table.tbody.prettify()
# print(k)
# for l in beaut.table.findAll(True):
#     print(l)
tree = ET.fromstring(k)

kkk = tree.findall('tr/td')

k = []
for list in kkk:
    if list:
        kl = list.find('div').text
        kl = kl.strip()
        print(kl)
        k.append(kl)
    # else:print(1)

print(k)