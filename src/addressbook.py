from collections import UserDict
import re
from datetime import datetime
import exceptions


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(value.title())

    def __validate_item(self, name: str):
        if type(str) != type(str):
            message = f"Validation of name {name} failed. str type expected"
            raise exceptions.ValidationError(message)


class Phone(Field):
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(value)

    def __validate_item(self, phone: str):
        match = re.match(r"^\d{10}$", phone)
        if match == None:
            message = f"Validation of phone number {phone} failed. 10 digits expected"
            raise exceptions.ValidationError(message)


class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise exceptions.ValidationError(
                "Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return str(datetime.strftime(self.value, "%d.%m.%Y"))

    def __repr__(self):
        return str(datetime.strftime(self.value, "%d.%m.%Y"))


class Email(Field):
    def __init__(self, email: str):
        self.__validate_item(email)
        super().__init__(email)

    def __validate_item(self, email: str):
        match = re.match(r"^[\w._%+-]+@[\w.-]+\.[\w]+$", email)
        if match == None:
            message = f"Validation of email {email} failed"
            raise exceptions.ValidationError(message)


class Address(Field):
    def __init__(self, address):
        self.__validate_item(address)
        super().__init__(address.title())

    def __validate_item(self, address: str):
        if type(str) != type(str):
            message = f"Validation of address {address} failed. str type expected"
            raise exceptions.ValidationError(message)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.address = None
        self.email = None
        self.birthday = None

    def add_phone(self, phone: str):
        if not self.__is_phone_added(phone):
            self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        if old_phone == new_phone:
            raise exceptions.InputError(
                "new phone should differ from previous one")

        index = self.__find_idx_by_phone(old_phone)
        if index != None:
            self.phones[index] = Phone(new_phone)

    def remove_phone(self, phone: str):
        self.phones.remove(self.find_phone(phone))

    def find_phone(self, phone: str):
        index = self.__find_idx_by_phone(phone)
        if index != None:
            return self.phones[index]

    def add_address(self, address: str):
        self.address = Address(address)

    def add_email(self, email: str):
        self.email = Email(email)

    def __is_phone_added(self, phone):
        for phone_item in self.phones:
            if phone_item.value == phone:
                return True

        return False

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def __find_idx_by_phone(self, phone: str) -> int:
        for index, phone_item in enumerate(self.phones):
            if phone_item.value == phone:
                return index

    def __str__(self):
        return f"name:{self.name}, phones: {', '.join(p.value for p in self.phones)}, email: {self.email}, address: {self.address}, birthday:{self.birthday}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data.update({record.name.value.lower(): record})

    def find(self, name: str):
        return self.data.get(name.lower())

    def delete(self, name: str):
        self.data.pop(name.lower())

    def get_upcoming_birthdays(self):
        condratulation_dct = {}
        records = filter(lambda rec: rec.birthday != None, self.data.values())

        for record in records:
            today_date = datetime.today()

            birthday_this_year = record.birthday.value.replace(
                year=today_date.year)

            birthday_next_year = record.birthday.value.replace(
                year=today_date.year+1)

            next_birthday = birthday_this_year if birthday_this_year > today_date else birthday_next_year

            days_to_birthday = next_birthday.toordinal() - today_date.toordinal()

            if days_to_birthday <= 7:
                condratulation_day = next_birthday.replace(
                    day=next_birthday.day + 7 - next_birthday.weekday()) if next_birthday.weekday() >= 5 else next_birthday
                condratulation_dct.update(
                    {record.name: datetime.strftime(condratulation_day, "%d.%m.%Y")})

        return condratulation_dct

    def __str__(self):
        str = "Address book:\n"
        for name, record in self.data.items():
            str += f"{record}\n"

        return str
