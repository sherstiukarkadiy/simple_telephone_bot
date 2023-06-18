import re
from exceptions import *

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

def phone_check(number: str) -> bool:
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

def email_check(email: str) -> bool:
    """Chek if email has mistakes

    Args:
        email (str): email number

    Returns:
        bool: True if email is not correct otherwise False
    """
    
    reg = r"[a-z]\w+@([a-z]{2,}\.)+[a-z]{2,}\b"
    
    email = re.search(reg,email)
    
    if not email:
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

def add_input_check(args: list) -> list|bool:
    
    if len(args) != 2:
        print("INVALID INPUT: Not enough or too much charecters, to use this comand enter <name> <phone\mail> separated by space")
        return False
    return args

def invalid_show_input(args: list) -> str|bool:
    
    if len(args) > 1:
        print("INVALID INPUT: too much charecters")
        return True
        
    try:
        value = args[0]
    except IndexError:
        print("INVALID INPUT: No name were written")
        return True
    
    return value
    
def try_to_class(value: str,__class: object) -> object|None:
    
    try:
        value = __class(value)
    except NoNameError as ne:
        print(ne)
        return
    except NoNumberError as nume:
        print(nume)
        return
    except NoMailError as me:
        print(me)
        return
    
    return value