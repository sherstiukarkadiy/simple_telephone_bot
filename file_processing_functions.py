from collections import defaultdict


def create_contacts_dict(path_to_file: str|object) -> dict:
    """Creates dictionary from all contacts in file using name as key and phone numbers as values

    Args:
        path_to_file (str | object): path to file

    Returns:
        dict: {<name>: [<phone_numbers>]}
    """
    
    dictionary = defaultdict(list)
    with open(path_to_file, "r") as file:
        header = file.readline()
        while True:
            new_line = file.readline()
            if not new_line: 
                break
            line_list = new_line.replace("\n","").split(",")
            name,number = line_list[0],line_list[1:]
            dictionary[name].extend(number)
    return dictionary

def save_contacts_to_file(path_to_file: str|object ,contacts: dict) -> None:
    """Save new contacts list in csv file

    Args:
        path_to_file (str | object): path to file
        contacts (dict): dictionary with phone numbers {<name>: [<phone_numbers>]}
    """
    def create_header():
        max_numbers_count = len(sorted(contacts.values(), key = lambda v: len(v))[-1])
        header = ["name"]
        for i in range(1,max_numbers_count+1):
            header.append(f"telephone_{i}")
        return ",".join(header)
    
    header = create_header()
    
    with open(path_to_file,"w") as file:
        file.write(header + "\n")
        for k,v in contacts.items():
            file.write(f"{k},{','.join(v)}\n")
