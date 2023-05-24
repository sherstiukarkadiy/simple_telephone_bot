import re

def create_menu_rows(lst: list) -> list:
    """Create string rows for menu creating

    Args:
        lst (list): list of menu elements

    Returns:
        list: list of menu rows type str
    """
    
    new_list = []
    for ind,elem in enumerate(lst):
        new_list.append("{:^3}|{:^14}".format(ind+1,elem))
    return new_list

def errors_check(number: str) -> bool:
    """Chek if phone number has mistakes or not

    Args:
        number (str): phone number

    Returns:
        bool: True if number is not correct (includes not number symbols) otherwise False
    """
    
    if number.startswith("+"):
        number = number[1:] 
    
    not_number = re.search(r'\D',number)
    
    if not_number:
        return True
    else:
        return False

def sort_contacts(contacts: dict) -> dict:
    """Sorts dictionary by key

    Args:
        contacts (dict): dictionary with contacts

    Returns:
        dict: sorted dictionary
    """
    
    return dict(sorted(contacts.items(),key = lambda elem: elem))    