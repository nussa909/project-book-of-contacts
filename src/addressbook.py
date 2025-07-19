from collections import UserDict
import re
from datetime import datetime, timedelta
import exceptions

class Field:
    '''
    Base class for all fields in the address book.
    '''
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
    '''
    Class for names with validation.
    '''
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(value.title())

    def __validate_item(self, name: str):
        '''
        Validate the name field.
        This method checks if the name is a string, not empty, has at least 2 characters,
        and contains only letters, spaces, and hyphens.
        The name should not contain any special characters or numbers.

        Args:
            name (str): The name to validate.
        Raises:
            exceptions.ValidationError: If the name does not meet the validation criteria.      
        ''' 
        # check if name is a string
        if not isinstance(name, str):
            raise exceptions.ValidationError(f"Validation of name '{name}' failed. Expected type str.")
        # check if name is not empty and has at least 2 characters
        if len(name.strip())< 2:
            raise exceptions.ValidationError(f"Validation of name '{name}' failed. Name must be at least 2 characters long." )
        # check if name contains only letters, spaces, and hyphens
        if not all(char.isalpha() or char.isspace() or char == '-' for char in name):
             raise exceptions.ValidationError(f"Validation of name '{name}' failed. Name can only contain letters, spaces, and hyphens.")

class Phone(Field):
    '''
    Class for phone numbers with validation.
    '''
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(value)

    def __validate_item(self, phone: str):
        ''' 
        Validate the phone number.
        This method checks if the phone number is a string, matches the Ukrainian mobile number format,
        and is exactly 13 characters long (including the country code).
        The expected format is +380XXXXXXXXX, where X is a digit.

        Args:
            phone (str): The phone number to validate.
        Raises:
            exceptions.ValidationError: If the phone number does not meet the validation criteria.
        '''
        if not isinstance(phone, str):
            raise exceptions.ValidationError(f"Validation of phone '{phone}' failed. Expected type str")
        # check phone format
        match = re.match(r"^\+380\d{9}$", phone) 
        if not match:
            raise exceptions.ValidationError(f"Validation of phone '{phone}' failed. Ukrainian mobile number must be in +380XXXXXXXXX")

class Birthday(Field):
    '''
    Class for birthdays with validation and save as a date object.
    '''
    def __init__(self, value):
        self.__validate_item(value)
        super().__init__(datetime.strptime(value, "%d.%m.%Y"))

    def __validate_item(self, birthday: str):
        '''
        Validate the birthday field.
        This method checks if the birthday is a string in the format DD.MM.YYYY,
        and if the date is not in the future.
        The expected format is DD.MM.YYYY, where DD is the day, MM is the month, and YYYY is the year.

        Args:
            value (str): The birthday to validate.
        Raises:
            exceptions.ValidationError: If the birthday does not meet the validation criteria.
        '''
        if not isinstance(birthday, str):
            raise exceptions.ValidationError( f"Validation of birthday '{birthday}' failed. Expected type str")
        try:
            parse_date = datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise exceptions.ValidationError("Invalid date format. Use DD.MM.YYYY")
        if parse_date > datetime.now():
            raise exceptions.ValidationError("Birthday cannot be in the future.")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    def __repr__(self):
        return self.value.strftime("%d.%m.%Y")

class Email(Field):
    '''
    Class for email addresses with validation.
    '''
    def __init__(self, value: str):
        self.__validate_item(value)
        super().__init__(value)

    def __validate_item(self, email: str):
        '''
        Validate the email address.
        This method checks if the email is a string and matches a basic email format.
        The expected format is a string that contains an '@' symbol, followed by a domain name and a top-level domain.
        
        Args:
            email (str): The email address to validate.
        Raises:
            exceptions.ValidationError: If the email address does not meet the validation criteria.
        '''
        if not isinstance(email, str):
            raise exceptions.ValidationError(f"Validation of email '{email}' failed. Expected type str")
        match = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        if not match:
            raise exceptions.ValidationError(f"Validation of email '{email}' failed. Invalid email format")

class Address(Field):
    '''
    Class for addresses with validation.
    This class validates the address format and ensures it is a string of appropriate length.
    '''
    def __init__(self, value: str):
        self.__validate_item(value)
        super().__init__(value.title())

    def __validate_item(self, address: str):
        '''
        Validate the address field.
        This method checks if the address is a string and its length is appropriate.

        Args:
            address (str): The address to validate.
        Raises:
            exceptions.ValidationError: If the address does not meet the validation criteria.
        '''
        if not isinstance(address, str):
            raise exceptions.ValidationError(f"Validation of address '{address}' failed. Expected type str.")
        if len(address.strip()) < 5 or len(address.strip()) > 100:
            raise exceptions.ValidationError(f"Validation of address '{address}' failed. Address must be between 5 and 100 characters long.")

class Record:
    '''
    Class for a contact record in the address book.
    '''
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.address = None
        self.email = None
        self.birthday = None
    
    def add_phone(self, phone: str) -> bool:
        '''
        Add a phone number to the contact.
        This method checks if the phone number is already added before appending it to the list.

        Args:
            phone (str): The phone number to add.
        Returns:
            bool: True if the phone number was added, False if it was already present.
        '''
        if not self.__is_phone_added(phone):
            self.phones.append(Phone(phone))
            return True
        return False

    def change_phone(self, old_phone: str, new_phone: str) -> bool:
        '''
        Change an existing phone number to a new one.
        This method checks if the old phone number exists and if the new phone number is unique.

        Args:
            old_phone (str): The old phone number to change.
            new_phone (str): The new phone number to set.
        Returns:
            bool: True if the phone number was changed successfully, False otherwise.
        '''
        if old_phone == new_phone:
            raise exceptions.InputError("New phone should differ from previous one")

        index = self.__find_idx_by_phone(old_phone)
        if index is not None:
            self.phones[index] = Phone(new_phone)
            return True
        return False
    
    def remove_phone(self, phone: str) -> bool:
        '''
        Remove a phone number from the contact.
        This method checks if the phone number exists before attempting to remove it.

        Args:
            phone (str): The phone number to remove.
        Returns:
            bool: True if the phone number was removed, False if it was not found.
        '''
        phone_remove = self.find_phone(phone)
        if phone_remove:
            self.phones.remove(phone_remove)
            return True
        return False
        
    def find_phone(self, phone: str) -> Phone | None:
        '''
        Find a phone number in the contact.
        This method checks if the phone number exists in the contact's phone list.

        Args:
            phone (str): The phone number to find.
        Returns:
            Phone | None: The Phone object if found, None if not found.
        '''
        index = self.__find_idx_by_phone(phone)
        if index is not None:
            return self.phones[index]   
        return None

    def change_address(self, address: str) -> None:
        '''
        Change the address of the contact.
        This method updates the address of the contact with a new one.

        Args:
            address (str): The new address to set.
        '''
        self.address = Address(address)
    
    def remove_address(self) -> bool:
        '''
        Remove the address of the contact.
        This method checks if the address exists before attempting to remove it.

        Returns:
            bool: True if the address was removed, False if it was not found.
        '''
        if self.address is not None:
            self.address = None
            return True
        return False

    def change_email(self, email: str) -> None:
        '''
        Change the email of the contact.
        This method updates the email of the contact with a new one.

        Args:
            email (str): The new email to set.
        '''
        self.email = Email(email)
    
    def remove_email(self) -> bool:
        '''
        Remove the email of the contact.
        This method checks if the email exists before attempting to remove it.

        Returns:
            bool: True if the email was removed, False if it was not found.
        '''
        if self.email is not None:
            self.email = None
            return True
        return False

    def change_birthday(self, value: str) -> None:
        '''
        Change the birthday of the contact.
        This method updates the birthday of the contact with a new one.

        Args:
            value (str): The new birthday to set.
        '''
        self.birthday = Birthday(value)
    
    def remove_birthday(self) -> bool:
        '''
        Remove the birthday of the contact.
        This method checks if the birthday exists before attempting to remove it.

        Returns:
            bool: True if the birthday was removed, False if it was not found.
        '''
        if self.birthday is not None:
            self.birthday = None
            return True
        return False
    
    def __is_phone_added(self, phone: str)-> bool:
        '''
        Check if a phone number is already added to the contact.
        This method iterates through the contact's phone list to see if the phone number exists.

        Args:
            phone (str): The phone number to check.
        Returns:
            bool: True if the phone number is found, False otherwise.
        '''
        for phone_item in self.phones:
            if phone_item.value == phone:
                return True
        return False

    def __find_idx_by_phone(self, phone: str) -> int | None:
        '''
        Find the index of a phone number in the contact's phone list.
        This method uses a regular expression to match the phone number against the contact's phone list.

        Args:
            phone (str): The phone number to find.
        Returns:
            int | None: The index of the phone number if found, None if not found.
        '''
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
    '''
    Address Book to store and manage contacts.
    This class inherits from UserDict and provides methods to add, find, remove contacts,
    retrieve all contacts, and get upcoming birthdays.
    It also includes a method to search for records based on various fields using a pattern matching approach
    '''
    def __init__(self,):
        super().__init__()

    def get_all_contacts(self) -> list[Record]:
        '''
        Get all contacts in the address book.
        This method retrieves all contacts stored in the address book.

        Args:
            self: AddressBook instance.
        Returns:
            list: A list of all contacts in the address book.
        '''
        return [contact for _, contact in sorted(self.data.items(), key=lambda x: x[0].lower())]

    def add_record(self, record: Record) -> None:
        '''
        Add a record to the address book.
        This method adds a new record to the address book.
        If the record already exists (based on the name), it will update the existing record.
        
        Args:
            self: AddressBook instance.
            record (Record): The record to add to the address book.
        Returns:
            None
        '''
        self.data.update({record.name.value.lower(): record})

    def find(self, name: str) -> Record | None:
        ''' 
        Find a record by name.
        This method checks if the record exists in the address book and returns it if found.
        If the record is not found, it returns None.

        Args:
            self: AddressBook instance.
            name (str): The name of the record to find.
        Returns:
            Record | None: The record if found, None if not found.
        '''
        return self.data.get(name.lower())
    
    def remove(self, name: str) -> bool:
        '''
        Remove a record by name.
        This method checks if the record exists in the address book and removes it if found.
        If the record is not found, it returns False. If the record is successfully removed, it returns True.

        Args:
            self: AddressBook instance.
            name (str): The name of the record to remove.
        Returns:
            bool: True if the record was removed, False if it was not found.
        '''
        return self.data.pop(name.lower(), None) is not None

    def get_upcoming_birthdays(self, days: int = 7) -> dict[str, str]:
        '''
        Get a list of upcoming birthdays within a certain number of days.
        This method checks each record's birthday and calculates the next occurrence of the birthday.
        If the birthday is today or within the specified number of days, it adds it to the congratulation dictionary.
        If the birthday falls on a weekend, it adjusts the congratulation date to the next Monday.

        Args:
            self: AddressBook instance.
            days (int): The number of days to look ahead for upcoming birthdays. Defaults to 7.
        Returns:
            dict: A dictionary with names as keys and the date of the congratulation as values.
        '''
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
        This method allows searching for records based on a query string and a specified field type.
        The field_type can be one of the following: 'name', 'phone', 'email', 'address', 'birthday'.
        The search is performed using a pattern matching approach, where the query can contain wildcards:
        - '%' matches any sequence of characters
        - '_' matches any single character

        Arg:
            self: AddressBook instance.
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