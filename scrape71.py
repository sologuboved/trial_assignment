import requests
from bs4 import BeautifulSoup

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


def scrape(url, diff, field, field_n_a):
    def scrape_cells(rows):
        return [[cell.text for cell in row.find_all('td')] for row in rows]

    res = list()

    page_html = requests.get(url).content
    page_html = page_html.replace('&nbsp;'.encode(), ' '.encode())
    soup = BeautifulSoup(page_html, 'lxml')
    tbody = soup('tbody')[0]
    all_rows = tbody.find_all('tr')
    length = len(scrape_cells(all_rows[3:4])[0] + scrape_cells(all_rows[4:5])[0]) - diff
    orgs = scrape_cells(all_rows[6:])
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
        res.append(cur_org)

    print(res)
    return res


if __name__ == '__main__':
    # orgs2017 = scrape(URL2017, 2, VIOLATIONS, COMMENT)
    # for org2017 in orgs2017:
    #     for key in org2017:
    #         print(key)
    #         print(org2017[key])
    #         print()
    #     print()
    #     print()
    orgs2016 = scrape(URL2016, 3, COMMENT, VIOLATIONS)
    for org2016 in orgs2016:
        for key in org2016:
            print(key)
            print(org2016[key])
            print()
        print()
        print()
