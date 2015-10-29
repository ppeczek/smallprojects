"""
Gets and prints list of upcoming Polish Constitutional Court cases
"""

import requests
import bs4

root_url = 'http://trybunal.gov.pl'
index_url = root_url + '/rozprawy/wokanda/'


def get_case_url():
    """ Returns urls of every upcoming case """
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return[a.attrs.get('href') for a in soup.select('div.case-item h2 a')]


def get_case_data(case_page_url):
    """ Gets and prints title, signature and url of every case """
    case_data = {}
    response = requests.get(root_url + case_page_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    title_and_signature = soup.select('article.master-article h1')[0].get_text().split()
    case_data['signature'] = ' '.join([title_and_signature[-2], title_and_signature[-1]])
    case_data['title'] = ' '.join(title_and_signature[0:-2])
    print(case_data['title'])
    print(case_data['signature'])
    print(root_url + case_page_url)

cases = get_case_url()

for case in cases:
    get_case_data(case)