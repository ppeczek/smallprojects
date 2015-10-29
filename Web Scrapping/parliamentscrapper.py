import requests
import bs4
import csv

root_url = 'http://www.sejm.gov.pl'
index_url = root_url + '/Sejm7.nsf/terminarz.xsp'


def get_sessions():
    """ Returns dictionary of title:url of every session of the parliament in 2015"""
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    url_list = [a.attrs.get('href') for a in soup.select('table tr a')]
    title_list = tuple([a.get_text() for a in soup.select('table tr a')])
    info = {}
    for element in title_list:
        info[element] = root_url + url_list.pop(0)
    return info


def get_sessions_agenda(session_url):
    """ Returns session agenda"""
    response = requests.get(session_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    agenda = [a.get_text().strip() for a in soup.select('ol li')]
    for number in range(0, len(agenda)):
        agenda[number] = str(number + 1) + ". " + agenda[number]
    return agenda


def to_csv():
    wynik = get_sessions()
    with open('names.csv', 'w') as csvfile:
        fieldnames = ['Title', 'Link', 'Agenda']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in wynik.items():
            agenda = get_sessions_agenda(wynik[key])
            writer.writerow({'Title': key, 'Link': value, 'Agenda': agenda})

to_csv()
