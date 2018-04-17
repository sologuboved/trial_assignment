import requests
from bs4 import BeautifulSoup, NavigableString, Tag

PREFIX = 'http://nko71.ru'

ORGNAME = 'orgname'
WEBSITE = 'website'
MISSION = 'Миссия:'
OPF = "Организационно - правовая форма"
HEAD = 'Руководитель:'
CONTACTS = 'Контакты'
MUNICIPALITY = "Муниципальный район"

HEADERS = {MISSION: 'mission',
           'Целевые группы': 'targets',
           'Сферы деятельности': 'activities',
           'Реализованные проекты': 'projects',
           'Услуги': 'services',
           OPF: 'opf',
           HEAD: 'head',
           'Реквизиты': 'codes',
           CONTACTS: 'contacts',
           MUNICIPALITY: 'municipality'}

RUBRICS = [ORGNAME, WEBSITE] + list(HEADERS.values())


def scrape_org(url):
    org = dict.fromkeys(RUBRICS)
    page_html = requests.get(url).content
    soup = BeautifulSoup(page_html, 'lxml')

    org[ORGNAME] = soup.find_all('h1')[1].text.strip()

    raw_info = soup.find_all('article', {'class': "post clearfix"})[0]
    # print(raw_info)

    try:
        website = raw_info.find('a', href=True).get('href')
    except AttributeError:
        pass
    else:
        if '.' in website:
            org[WEBSITE] = website

    headers = raw_info.find_all('h3')
    for raw_header in headers:
        header = raw_header.text
        print(header)
        if header not in HEADERS:
            continue
        if header in (MISSION, OPF, HEAD, CONTACTS, MUNICIPALITY):
            postfix = ' '
        else:
            postfix = '*+*'
        info = str()
        for tag in raw_header.next_siblings:
            if tag.name == "h3":
                break
            else:
                if isinstance(tag, NavigableString):
                    new_info = tag.strip()
                elif isinstance(tag, Tag):
                    new_info = tag.get_text(strip=True).strip()
                else:
                    new_info = str()
                if new_info:
                    if new_info.startswith('-'):
                        new_info = new_info[1:]
                    info += new_info + postfix
                org[HEADERS[header]] = info.strip()
    return org


def scrape_mission():
    pass


if __name__ == '__main__':
    # print(scrape_org('http://nko71.ru/katalog-nko/nko-po-gruppam-naseleniya/vse-kategorii-grazhdan/bogoroditskoe-gorodskoe-kazache-obshchestvo.html'))
    print(scrape_org('http://nko71.ru/katalog-nko/nko-po-gruppam-naseleniya/vse-kategorii-grazhdan/vostochno-evropeyskiy-institut-ekonomiki-upravleniya-i-prava.html'))
    # print(scrape_org('http://nko71.ru/katalog-nko/nko-po-gruppam-naseleniya/invalidy/tulskoe-regionalnoe-otdelenie-obshcherossiyskoy-obshchestvennoy-organizatsii-novye-vozmozhnosti.html'))



