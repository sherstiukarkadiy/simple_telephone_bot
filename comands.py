from file_processing_functions import *
from logic_functions import *
from pathlib import Path
import sys

NUMBERS_PATH = Path(__file__).parent.joinpath("telephone_numbers.csv")
numbers_dict = create_contacts_dict(NUMBERS_PATH)

def hello(*args) -> None:
    """greeting printing function
    """
    
    if len(args):
        print ("INVALID INPUT: too much charecters")
        return
    
    print("How can I help you?")
    
def adding(*args) -> None:
    """ add new contact or new number to other contact
    """
    
    global numbers_dict
    
    try:
        name,number = args
    except ValueError:
        print("INVALID INPUT: Not enough or too much charecters, to use this comand enter <name> <phone> separated by space")
        return
    
    if errors_check(number):
        print("INVALID INPUT: number is not correct")
        return
        
    if name in numbers_dict.keys():
        print("""\nYou already have current contact in your book
              \rTo change contact number use comand 'change'
              \rTo create new contact repeat comand 'add' using other contact name
              \rYou want to add this new number to current contact?(Y/N): """,end = "")
        agreement = input()
        if agreement.lower() == 'n':
            return 
    
    numbers_dict[name].append(number)
    numbers_dict = sort_contacts(numbers_dict)
    print("Contact edded")
    
def change_number(*args) -> None:
    """ change one of contacts numbers
    """
    
    global numbers_dict
    
    try:
        name,new_number = args
    except ValueError:
        print("INVALID INPUT: Not enough or too much charecters, to use this comand enter <name> <phone> separated by space")
        return
    
    if errors_check(new_number):
        print("INVALID INPUT: number is not correct")
        return
    
    if name not in numbers_dict.keys():
        print("""\nYou don't have any contact with this name
              \rTo create new contact use comand 'add'""")
        return
     
    elif len(numbers_dict[name]) > 1:
        menu_rows = create_menu_rows(numbers_dict[name])
        print("Choose number you want to change")
        print("\n".join(menu_rows))
        
        while True:
            try:
                index = int(input("variant number: "))-1
                numbers_dict[name][index] = new_number
                print("Number changed")
            except ValueError as er:
                print(er)
                continue
            except IndexError as er:
                print(er)
                continue
            break
    else:
        numbers_dict[name][0] = new_number
        print("Number changed")
        
def show_number(*args) -> None:
    """printing all numbers of current contact
    """
    
    if len(args) > 1:
        print("INVALID INPUT: too much charecters")
        return
    
    try:
        name = args[0]
    except IndexError:
        print("INVALID INPUT: No name were written")
        return 
    
    if name not in numbers_dict.keys():
        print("INVALID INPUT: No contact was found")
        return
    
    print(', '.join(numbers_dict[name]))

def show_all_contacts(*args) -> None:
    """printing all contacts
    """
    
    if len(args):
        print("INVALID INPUT: too much charecters")
        return
    
    print()
    for name,numbers in numbers_dict.items():
        print(f"{name}: {', '.join(numbers)}")

def close(*args) -> None:
    """breake all program
    """
    
    if len(args):
        print("INVALID INPUT: too much charecters")
        return
    
    print("Good bye")
    sys.exit()
    


    