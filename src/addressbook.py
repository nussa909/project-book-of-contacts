from collections import UserDict
import re
from datetime import datetime, timedelta
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

# Class for names with validation
class Name(Field):
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(value.title())

    def __validate_item(self, name: str):
        # check if name is a string
        if not isinstance(name, str):
            raise exceptions.ValidationError(f"Validation of name '{name}' failed. Expected type str.")
        # check if name is not empty and has at least 2 characters
        if len(name.strip())< 2:
            raise exceptions.ValidationError(f"Validation of name '{name}' failed. Name must be at least 2 characters long." )
        # check if name contains only letters, spaces, and hyphens
        if not all(char.isalpha() or char.isspace() or char == '-' for char in name):
             raise exceptions.ValidationError(f"Validation of name '{name}' failed. Name can only contain letters, spaces, and hyphens.")

# Class for phone numbers with validation
class Phone(Field):
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(value)

    def __validate_item(self, phone: str):
        if not isinstance(phone, str):
            raise exceptions.ValidationError(f"Validation of phone '{phone}' failed. Expected type str")
        # check phone format
        match = re.match(r"^\+380\d{9}$", phone) 
        if not match:
            raise exceptions.ValidationError(f"Validation of phone '{phone}' failed. Ukrainian mobile number must be in +380XXXXXXXXX")

# Class for birthdays with validation and save as a date object
class Birthday(Field):
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        
    def __validate_item(self, value: str):
        if not isinstance(value, str):
            raise exceptions.ValidationError( f"Validation of birthday '{value}' failed. Expected type str")
        try:
            parse_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise exceptions.ValidationError("Invalid date format. Use DD.MM.YYYY")
        if parse_date > datetime.now():
            raise exceptions.ValidationError("Birthday cannot be in the future.")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    def __repr__(self):
        return self.value.strftime("%d.%m.%Y")

class Email(Field):
    def __init__(self, email: str):
        self.__validate_item(email)
        super().__init__(email)

    def __validate_item(self, email: str):
        if not isinstance(email, str):
            raise exceptions.ValidationError(f"Validation of email '{email}' failed. Expected type str")
        match = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        if not match:
            raise exceptions.ValidationError(f"Validation of email '{email}' failed. Invalid email format")

class Address(Field):
    def __init__(self, address):
        self.__validate_item(address)
        super().__init__(address.title())

    def __validate_item(self, address: str):
        if not isinstance(address, str):
            message = f"Validation of address '{address}' failed. Expected type str."
            raise exceptions.ValidationError(message)
        if len(address.strip()) < 5 or len(address.strip()) > 100:
            message = f"Validation of address '{address}' failed. Address must be between 5 and 100 characters long."
            raise exceptions.ValidationError(message)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.address = None
        self.email = None
        self.birthday = None

    # phone have to be unique, so we check if it is already added
    def add_phone(self, phone: str)-> bool:
        if not self.__is_phone_added(phone):
            self.phones.append(Phone(phone))
            return True
        return False

    def change_phone(self, old_phone: str, new_phone: str)-> bool:
        if old_phone == new_phone:
            raise exceptions.InputError("New phone should differ from previous one")

        index = self.__find_idx_by_phone(old_phone)
        if index is not None:
            self.phones[index] = Phone(new_phone)
            return True
        return False
    
    def remove_phone(self, phone: str) -> bool:
        phone_remove = self.find_phone(phone)
        if phone_remove:
            self.phones.remove(phone_remove)
            return True
        return False
        
    def find_phone(self, phone: str) -> Phone | None:
        index = self.__find_idx_by_phone(phone)
        if index is not None:
            return self.phones[index]   
        return None

    def change_address(self, address: str) -> None:
        self.address = Address(address)
    
    def remove_address(self) -> bool:
        if self.address is not None:
            self.address = None
            return True
        return False

    def change_email(self, email: str) -> None:
        self.email = Email(email)
    
    def remove_email(self) -> bool:
        if self.email is not None:
            self.email = None
            return True
        return False
    
    def change_birthday(self, value) -> None:
        self.birthday = Birthday(value)
    
    def remove_birthday(self) -> bool:
        if self.birthday is not None:
            self.birthday = None
            return True
        return False
    
    def __is_phone_added(self, phone)-> bool:
        for phone_item in self.phones:
            if phone_item.value == phone:
                return True
        return False

    def __find_idx_by_phone(self, phone: str) -> int | None:
        for index, phone_item in enumerate(self.phones):
            regex = '^' + re.escape(phone).replace('%', '.*').replace('_', '.') + '$'
            if bool(re.match(regex, phone_item.value)):
                return index
        return None

    def __str__(self):
        ph = ", ".join(p.value for p in self.phones) or "N/A"
        em = self.email or "N/A"
        ad = self.address or "N/A"
        bd = self.birthday or "N/A"
        return f"{self.name}: phones={ph}; email={em}; address={ad}; birthday={bd}"
    
    def __repr__(self):
        return str(self)

class AddressBook(UserDict):
    def __init__(self,  autosave_interval_minutes=1):
        super().__init__()
        self.__autosave_interval_minutes = autosave_interval_minutes # interval for autosaving
        self.__last_autosave_time = datetime.now() # time of the last autosave

    def check_autosave(self):
        """
        Checks if it's time for autosaving.
        Returns False if __autosave_interval_minutes is 0.
        """
        if self.__autosave_interval_minutes == 0: 
            return False # disable autosave if interval is 0

        required_interval = timedelta(minutes=self.__autosave_interval_minutes) 
        return datetime.now() - self.__last_autosave_time >= required_interval 

    def autosave(self, save_function):
        """
        Autosaves the address book if the time interval has passed.
        Args:
            save_function: a function that takes the address book and filename as arguments and returns True if successful.
        Returns:
            True if autosave was successful, False otherwise.
        """
        if self.check_autosave():
            try:
                #success = save_function(self, self.__autosave_filename) 
                success = save_function(self)
                if success:
                    self.__last_autosave_time = datetime.now() 
                    return True
                else:
                    return False
            except Exception as e:
                return False
        return False

    def get_all_contacts(self):
        return [contact for _, contact in self.data.items()]

    def add_record(self, record: Record):
        self.data.update({record.name.value.lower(): record})

    # Find a record by name
    def find(self, name: str) -> Record | None:
        return self.data.get(name.lower())
    
    # Remove a record by name
    def remove(self, name: str) -> bool:
        return self.data.pop(name.lower(), None) is not None

    def get_upcoming_birthdays(self, days: int = 7) -> dict[str, str]:
        congratulation_dct = {}
        records = filter(lambda rec: rec.birthday != None, self.data.values())
        today_date = datetime.today().date()

        for record in records:
            birthday_value_date = record.birthday.value.date()
            try:
                birthday_this_year = birthday_value_date.replace(year=today_date.year)
            except ValueError:
                # This happens if birthday_date_original is Feb 29th and today_date.year is not a leap year.
                # In this case, we move the birthday to March 1st of the current year.
                birthday_this_year = datetime(today_date.year, 3, 1).date()

            if birthday_this_year < today_date:
                try:
                    next_birthday = birthday_value_date.replace(year=today_date.year + 1)
                except ValueError:
                    next_birthday = datetime(today_date.year + 1, 3, 1).date()
            else:
                next_birthday = birthday_this_year

            days_to_birthday = (next_birthday - today_date).days

            if 0 <= days_to_birthday <= days:
                congratulation_day = next_birthday
                if next_birthday.weekday() >= 5:
                    days_to_add = 7 - next_birthday.weekday()
                    congratulation_day = next_birthday + timedelta(days=days_to_add)
                congratulation_dct.update({record.name.value: datetime.strftime(congratulation_day, "%d.%m.%Y")})

        return congratulation_dct

    def find_records(self, query: str, field_type: str) -> list[Record]:
        """
        New method for searching records by various fields.
        Arg:
            self:  AddressBook.
            query: string for search.
            field_type: type field ('name', 'phone', 'email', 'address', 'birthday').
        Return: 
            list of Record
        """
        def like(pattern: str, text: str) -> bool:
            regex = '^' + re.escape(pattern).replace('%', '.*').replace('_', '.') + '$'
            return re.match(regex, text) is not None

        matching_records = [] # Initialize an empty list to store matching records
        search_value = query.lower() # lowercase 

        if field_type not in ['name', 'phone', 'email', 'address', 'birthday']:
           return matching_records # If field_type is not valid, return empty list

        for record in self.data.values():
            field_value = None

            if field_type == 'name' and record.name:
                field_value = record.name.value
            elif field_type == 'email' and record.email:
                field_value = record.email.value
            elif field_type == 'address' and record.address:
                field_value = record.address.value
            elif field_type == 'birthday' and record.birthday:
                try:
                    search_date = datetime.strptime(query, "%d.%m.%Y").date()
                    if record.birthday.value.date() == search_date:
                        matching_records.append(record)
                    continue # Next record
                except ValueError:
                    raise exceptions.InputError("Invalid birthday date format for search. Use DD.MM.YYYY")
            elif field_type == 'phone':
                # If field_type is 'phone', we use the find_phone method of Record
                if record.find_phone(query):
                    matching_records.append(record)
                continue #  Next record

            if field_value:
                if like(search_value, field_value.lower()):
                    matching_records.append(record)
                    
        return matching_records

    def __str__(self):
        str = "Address book:\n"
        for name, record in self.data.items():
            str += f"{record}\n"

        return str