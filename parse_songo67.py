"""
Source:
http://www.xn--67-1lclg.xn--p1ai/baza-dannyx-o-so-nko/reestr-so-nko-poluchatelej-podderzhki/
"""

from xlrd import open_workbook
from basic_operations import dump_utf_json

XLS_FNAME = 'sources/songo67_{}.xls'
JSON_FNAME = 'data/songo67.json'

YEAR = 'year'
AMOUNT = 'amount'
OGRN = 'ogrn'
INN = 'inn'
VIOLATIONS = 'violations'

MAPPER = ('regnum',  # номер реестровой записи
          'datedecision',  # дата принятия решения об оказании поддержки или о прекращении оказания поддержки
          'orgname',  # наименование постоянно действующего органа НКО
          'postaddress',  # почтовый адрес (место нахождения) постоянно действующего органа НКО
          OGRN,  # ОГРН
          INN,  # ИНН
          'activities',  # виды деятельности НКО
          'form',  # формы поддержки
          AMOUNT,  # размер поддержки
          'term',  # сроки оказания поддержки
          'violations',  # информация (если имеется) о нарушениях
          YEAR)  # год


def dump_orgs():
    orgs = list()

    for year in range(2012, 2018):
        print("Parsing %d..." % year)
        orgs.extend(parse_xls(year))

    dump_utf_json(orgs, JSON_FNAME)


def parse_xls(year):
    orgs = list()

    with open_workbook(XLS_FNAME.format(year), 'rb') as wb:
        sheet_names = wb.sheet_names()
        target_sheet = wb.sheet_by_name(sheet_names[0])

        for row in range(21, target_sheet.nrows):
            org = dict()

            for ind in range(len(MAPPER) - 1):
                org[MAPPER[ind]] = target_sheet.cell(row, ind).value

            if org[AMOUNT]:
                try:
                    org[AMOUNT] = float(org[AMOUNT].replace(u'\xa0', u'').replace(u' ', u''))
                except AttributeError:
                    pass

            if org[INN]:
                org[INN] = str(int(org[INN]))

            if org[OGRN]:
                org[OGRN] = str(int(org[OGRN]))

            if not org[VIOLATIONS]:
                org[VIOLATIONS] = None

            org[YEAR] = year

            orgs.append(org)

        return orgs


if __name__ == '__main__':
    # songos = parse_xls(2017)
    # for songo in songos:
    #     for key in songo:
    #         print(key)
    #         print(songo[key])
    #         print()
    #     print()
    #     print('**************************')
    #     print()

    # dump_orgs()

    pass
