# from comands import *
from objects import *
from file_processing_functions import *
from pathlib import Path

NUMBERS_PATH = Path(__file__).parent.joinpath("telephone_numbers.csv")
contacts = create_contacts_dict(NUMBERS_PATH)

comands = {
    "hello": contacts.hello,
    "add phone": contacts.add_phone,
    "add mail": contacts.add_mail,
    "add": contacts.add_contact,
    "change birthday": contacts.add_change_birth,
    "change phone": contacts.change_number,
    "change mail": contacts.change_mail,
    "change": contacts.change_contact,
    "contact": contacts.show_contact,
    "show all": contacts.show_all_contacts,
    "show parts": contacts.show_by_pages,
    "days to": contacts.days_to_birth,
    "good bye": contacts.close,
    "close": contacts.close,
    "exit": contacts.close,
    "help": (lambda *args: print([comand for comand in comands] if not len(args) else "INVALID INPUT: too much charecters"))
}

try:
    while True:
        print("(bot)>>>", end = "")
        user_comand = input().strip()
        for bot_com in comands:
            regex = re.escape(bot_com) + r"\b"
            comand_match = re.match(regex,user_comand)
            if comand_match: break
            
            
        if not comand_match:
            print(f"(bot): comand '{user_comand.split()[0]}' not found")
            continue
        
        comand = comand_match.group()
        user_args = user_comand[comand_match.end():].split()
        
        print("(bot):", end="")
        comands[comand](*user_args)
finally:
    save_contacts_to_file(NUMBERS_PATH,contacts)