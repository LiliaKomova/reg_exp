import csv
from pprint import pprint
from re import sub


# Читаем адресную книгу в формате CSV в список contacts_list:
def open_file(filename):
    with open(filename) as file:
        contacts = csv.reader(file)
        contacts_list = list(contacts)
    return contacts_list


#  Поместить Фамилию, Имя и Отчество человека в поля
#  lastname, firstname и surname соответственно.
def change_name(contacts_list):
    name = r'^([А-ЯЁа-яё]+)(\s*)(\,?)([А-ЯЁа-яё]+)' \
           r'(\s*)(\,?)([А-ЯЁа-яё]*)(\,?)(\,?)(\,?)'
    name_new = r'\1\3\10\4\6\9\7\8'
    contacts_list_new = list()
    for value in contacts_list:
        value_string = ','.join(value)
        formatted_value = sub(name, name_new, value_string)
        value_list = formatted_value.split(',')
        contacts_list_new.append(value_list)
    return contacts_list_new


#  Привести все телефоны в формат +7(999)999-99-99.
#  Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.
def change_number(contacts_list):
    number = r'(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)' \
             r'(\-*)(\d{3})(\s*)(\-*)(\d{2})(\s*)(\-*)' \
             r'(\d{2})(\s*)(\(*)(доб)*(\.*)(\s*)(\d+)*(\)*)'
    number_new = r'+7(\4)\8-\11-\14\15\17\18\19\20'
    contacts_list_new = list()
    for value in contacts_list:
        value_string = ','.join(value)
        formatted_value = sub(number, number_new, value_string)
        value_list = formatted_value.split(',')
        contacts_list_new.append(value_list)
    return contacts_list_new


#  Объединить все дублирующиеся записи о человеке в одну.
def unification_duplicate(contacts_list):
    for i in contacts_list:
        for j in contacts_list:
            if i[0] == j[0] and i[1] == j[1] and i is not j:
                if i[2] in '':
                    i[2] = j[2]
                if i[3] in '':
                    i[3] = j[3]
                if i[4] in '':
                    i[4] = j[4]
                if i[5] in '':
                    i[5] = j[5]
                if i[6] in '':
                    i[6] = j[6]
    contacts_list_new = list()
    for value in contacts_list:
        if value not in contacts_list_new:
            contacts_list_new.append(value)
    return contacts_list_new


#  Сохранение, получившихся данных в другой файл
def save_new_file(contacts_list):
    with open("phonebook.csv", "w") as file:
        datawriter = csv.writer(file, delimiter=',')
        datawriter.writerows(contacts_list)

try:
    if __name__ == '__main__':
        cont = open_file('phonebook_raw.csv')
        transform = change_name(cont)
        transform = change_number(transform)
        transform = unification_duplicate(transform)
        pprint(transform)
        save_new_file(transform)
except:
    print('Error! Try again!')