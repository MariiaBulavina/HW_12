from collections import UserDict
from datetime import datetime
import pickle

class BirthdayError(Exception):
    pass
   
class PhoneError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    def __eq__(self, __value: object) -> bool:
        return self.value == object


class Birthday(Field):
    
    def __init__(self, value):
        self.__value = None
        self.value = value

        super().__init__(value)
        
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime((str(value)), '%d-%m-%Y').date()
        except ValueError:
            raise BirthdayError


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if len(str(value)) == 10 and str(value).isdigit():
            self.__value = value
        else:
            raise PhoneError
     

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [phone] if phone else []

        self.birthday = birthday if birthday else None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):

        birthday = self.birthday.value
        today = datetime.now().date()

        current_year_birthday = birthday.replace(year=today.year)

        if current_year_birthday < today:
            current_year_birthday = current_year_birthday.replace(year=current_year_birthday.year+1)

        days_until_birthday = current_year_birthday - today

        return f'{days_until_birthday.days} days until {self.name}\'s birthday'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):

        for p in self.phones:

            if str(p.value) == phone:
                index = self.phones.index(p)
                self.phones.pop(index)
                return f'Contact number {self.name} {phone} has been deleted'
            
        return f'Contact {self.name} does not have a number {phone}'

    def edit_phone(self, old_phone, new_phone):

        for p in self.phones:
            if str(p.value) == old_phone:
                index = self.phones.index(p)
                self.phones[index] = Phone(new_phone)
                return f'Сontact number {self.name.value} {old_phone} has been changed to: {new_phone}' 
            
        raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join([str(p.value) for p in self.phones]) if self.phones else '...'}, birthday: {self.birthday if self.birthday else '...'}"  

    def __repr__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join([str(p.value) for p in self.phones]) if self.phones else '...'}, birthday: {self.birthday if self.birthday else '...'}"  


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        try:
            self.data.pop(name)
        except KeyError:
            return 'You have no contacts with this name'
        
        return f'Сontact with the name {name} has been deleted'
        
    def iterator(self, page):

        start_of_iteration = 0
        while True:
            if len(self.data) <= start_of_iteration:
                break
            result = list(self.data.items())[start_of_iteration:start_of_iteration+page]
            yield result
            start_of_iteration += page

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    def load(self, file_name):
            try:
                with open(file_name, 'rb') as file:
                    file.seek(0)
                    self.data = pickle.load(file)
            except FileNotFoundError:
                pass    
          