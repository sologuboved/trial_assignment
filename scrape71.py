import requests
from bs4 import BeautifulSoup
from basic_operations import dump_json

JSON_FNAME = 'sonko71.json'
URL2017 = 'http://nko71.ru/gospodderzhka/oblastnye-granty/reestr-sonko-poluchateley-podderzhki-2017-god.html'
URL2016 = 'http://nko71.ru/gospodderzhka/oblastnye-granty/reestr-sonko-poluchateley-podderzhki.html'
SOURCE = 'source'
COMMENT = 'comment'
VIOLATIONS = 'violations'
AMOUNT = 'amount'
N_A = 'n/a'
MAPPER = ('regnum',  # номер реестровой записи
          'datedecision',  # дата принятия решения об оказании поддержки или о прекращении оказания поддержки
          'orgname',  # наименование постоянно действующего органа НКО
          'postaddress',  # почтовый адрес (место нахождения) постоянно действующего органа НКО
          'ogrn',  # ОГРН
          'inn',  # ИНН
          'activities',  # виды деятельности НКО
          'form',  # формы поддержки
          AMOUNT,  # размер поддержки
          'term',  # сроки оказания поддержки
          VIOLATIONS,  # информация (если имеется) о нарушениях
          COMMENT,  # примечание
          SOURCE)  # источник


def scrape(url, beg, diff, field, field_n_a):
    def scrape_cells(rows):
        return [[cell.text for cell in row.find_all('td')] for row in rows]

    res = list()

    page_html = requests.get(url).content
    page_html = page_html.replace('&nbsp;'.encode(), ' '.encode())
    soup = BeautifulSoup(page_html, 'lxml')
    tbody = soup('tbody')[0]
    all_rows = tbody.find_all('tr')
    length = len(scrape_cells(all_rows[3:4])[0] + scrape_cells(all_rows[4:5])[0]) - diff
    orgs = scrape_cells(all_rows[beg:])

    for org in orgs:
        assert len(org) == length, "Something is amiss: current length {}, headers' length {}".format(len(org), length)
        cur_org = {MAPPER[ind]: org[ind].strip() if org[ind] else None for ind in range(length - 1)}
        cur_field_content = org[-1].strip()
        if not cur_field_content:
            cur_field_content = None
        cur_org[field] = cur_field_content
        cur_org[field_n_a] = N_A
        try:
            cur_org[AMOUNT] = float(cur_org[AMOUNT].replace(' ', '').replace(',', '.'))
        except ValueError as e:
            print(e)
        cur_org[SOURCE] = url
        res.append(cur_org)

    return res


def make_json():
    orgs2016 = scrape(url=URL2016, beg=5, diff=3, field=COMMENT, field_n_a=VIOLATIONS)
    orgs2017 = scrape(url=URL2017, beg=6, diff=2, field=VIOLATIONS, field_n_a=COMMENT)
    orgs_2016_2017 = orgs2016 + orgs2017
    dump_json(orgs_2016_2017, JSON_FNAME)

    # print(len(orgs_2016_2017))
    # for o in orgs_2016_2017:
    #     for key in o:
    #         print(key)
    #         print(o[key])
    #         print()
    #     print()
    #     print()


if __name__ == '__main__':
    make_json()
