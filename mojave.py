import requests
from lxml import html
from bs4 import BeautifulSoup

PAGE_1_URL = 'http://www.physics.purdue.edu/astro/MOJAVE/allsources.html'
PAGE_2_URL = 'http://www.physics.purdue.edu/astro/MOJAVE/sourcepages/0003+380.shtml'

def process_page1(url):
    r = requests.get(url)
    tree = html.fromstring(r.content)

    links = tree.xpath('//center//small/a')
    result = []
    for a in links:
        text = a.text
        href = 'http://http://www.physics.purdue.edu/astro/MOJAVE/' + a.attrib['href']
        result.append({'text': text, 'href': href})

    return result
    


def process_page2(url):
    r = requests.get(url)
    tree = html.fromstring(r.content)
    result = {}

    result['common_name'] = tree.xpath('/html/body/center/table[1]/tbody/tr[1]/td[2]/text()')[0]
    result['b1950_name'] = tree.xpath('/html/body/center/table[1]/tbody/tr[2]/td[2]/a/text()')[0]
    result['b1950_link'] = tree.xpath('/html/body/center/table[1]/tbody/tr[3]/td[2]/a/@href')[0]
    result['j2000_name'] = tree.xpath('/html/body/center/table[1]/tbody/tr[3]/td[2]/a/text()')[0]

    # beatiful soup 
    soup = BeautifulSoup(r.content, "html5lib")
    table = soup.findAll('table')[2]

    result['unk_array'] = []

    #print(table.tbody.findAll('tr'))

    for tr_index, tr in enumerate(table.tbody.findAll('tr')):
        tr_object = []
        for td_index, td in enumerate(tr.findAll('td')):
            td_object = {}
            td_object['text'] = td.text
            td_object['links'] = []
            
            for a in td.findAll('a'):
                a_object = {'text': a.text, 'href': a['href']}
                td_object['links'].append(a_object)

            tr_object.append(td_object)
        result['unk_array'].append(tr_object)
    return result


def download_link(url, file_name):
    r = requests.get(url, allow_redirects=True)
    open(file_name, 'wb').write(r.content)


result1 = process_page1(PAGE_1_URL)
print(result1)

result2 = process_page2(PAGE_2_URL)
print(result2)