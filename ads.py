
import requests
from lxml import html
from bs4 import BeautifulSoup

url_template = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PRE&qform=AST&arxiv_sel=astro-ph&arxiv_sel=cond-mat&arxiv_sel=cs&arxiv_sel=gr-qc&arxiv_sel=hep-ex&arxiv_sel=hep-lat&arxiv_sel=hep-ph&arxiv_sel=hep-th&arxiv_sel=math&arxiv_sel=math-ph&arxiv_sel=nlin&arxiv_sel=nucl-ex&arxiv_sel=nucl-th&arxiv_sel=physics&arxiv_sel=quant-ph&arxiv_sel=q-bio&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_logic=OR&obj_logic={}&author={}&object=&start_mon={}&start_year={}&end_mon={}&end_year={}&ttl_logic={}&title={}&txt_logic=OR&text=&nr_to_return=200&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=SHORT&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1'

author = 'feng'
author_logic = 'And'
start_mon = '1'
start_year = '2018'
end_mon = '12'
end_year = '2018'
title = ''
title_logic = 'OR'

page1_url = url_template.format(author_logic, author, start_mon, start_year, end_mon, end_year, title_logic, title)
print(page1_url)

def process_page1(url):
    r = requests.get(url)
    tree = html.fromstring(r.content)
    num = len(tree.xpath('/html/body/form[1]/table[2]//tr[position()>3]')) // 3

    nums = tree.xpath('/html/body/form[1]/table[1]//strong/text()')
    total_num = int(nums[0])
    result = {'total_num': total_num, 'info': [], 'next_url': []}

    # 当返回结果多于200时，出出现额外信息，解析规则不一样
    if (len(nums) == 3):
        total_num = int(nums[2])

    if (total_num > 200):
        page_num = total_num // 200
        if (total_num % 200 > 0):
            page_num = page_num + 1
        for i in range(0, page_num):
            next_url = r.url + '&start_cnt={}'.format(i*200+1)
            result['next_url'].append(next_url)

    for i in range(0, num):
        title = tree.xpath('/html/body/form[1]/table[2]//tr[{}]/td[2]/a/text()'.format((i+1)*3 + 1))[0]
        title_link = tree.xpath('/html/body/form[1]/table[2]//tr[{}]/td[2]/a/@href'.format((i+1)*3 + 1))[0]

        unkown = tree.xpath('/html/body/form[1]/table[2]//tr[{}]/td[4]/text()'.format((i+1)*3 + 1))[0]
        date = tree.xpath('/html/body/form[1]/table[2]//tr[{}]/td[5]/text()'.format((i+1)*3 + 1))[0]

        links = tree.xpath('/html/body/form[1]/table[2]//tr[{}]/td[6]/a'.format((i+1)*3 + 1))
        attach_links = []
        for a in links:
            l = {'text':a.text, 'href':a.attrib['href']}
            attach_links.append(l)

        author = tree.xpath('/html/body/form[1]/table[2]//tr[{}]/td[2]/text()'.format((i+1)*3 + 2))[0]
        desc = tree.xpath('/html/body/form[1]/table[2]//tr[{}]/td[4]/text()'.format((i+1)*3 + 2))[0]
        result['info'].append({
            'title:': title,
            'title_link': title_link, 
            'unkown': unkown,
            'date': date, 
            'attach_links': attach_links,
            'author': author,
            'desc': desc})

    return result


#'http://adsabs.harvard.edu/abs/2019arXiv190101119F'
def process_page2(url):
    result = {}
    tree = html.fromstring(requests.get(url).content)

    result['begin_links'] = (tree.xpath('/html/body/dl//a/@href'))
    # title
    result['title'] = tree.xpath('/html/body/table[1]/tbody/tr[1]/td[3]/text()')[0]

    author_links = tree.xpath('/html/body/table[1]/tbody/tr[2]/td[3]/a')
    result['authors'] = []
    for l in author_links:
        result['authors'].append({'name': l.text, 'href': l.attrib['href']})


    result['publication1'] = tree.xpath('/html/body/table[1]/tbody/tr[3]/td[3]/text()')
    result['publication2'] = tree.xpath('/html/body/table[1]/tbody/tr[4]/td[3]/text()')
    result['date'] = tree.xpath('/html/body/table[1]/tbody/tr[5]/td[3]/text()')
    result['Origin'] = tree.xpath('/html/body/table[1]/tbody/tr[6]/td[3]/text()')
    result['keywords'] = tree.xpath('/html/body/table[1]/tbody/tr[7]/td[3]/text()')
    result['comment'] = tree.xpath('/html/body/table[1]/tbody/tr[8]/td[3]/a/text()')
    result['bibliographic']  = tree.xpath('/html/body/table[1]/tbody/tr[8]/td[3]/a/@href')

    result['abstract'] = tree.xpath('/html/body/text()')
    return result



result = process_page1(page1_url)
#print(result)

if (len(result['next_url']) > 1):
    print('crawl next page:')
    url = result['next_url'][1]
    print(url)
    process_page1(url)

temp_url = result['info'][0]['title_link']
print(temp_url)
result = process_page2(temp_url)
print(result)