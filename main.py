from pprint import pprint
import csv
import re
import os


def fix_commas(contacts_list):
    """
    Приводим поля в соответствие с заголовком csv)
    """
    correct_format = len(contacts_list[0])
    for index, contact in enumerate(contacts_list):
        contacts_list[index] = contact[:correct_format]


def fix_fio(contacts_list):
    """
    Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно
    """
    for row in contacts_list[1:]:
        fio = re.search(r'([а-я]+[ин|ов|ев]а?) ([а-я]+) ?([а-я]+[ич|вна])?', ' '.join(row[:3]).strip(), flags=re.I)
        row[0], row[1], row[2] = fio.group(1), fio.group(2), fio.group(3)


def fix_phone(contacts_list):
    """
    Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999
    """
    for row in contacts_list[1:]:
        row[5] = re.sub(r'(\+?[7|8])? ?\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{2})[ -]?(\d{2}) ?\(?(доб.\)?)? ?(\d{4})?\)?',
                        r'+7(\2)\3-\4-\5 \6\7', row[5])
        row[5] = row[5].strip()


def merge_contacts(contacts_list):
    """
    Объединить все дублирующиеся записи о человеке в одну
    """
    surname = {}
    fixed_list = [contacts_list[0]]

    for index, row in enumerate(contacts_list[1:]):
        if row[0] not in surname.keys():
            surname[row[0]] = index + 1

        else:
            fix_row = contacts_list[surname[row[0]]]
            for i in range(1, 7):
                fix_row[i] = fix_row[i] or row[i]

    for index in surname.values():
        fixed_list.append(contacts_list[index])

    return fixed_list


if __name__ == '__main__':
    path = os.path.dirname(__file__)

    with open(path + "/phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts = list(rows)

        fix_commas(contacts)
        fix_fio(contacts)
        fix_phone(contacts)
        contacts = merge_contacts(contacts)

    with open(path + "/phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts)
pprint(contacts)
