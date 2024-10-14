import re
import csv

PATH = "phonebook_raw.csv"
PHONE_PATTERN = r'(8|\+7)?\s*(\(*)(\d{3})(\)*)(\s*|-)(\d{3})(\s*|-)(\d{2})(\s*|-)(\d{2})\s*(\(*)(\w\w\w\.)*\s*(\d{4})*(\))*'
PHONE_SUB = r'+7(\3)\6-\8-\10 \12\13'


def open_file():
    """
    The function opens the file for reading.
    """
    with open(PATH, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def pars_contacts_list(contacts_list: list):
    """
    Function to return a new list of processed contacts
    params: contact_list - uploaded file with contact
    return: new_contact_list - the new list of processed contacts
    """
    new_contact_list = list()
    for contact in contacts_list:
        new_list = []
        full_name = ','.join(contact[:3])
        result = re.findall(r'(\w+)',full_name)
        while len(result) < 3:
            result.append('')
        new_list += result
        new_list.append(contact[3])
        new_list.append(contact[4])
        phone_pattern = re.compile(PHONE_PATTERN)
        change_phone = phone_pattern.sub(PHONE_SUB, contact[5])
        new_list.append(change_phone)
        new_list.append(contact[6])
        new_contact_list.append(new_list)
        print(new_list)
    return new_contact_list


def union(new_contact_list):
    """
    Function to return a list of unique contacts from dictionary values
    :param new_contact_list - the new list of processed contacts
    :return list(phone_book.values()) - list of unique contacts
    """
    phone_book = dict()
    for contact in new_contact_list:
        if contact[0] in phone_book:
            contact_values = phone_book[contact[0]]
            for i in range(len(contact_values)):
                if contact[i]:
                    contact_values[i] = contact[i]
        else:
            phone_book[contact[0]] = contact
    return list(phone_book.values())


def write_file(phone_book_list):
    """
    Function to write lines from contact list to file
    :param phone_book_list  - the list of the unique contacts
    """
    with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(phone_book_list)


contact_list = open_file()
new_pars_list = pars_contacts_list(contact_list)
phones_book = union(new_pars_list)
write_file(phones_book)