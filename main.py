from comands import *

comands = {
    "hello": hello,
    "add": adding,
    "change": change_number,
    "phone": show_number,
    "show all": show_all_contacts,
    "good bye": close,
    "close": close,
    "exit": close,
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
    save_contacts_to_file(NUMBERS_PATH,numbers_dict)