from collections import defaultdict
from objects import *

def create_contacts_dict(path_to_file: str|object) -> AdressBook:
    """Creates dictionary from all contacts in file using name as key and phone numbers as values

    Args:
        path_to_file (str | object): path to file

    Returns:
        dict: {<name>: [<phone_numbers>]}
    """
    
    dictionary = AdressBook()
    with open(path_to_file, "r") as file:
        header = file.readline().split(",")
        name_ind = 0
        birthday_ind = 1
        phone_ind = [ind for ind,elem in enumerate(header) if "phone" in elem]
        mail_ind = [ind for ind,elem in enumerate(header) if "mail" in elem]
        while True:
            new_line = file.readline()
            if len(new_line) -1 == 0 or not new_line: 
                break
            line_list = new_line.replace("\n","").split(",")
            name = Name(line_list[name_ind])
            try:
                birthday = Birthday(line_list[birthday_ind])
            except:
                birthday = Birthday()
            numbers = list(map(Phone,[line_list[i] for i in phone_ind if line_list[i] != "-"]))
            mailes = list(map(Email,[line_list[i] for i in mail_ind if line_list[i] != "-"]))
            dictionary[str(name)] = Record(name, phone=numbers,email=mailes,birthday=birthday)
    return dictionary

def save_contacts_to_file(path_to_file: str|object ,contacts: AdressBook) -> None:
    """Save new contacts list in csv file

    Args:
        path_to_file (str | object): path to file
        contacts (dict): dictionary with phone numbers {<name>: [<phone_numbers>]}
    """
    with open(path_to_file,"w") as file:
        csv_rows = contacts.to_csv()
        file.write('\n'.join(csv_rows))
