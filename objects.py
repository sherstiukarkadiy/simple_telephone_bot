from collections import UserDict
from logic_functions import *
import sys
import re

class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.value}"
    
    def __eq__(self, __value: object) -> bool:
        if self.value == __value.value:
            return True
        else:
            return False


class Name(Field):
    def __init__(self, name: str) -> None:
        if re.search(r"\W", name):
            raise NoNameError
        super().__init__(name)
        
class Phone(Field):
    def __init__(self, number: str|object) -> None:
        number = str(number)
        if phone_check(number):
            raise NoNumberError
        super().__init__(number)
        
class Email(Field):
    def __init__(self, email: str|object) -> None:
        email = str(email)
        if email_check(email):
            raise NoNumberError
        super().__init__(email)
        

class Record:
    def __init__(self, name,*, phone = None, email = None) -> None:
        self.name = name
        self.phones = []
        self.emailes = []
        if phone:
            if isinstance(phone,list):
                self.phones.extend(phone)
            else:
                self.phones.append(phone)
        if email:
            if isinstance(email,list):
                self.emailes.extend(email)
            else:
                self.phones.append(email)
            
    def add_phone(self,number: Phone) -> None:
        self.phones.append(number)
        
    def add_email(self,email: Email) -> None:
        self.emailes.append(email)
        
    def change_phone(self,index: int,new_phone: Phone) -> None:
        self.phones[index] = new_phone
    
    def change_email(self,index: int,email: Email) -> None:
        self.emailes[index] = email
        
    def __repr__(self) -> str:
        name = f"{self.name}"
        phones = f"{', '.join(map(str, self.phones))}"
        emailes = f"{', '.join(map(str, self.emailes))}"
        return f"Name: {name}\nPhones: {phones}\nEmailes: {emailes}"
        
class AdressBook(UserDict):
    
    def hello(self,*args) -> None:
        """greeting printing function
        """
    
        if len(args):
            print ("INVALID INPUT: too much charecters")
            return
        
        print("How can I help you?")
    
    def add_phone(self, *args) -> None:
        """ add new contact or new number to other contact
        """
        
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        key_name = str(key_name)
        
        name = try_to_class(key_name,Name)
        if not name: return
        
        number  = try_to_class(value,Phone)
        if not number: return
        
        if key_name not in self.data:
            self.data[key_name] = Record(name,phone = number)
        if key_name in self.data and number in self.data[key_name].phones:
            print("That contact already has this number")
            return
        else:
            self.data[key_name].add_phone(number)
        
        print("Contact edded")
        
    def add_mail(self, *args) -> None:
        """ add new contact or new number to other contact
        """
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        key_name = str(key_name)
        
        name = try_to_class(key_name,Name)
        if not name: return
        
        mail  = try_to_class(value,Email)
        if not mail: return
        
        if key_name not in self.data:
            self.data[key_name] = Record(name,email=mail)
        if key_name in self.data and mail in self.data[key_name].emailes:
            print("That contact already has this email")
            return
        else:
            self.data[key_name].add_email(mail)

        print("Contact edded")
        
    def add_contact(self, *args) -> None:
        """ add new contact or new number to other contact
        """
        
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        key_name = str(key_name)
        
        name = try_to_class(key_name,Name)
        if not name: return
        
        if key_name in self.data:
            print("""\nYou already have current contact in your book
                \rYou want to add this phone\mail to current contact?(Y/N): """,end = "")
            agreement = input()
            if agreement.lower() != 'y':
                return
        elif key_name not in self.data:
            self.data[key_name] = Record(name)
            self.data = sort_contacts(self.data)
        
        try:
            phone = Phone(value)
            self.add_phone(name,phone)
            return
        except:
            pass
        
        try:
            email = Email(value)
            self.add_mail(name,email)
            return
        except:
            pass
        
        print("Not correct phone or mail")
        
    def change_number(self, *args) -> None:
        """ change one of contacts numbers
        """
        
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        key_name = str(key_name)
        
        new_number  = try_to_class(value,Phone)
        if not new_number: return
        
        if key_name not in self.data:
            print("""\nYou don't have any contact with this name
                \rTo create new contact use comand 'add'""")
            return
        
        elif len(self.data[key_name].phones) > 1:
            menu_rows = create_menu_rows(list(map(str,self.data[key_name].phones)))
            print("Choose number you want to change")
            print("\n".join(menu_rows))
            
            while True:
                try:
                    index = int(input("variant number: "))-1
                    self.data[key_name].change_phone(index,new_number)
                    print("Number changed")
                except ValueError as er:
                    print(er)
                    continue
                except IndexError as er:
                    print(er)
                    continue
                break
        elif len(self.data[key_name].phones) == 1:
            self.data[key_name].change_phone(0,new_number)
            print("Number changed")
        else:
            self.data[key_name].add_phone(new_number)
           
    def change_mail(self, *args) -> None:
        """ change one of contacts mailes
        """
        
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        key_name = str(key_name)
        
        new_mail  = try_to_class(value,Email)
        if not new_mail: return
        
        if key_name not in self.data:
            print("""\nYou don't have any contact with this name
                \rTo create new contact use comand 'add'""")
            return
        
        elif len(self.data[key_name].emailes) > 1:
            menu_rows = create_menu_rows(list(map(str,self.data[key_name].emailes)))
            print("Choose mail you want to change")
            print("\n".join(menu_rows))
            
            while True:
                try:
                    index = int(input("variant number: "))-1
                    self.data[key_name].change_email(index,new_mail)
                    print("Mail changed")
                except ValueError as er:
                    print(er)
                    continue
                except IndexError as er:
                    print(er)
                    continue
                break
        elif len(self.data[key_name].emailes) == 1:
            self.data[key_name].change_email(0,new_mail)
            print("Mail changed")
        else:
            self.data[key_name].add_email(new_mail)
           
    def change_contact(self, *args) -> None:
        """ change one of contacts mailes
        """
        
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        
        if key_name not in self.data:
            print("No such contact")
            return
        
        try:
            phone = Phone(value)
            self.change_number(key_name,phone)
            return
        except:
            pass
        
        try:
            email = Email(value)
            self.change_mail(key_name,email)
            return
        except:
            pass
        
        print("Not correct phone\mail")
           
    def show_by_number(self, *args):
        
        value = invalid_show_input(args)
        if value is True:
            return
        
        phone = try_to_class(value,Phone)
        if not phone: return
        
        for contact in self.data.values():
            if phone in contact.phones:
                print()
                print(contact)
                return
                
    def show_by_mail(self, *args):
        
        value = invalid_show_input(args)
        if value is True:
            return
        
        mail  = try_to_class(value,Email)
        if not mail: return
            
        for contact in self.data.values():
            if mail in contact.emailes:
                print()
                print(contact)
                return
            
    def show_contact(self, *args) -> None:
        """printing all numbers of current contact
        """
        
        value = invalid_show_input(args)
        if value is True:
            return
        
        if value in self.data:
            print()
            print(self.data[value])
            return
        
        phone = email = None
        
        try:
            phone = Phone(value)
            self.show_by_number(phone)
            return
        except:
            pass
        
        try:
            email = Email(value)
            self.show_by_mail(email)
            return
        except:
            pass
        
        print("No matches founded")

    def show_all_contacts(self, *args) -> None:
        """printing all contacts
        """
        
        if len(args):
            print("INVALID INPUT: too much charecters")
            return
        
        print()
        for contact in self.data.values():
            print(str(contact).replace("\n","\t"))

    def close(self, *args) -> None:
        """breake all program
        """
        
        if len(args):
            print("INVALID INPUT: too much charecters")
            return
        
        print("Good bye")
        sys.exit()
        
        pass
