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
        phone_ind = [ind for ind,elem in enumerate(header) if "phone" in elem]
        mail_ind = [ind for ind,elem in enumerate(header) if "mail" in elem]
        while True:
            new_line = file.readline()
            if len(new_line) -1 == 0 or not new_line: 
                break
            line_list = new_line.replace("\n","").split(",")
            name = Name(line_list[name_ind])
            numbers = list(map(Phone,[line_list[i] for i in phone_ind if line_list[i] != "-"]))
            mailes = list(map(Email,[line_list[i] for i in mail_ind if line_list[i] != "-"]))
            dictionary[str(name)] = Record(name, phone=numbers,email=mailes)
    return dictionary

def save_contacts_to_file(path_to_file: str|object ,contacts: AdressBook) -> None:
    """Save new contacts list in csv file

    Args:
        path_to_file (str | object): path to file
        contacts (dict): dictionary with phone numbers {<name>: [<phone_numbers>]}
    """
    def create_header():
        max_numbers_count = len(sorted(contacts.values(), key = lambda v: len(v.phones))[-1].phones)
        max_email_count = len(sorted(contacts.values(), key = lambda v: len(v.emailes))[-1].emailes)
        header = ["name"]
        for i in range(1,max_numbers_count+1):
            header.append(f"telephone_{i}")
        for j in range(1,max_email_count+1):
            header.append(f"email_{j}")
        return ",".join(header), max_numbers_count,max_email_count
    
    header,max_num_count,max_email_count = create_header()
    
    with open(path_to_file,"w") as file:
        file.write(header + "\n")
        for contact in contacts.values():
            name = f"{contact.name}"
            phones_list = list(map(str, contact.phones))
            emailes_list = list(map(str,contact.emailes))
            
            while len(phones_list) < max_num_count: phones_list.append("-")
            while len(emailes_list) < max_email_count: emailes_list.append("-")
            
            file.write(f"{name},{','.join(phones_list)},{','.join(emailes_list)}\n")
