from collections import UserDict
from collections.abc import Iterator
from logic_functions import *
import sys
import re
from datetime import datetime
from calendar import isleap

class Field:
    def __init__(self, value) -> None:
        self.__value = value
    
    @property
    def value(self):
        return self.__value
    
    def __str__(self) -> str:
        return f"{self.value}"
    
    def __eq__(self, __value: object) -> bool:
        if self.value == __value.value:
            return True
        else:
            return False

class Name(Field):
    def __init__(self, name: str) -> None:
        self.value = name
        
    @property
    def value(self):
        return super().value
        
    @value.setter
    def value(self, value):
        if re.search(r"\W", value):
            raise NoNameError
        super().__init__(value)
        
class Phone(Field):
    def __init__(self, number: str) -> None:
        self.value = number
    
    @property
    def value(self):
        return super().value
    
    @value.setter
    def value(self, number: str|object) -> None:
        number = str(number)
        if phone_check(number):
            raise NoNumberError
        super().__init__(number)
        
class Email(Field):
    def __init__(self, email: str) -> None:
        self.value = email
    
    @property
    def value(self):
        return super().value
    
    @value.setter
    def value(self, email: str|object) -> None:
        email = str(email)
        if email_check(email):
            raise NoMailError
        super().__init__(email)
        
class Birthday(Field):
    def __init__(self, date: str = "dd/mm/yyyy") -> None:
        self.value = date
    
    @property
    def value(self):
        return super().value
    
    @value.setter
    def value(self, date: str|object) -> None:
        date = str(date)
        if date == "dd/mm/yyyy":
            super().__init__(date)
            return
        
        date = birthday_check(date)
        if not date:
            raise NoDateError
        else:
            day,month,year = map(int,date)
            date = datetime(year=year,month=month,day=day)
        super().__init__(date)
        
    def __str__(self) -> str:
        if isinstance(self.value, datetime):
            return self.value.strftime("%d.%m.%Y")
        else:
            return self.value

class Record:
    def __init__(self, name: Name,*, phone: Phone = None, email: Email = None, birthday = Birthday()) -> None:
        self.name = name
        self.phones = []
        self.emailes = []
        self.birthday = birthday
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
    
    def change_birthday(self,birthday: Birthday) -> None:
        self.birthday = Birthday(birthday)
    
    def days_to_birthday(self) -> int:
        today = datetime.now()
        birthday = self.birthday.value
        if isinstance(birthday,str):
            return "Current contact don't have birthday date"
        
        birthday = birthday.replace(year = today.year)
        if today <= birthday:
            pass
        else:
            birthday = self.birthday.value.replace(year = today.year+1)
        time_to_birth =  (birthday - today)
    
        return time_to_birth.days
    
    def __repr__(self) -> str:
        name = self.name
        birth = str(self.birthday)
        phones = f"{', '.join(map(str, self.phones))}"
        emailes = f"{', '.join(map(str, self.emailes))}"
        return f"Name: {name}\nBirthday: {birth}\nPhones: {phones}\nEmailes: {emailes}"

class Iterable:
    def __init__(self, contacts: list) -> None:
        self.current_index = 0
        self.contacts = contacts
        
    def __next__(self):
        if self.current_index <= len(self.contacts):
            new_ind = self.current_index + 5
            res = self.contacts[self.current_index: new_ind]
            self.current_index = new_ind
            res = map(lambda x: str(x).replace("\n","\t"), res)
            return '\n'.join(res)
        raise StopIteration
        
class AdressBook(UserDict):
    
    def hello(self,*args) -> None:
        """greeting printing function
        """
    
        if len(args):
            print ("INVALID INPUT: too much charecters")
            return
        
        print("How can I help you?")
        
    def add_change_birth(self, *args):
        
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        key_name = str(key_name)
        
        new_date  = try_to_class(value,Birthday)
        if not new_date: return
        
        if key_name not in self.data:
            print("""\nYou don't have any contact with this name
                \rTo create new contact use comand 'add'""")
            return
        
        self.data[key_name].change_birthday(new_date)
        print("Contact changed\\added")
    
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
        
        if len(args) == 1:
            key_name = args[0]
            name = try_to_class(key_name,Name)
            if not name: return
            self.data[key_name] = Record(name)
            return
        
        args = add_input_check(args)
        if not args: return
        key_name,value = args
        key_name = str(key_name)
        
        name = try_to_class(key_name,Name)
        if not name: return
        
        if key_name in self.data:
            print("""\nYou already have current contact in your book
                \rYou want to add this phone\mail to current contact, or to cahange hith birthday?(Y/N): """,end = "")
            agreement = input()
            if agreement.lower() != 'y':
                return
        elif key_name not in self.data:
            self.data[key_name] = Record(name)
            self.data = sort_contacts(self.data)
        
        birth = phone = email = None
        
        try:
            birth = Birthday(value)
            self.add_change_birth(key_name,birth)
            return
        except:
            pass
        
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
        
        print("Not correct phone/mail/date")
        
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
        
        birth = phone = email = None
        
        try:
            birth = Birthday(value)
            self.add_change_birth(key_name,birth)
            return
        except:
            pass
        
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
        
    def show_by_birth(self, *args):
        
        value = invalid_show_input(args)
        if value is True:
            return
        
        birth  = try_to_class(value,Birthday)
        if not birth: return
            
        for contact in self.data.values():
            if birth == contact.birthday:
                print()
                print(contact)
           
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
        
        birth = phone = email = None
        
        try:
            birth = Birthday(value)
            self.show_by_birth(birth)
            return
        except:
            pass
        
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
            
    def days_to_birth(self, *args):
        
        value = invalid_show_input(args)
        if value is True:
            return
        
        if value in self.data:
            print()
            print(self.data[value].days_to_birthday())
            return
        
        print("No matches founded")

    def close(self, *args) -> None:
        """breake all program
        """
        
        if len(args):
            print("INVALID INPUT: too much charecters")
            return
        
        print("Good bye")
        sys.exit()
        
        pass
    
    def __iter__(self) -> Iterator:
        return Iterable(list(self.data.values()))
    
    def show_by_pages(self):
        i = 1
        for page in self:
            print(f"\nPage {i}:")
            print(page)
            i += 1
    
    def to_csv(self):
        
        def create_header():
            max_numbers_count = len(sorted(self.data.values(), key = lambda v: len(v.phones))[-1].phones)
            max_email_count = len(sorted(self.data.values(), key = lambda v: len(v.emailes))[-1].emailes)
            header = ["name,birthday"]
            for i in range(1,max_numbers_count+1):
                header.append(f"telephone_{i}")
            for j in range(1,max_email_count+1):
                header.append(f"email_{j}")
            return ",".join(header), max_numbers_count,max_email_count
        
        header,max_num_count,max_email_count = create_header()
        
        csv_rows = [header]
        for contact in self.data.values():
            name = str(contact.name)
            birthday = str(contact.birthday)
            phones_list = list(map(str, contact.phones))
            emailes_list = list(map(str,contact.emailes))
            
            while len(phones_list) < max_num_count: phones_list.append("-")
            while len(emailes_list) < max_email_count: emailes_list.append("-")
            
            csv_rows.append(f"{name},{birthday},{','.join(phones_list)},{','.join(emailes_list)}")
        
        return csv_rows