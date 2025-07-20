from addressbook import AddressBook, Record
from notebook import Notebook, Note
from file_serializer import SerializedObject
from exceptions import error_handler, InputError
from console_prompt import Command as ECommand
from console_prompt import CommandPrompt, ContactKeys
from console_output import ConsoleOutput


############################ bot's commands #########################################
@error_handler
def add_contact(kwards, book: AddressBook) -> None:
    ''' 
    Add a new contact to the address book.
    The function takes keyword arguments for contact details and adds or updates the contact in the book.
    If the contact already exists, it updates the details.

    Args:
        kwards (dict): The keyword arguments containing contact details.
        book (AddressBook): The address book instance. 
    Raises:
        InputError: If the contact details are invalid. 
    '''
    name = kwards.get("name")
    phone = kwards.get("phone")
    email = kwards.get("email")
    address = kwards.get("address")
    birthday = kwards.get("birthday")
    if not name:
        raise InputError("add - no name of contact was entered")
    else:
        if len(kwards) <= 1:
            raise InputError("add - too less parameters were entered")

    record = book.find(name)
    message = f"Contact {name} updated"

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} added"

    if phone:
        if len(phone) > 10:
            phone_list = phone.split(",")
            for phone_item in phone_list:
                if phone_item != None:
                    record.add_phone(phone_item)
        else:
            record.add_phone(phone)

    if email:
        record.change_email(email)

    if address:
        record.change_address(address)

    if birthday:
        record.change_birthday(birthday)

    ConsoleOutput().print_msg(message)

@error_handler
def change_contact(kwards, book: AddressBook) -> None:
    '''
    Change an existing contact in the address book.
    The function takes keyword arguments for contact details and updates the contact in the book.

    Args:
        kwards (dict): The keyword arguments containing contact details.
        book (AddressBook): The address book instance.
    Raises:
        InputError: If the contact details are invalid.
    '''
    name = kwards.get("name")
    old_phone = kwards.get("old_phone")
    new_phone = kwards.get("new_phone")
    email = kwards.get("email")
    address = kwards.get("address")
    birthday = kwards.get("birthday")

    if not name:
        raise InputError("change - no name of contact was entered")
    else:
        if old_phone is None and new_phone is None and not (email or address or birthday):
            raise InputError("change - too less parameters were entered")
        elif (old_phone is None and new_phone is not None) or (old_phone is not None and new_phone is None):
            raise InputError(
                "change - both old and new phone numbers must be provided")

    record = book.find(name)
    if record is None:
        raise InputError(f"change - contact '{name}' not found")

    if old_phone and new_phone:
        if record.find_phone(new_phone):
            raise InputError(
                f"change - new phone '{new_phone}' already exists for contact '{name}'")
        if not record.change_phone(old_phone, new_phone):
            raise InputError(
                f"change - old phone '{old_phone}' not found for contact '{name}'")

    if email:
        record.change_email(email)

    if address:
        record.change_address(address)

    if birthday:
        record.change_birthday(birthday)

    ConsoleOutput().print_msg("Contact updated")

@error_handler
def remove_contact(kwards, book: AddressBook) -> None:
    '''
    Remove a contact from the address book.
    The function takes keyword arguments for contact details and removes the contact from the book.

    Args:
        kwards (dict): The keyword arguments containing contact details.
        book (AddressBook): The address book instance.
    Raises:
        InputError: If the contact details are invalid.
    '''
    name = kwards.get("name")
    if not name:
        raise InputError("remove - no name of contact was entered")
    book.remove(name)
    ConsoleOutput().print_msg(f"Contact '{name}' removed" or f"Contact '{name}' not found")

@error_handler
def find_contact(kwards, book: AddressBook) -> None:
    '''
    Find a contact in the address book.
    The function takes keyword arguments for contact details and searches for the contact in the book.

    Args:
        kwards (dict): The keyword arguments containing contact details.
        book (AddressBook): The address book instance.
    Raises:
        InputError: If the contact details are invalid.
    '''
    name = kwards.get("name")
    phone = kwards.get("phone")
    email = kwards.get("email")
    address = kwards.get("address")
    birthday = kwards.get("birthday")
    if len(kwards) == 0:
        raise InputError("find - too less parameters were entered")

    res = None
    if name:
        res = book.find_records(name, 'name')
    if phone:
        res = book.find_records(phone, 'phone')
    if email:
        res = book.find_records(email, 'email')
    if address:
        res = book.find_records(address, 'address')
    if birthday:
        res = book.find_records(birthday, 'birthday')

    if not res:
        k = next(iter(kwards))
        ConsoleOutput().print_msg(f"Contact not found for criteria: {k} = {kwards[k]}")
    else:
        ConsoleOutput().print_object_list(res)

@error_handler
def show_details(kwards, book: AddressBook) -> None:
    '''
    Show details of a specific contact in the address book.
    The function takes keyword arguments for contact details and displays the requested information.
    The filter can be one of the following: phone, email, address, birthday.
    If the contact does not exist or the filter is invalid, an error is raised.

    Args:
        kwards (dict): The keyword arguments containing contact details.
        book (AddressBook): The address book instance.
    Raises:
        InputError: If the contact details are invalid.
    '''
    name = kwards.get("name")
    filter = kwards.get("filter")
    if not name:
        raise InputError("show - no name of contact was entered")
    if filter not in [ContactKeys.PHONE.value, ContactKeys.EMAIL.value, ContactKeys.ADDRESS.value, ContactKeys.BIRTHDAY.value]:
        raise InputError(
            f"show - invalid filter '{filter}' provided. Valid filters are: phone, email, address, birthday")
    record = book.find(name)
    if record is None:
        raise InputError(f"show - contact '{name}' not found")
    messgae = ""
    data = {}
    match filter:
        case ContactKeys.PHONE.value:
            phones = record.phones
            if not phones:
                messgae = f"Contact '{record.name}' has no phone numbers"
            else:
                for idx, phone in enumerate(record.phones, start=1):
                    data[f"Phone #{idx}"] = phone
                # messgae = f"Phones for {record.name}: {', '.join(p.value for p in phones)}"
        case ContactKeys.EMAIL.value:
            email = record.email
            if not email:
                messgae = f"Contact '{record.name}' has no email"
            else:
                data["Email"] = record.email
        case ContactKeys.ADDRESS.value:
            address = record.address
            if not address:
                messgae = f"Contact '{record.name}' has no address"
            else:
                data["Address"] = record.address
        case ContactKeys.BIRTHDAY.value:
            birthday = record.birthday
            if not birthday:
                messgae = f"Contact '{record.name}' has no birthday"
            else:
                data["Birthday"] = record.birthday
    if messgae:
        ConsoleOutput().print_msg(messgae)
    else:
        ConsoleOutput().print_map_with_title('', data)

@error_handler
def show_all_contacts(kwards, books: list[AddressBook])-> None:
    '''
     Show all contacts or notes in the address book or notebook. 
     The function takes keyword arguments to determine whether to show contacts or notes.
        If "notes" is in the keyword arguments, it shows notes from the notebook.
        If "contacts" is in the keyword arguments, it shows contacts from the address book.
        If neither is specified, it defaults to showing contacts.

     Args:
         kwards (dict): The keyword arguments containing the request details.
         books (list[AddressBook]): The list of address books and notebooks.
     Raises:
         InputError: If the request details are invalid.
    '''
    if "notes" in kwards:
        ConsoleOutput().print_object_list(books[1].get_notes())
    else:
        ConsoleOutput().print_object_list(books[0].get_all_contacts())

@error_handler
def birthdays(kwards, book: AddressBook) -> None:
    '''
    Show upcoming birthdays for the specified number of days.
    The function takes keyword arguments to determine how many days ahead to check for upcoming birthdays.
    Args:
        kwards (dict): The keyword arguments containing the request details.
        book (AddressBook): The address book instance.
    Raises:
        InputError: If the request details are invalid.
    '''
    days = kwards.get("days", 7)
    try:
        days = int(days)
    except ValueError:
        raise InputError(f"birthdays - days {days} must be a positive integer")
    if days < 1:
        raise InputError(f"birthdays - days {days} must be more than 0")
    ConsoleOutput().print_msg(f"People to congratulate next {days} days:")
    ConsoleOutput().print_map(("Name", "Birthday"), book.get_upcoming_birthdays(days))


@error_handler
def show_help(kwards=None, _=None):
    '''
    Show help information about available commands.
    This function prints a list of commands and their descriptions to the console.
    Args:
        kwards (dict): The keyword arguments containing the request details.
        _ (NoneType): Placeholder for future use.
    Raises:
        None: This function does not raise any exceptions.
    '''
    command_map = {
        "help": "Show commands description",
        "add": "Add new contact",
        "change": "Edit contact",
        "remove": "Remove the contact",
        "find": "Find contact by selected criteria",
        "all": "Display all contacts/notes(contacts by default)",
        "birthdays": "Display contacts who have birthday next week and date when you have to condratulate them",
        "add_note": "Add new note",
        "remove_note": "Remove dedicated note",
        "change_note": "Edit dedicated note",
        "find_note": "Find notes by selected criteria",
        "add_tag": "Add tag to selected note",
        "remove_tag": "Remove tag from selected note",
        "show_notes": "Display notes sorted by tags",
        "exit/close": "Exit the application"
    }
    ConsoleOutput().print_map(("Command", "Description"), command_map)

@error_handler
def add_note(kwards, notebook: Notebook) -> None:
    '''
    Add a new note to the notebook.
    The function takes keyword arguments for note details and adds the note to the notebook.
    If the note already exists, it updates the details.

    Args:
        kwards (dict): The keyword arguments containing note details.
        notebook (Notebook): The notebook instance.
    Raises:
        InputError: If the note details are invalid.
    '''
    title = kwards.get("title")
    text = kwards.get("text")
    tags_str = kwards.get("tags")

    if not title or not text:
        raise InputError(
            "add_note : title or\\and text of note was not provided")

    tags = {}
    if tags_str:
        tags_str = tags_str.lower().strip()
        tags = set(tags_str.split(","))

    note = Note(title, text, tags)
    notebook.add_note(note)

    ConsoleOutput().print_msg("Note added")

@error_handler
def change_note(kwards, notebook: Notebook) -> None:
    '''
    Change an existing note in the notebook.
    The function takes keyword arguments for note identification and new details.
    If the note exists, it updates the details; otherwise, it raises an error.
    If no identification or new details are provided, it raises an error.

    Args:
        kwards (dict): The keyword arguments containing note identification and new details.
        notebook (Notebook): The notebook instance.
    Raises:
        InputError: If the note identification or new details are invalid.
    '''
    id = int(kwards.get("id"))
    new_title = kwards.get("title")
    new_text = kwards.get("text")

    if not id and not (new_title or new_text):
        raise InputError(
            "change_note : id or modifying attribute was not provided")

    note = notebook.find_note_by_id(id)
    message = "Note was updated"
    if note:
        if new_text:
            note.text = new_text
        if new_title:
            note.header = new_title
    else:
        message = "Note was not found"

    ConsoleOutput().print_msg(message)

@error_handler
def remove_note(kwards, notebook: Notebook) -> None:
    '''
    Remove an existing note from the notebook.
    The function takes keyword arguments for note identification.
    If the note exists, it removes it; otherwise, it raises an error.

    Args:
        kwards (dict): The keyword arguments containing note identification.
        notebook (Notebook): The notebook instance.
    Raises:
        InputError: If the note identification is invalid.
    '''
    id = int(kwards.get("id"))

    if not id:
        raise InputError("remove_note : id of note was not provided")

    note = notebook.find_note_by_id(id)
    message = "Note was removed"
    if note:
        notebook.remove_note(note)
    else:
        message = "Note was not found"

    ConsoleOutput().print_msg(message)

@error_handler
def add_tag(kwards, notebook: Notebook) -> None:
    '''
    Add a tag to an existing note in the notebook.
    The function takes keyword arguments for note identification and tag details.
    If the note exists, it adds the tag; otherwise, it raises an error.

    Args:
        kwards (dict): The keyword arguments containing note identification and tag details.
        notebook (Notebook): The notebook instance.
    Raises:
        InputError: If the note identification or tag details are invalid.
    '''
    id = int(kwards.get("id"))
    tag = kwards.get("tag")

    if not id or not tag:
        raise InputError("add_tag : id or tag of note was not provided")

    note = notebook.find_note_by_id(id)
    message = f"Tag {tag} for note was added"
    if note:
        note.add_tag(tag)
    else:
        message = "Note was not found"

    ConsoleOutput().print_msg(message)

@error_handler
def remove_tag(kwards, notebook: Notebook) -> None:
    '''
    Remove a tag from an existing note in the notebook.
    The function takes keyword arguments for note identification and tag details.
    If the note exists, it removes the tag; otherwise, it raises an error.

    Args:
        kwards (dict): The keyword arguments containing note identification and tag details.
        notebook (Notebook): The notebook instance.
    Raises:
        InputError: If the note identification or tag details are invalid.
    '''
    id = int(kwards.get("id"))
    tag = kwards.get("tag")

    if not id or not tag:
        raise InputError("remove_tag : id or tag of note was not provided")

    note = notebook.find_note_by_id(id)
    message = f"Tag {tag} for note was removed"
    if note:
        note.remove_tag(tag)
    else:
        message = "Note was not found"

    ConsoleOutput().print_msg(message)

@error_handler
def show_notes(kwards, notebook: Notebook) -> None :
    '''
    Show all notes in the notebook.
    The function retrieves all notes from the notebook and prints them to the console.
    It sorts the notes by tags and ID for better readability.
    If there are no notes, it prints an empty list.

    Args:
        kwards (dict): The keyword arguments containing the request details.
        notebook (Notebook): The notebook instance.
    Raises:
        None: This function does not raise any exceptions.
    '''
    notes = notebook.get_notes()
    ConsoleOutput().print_object_list(sorted(notes, key=lambda note: (
        ", ".join(sorted(list(note.tags))) if note.tags else "",
        note.id)))

@error_handler
def find_notes(kwards, notebook: Notebook) -> None :
    '''
    Find notes by tags in the notebook.
    The function takes keyword arguments for tags and searches for notes that match the specified tags.
    If the tags are not provided, it raises an error.
    Args:
        kwards (dict): The keyword arguments containing the tags to search for.
        notebook (Notebook): The notebook instance.
    Raises:
        InputError: If the tags are not provided or are invalid.
    '''

    tags_str = kwards.get("tags")

    tags = {}
    if tags_str:
        tags_str = tags_str.lower().strip()
        tags = set(tags_str.split(","))

    res = notebook.find_note_by_tags(tags)
    ConsoleOutput().print_object_list(sorted(res))

@error_handler
def say_bye(kwards, bot):
    bot.stop()
    ConsoleOutput().print_msg("Good buy!")
##############################################################################


class Command:
    """
    Represents a command for the console bot.

    Properties:
        command (str): The command name.
        func (callable): The function to execute for this command.
        receiver (object): The object or data to operate on.
    """

    def __init__(self, command, func, receiver):
        """
        Initialize the Command object.

        :param command: Command enum value.
        :param func: Function to execute.
        :param receiver: Data or object to operate on.
        """
        self.command = command.value  # Command name as string
        self.func = func              # Function to execute
        self.receiver = receiver      # Data or object to operate on

    def __eq__(self, command):
        """
        Compare the command with a string.

        :param command: Command string to compare.
        :return: True if equal, False otherwise.
        """
        return self.command == command

    def __call__(self, args):
        """
        Call the command's function with arguments.

        :param args: Arguments for the function.
        :return: Result of the function call.
        """
        return self.func(args, self.receiver)

class ConsoleBot:
    """
    Console bot for managing contacts and notes.

    Properties:
        __book (SerializedObject): Serialized address book.
        __notes (SerializedObject): Serialized notebook.
        __commands (list): List of Command objects.
        __is_running (bool): Bot running state.
    """

    def __init__(self):
        """
        Initialize the console bot with commands and data.
        This constructor sets up the address book and notebook, and initializes the commands list.
        It also sets the running state of the bot to False.
        """
        self.__book = SerializedObject("addressbook.pkl", AddressBook())
        self.__notes = SerializedObject("notebook.pkl", Notebook())
        self.__commands = [Command(ECommand.HELP, show_help, self.__book.object),
                           Command(ECommand.ADD, add_contact,
                                   self.__book.object),
                           Command(ECommand.CHANGE, change_contact,
                                   self.__book.object),
                           Command(ECommand.REMOVE, remove_contact,
                                   self.__book.object),
                           Command(ECommand.FIND, find_contact,
                                   self.__book.object),
                           Command(ECommand.SHOW_DETAILS,
                                   show_details, self.__book.object),
                           Command(ECommand.ALL, show_all_contacts,
                                   (self.__book.object, self.__notes.object)),
                           Command(ECommand.BIRTHDAYS, birthdays,
                                   self.__book.object),
                           Command(ECommand.ADD_NOTE, add_note,
                                   self.__notes.object),
                           Command(ECommand.REMOVE_NOTE,
                                   remove_note, self.__notes.object),
                           Command(ECommand.CHANGE_NOTE,
                                   change_note, self.__notes.object),
                           Command(ECommand.FIND_NOTES, find_notes,
                                   self.__notes.object),
                           Command(ECommand.ADD_TAGS, add_tag,
                                   self.__notes.object),
                           Command(ECommand.REMOVE_TAGS,
                                   remove_tag, self.__notes.object),
                           Command(ECommand.SHOW_NOTES, show_notes,
                                   self.__notes.object),
                           Command(ECommand.CLOSE, say_bye, self),
                           Command(ECommand.EXIT, say_bye, self)]
        self.__is_running = False  # Bot running state

    def start(self):
        '''
        Start the console bot.
        This method initializes the console output, prints a welcome message, and shows the help information.
        It enters a loop to prompt the user for commands, executes the commands, and handles errors
        until the bot is stopped.
        It saves the address book and notebook data before exiting.
        '''
        ConsoleOutput().clear()
        ConsoleOutput().print_msg("Welcome to the assistant bot!")
        show_help()
        # Start the console bot.
        self.__is_running = True
        while self.__is_running:
            try:
                command, args = CommandPrompt().prompt()
                command = command.strip().lower()

                index = self.__commands.index(command)
                self.__commands[index](args)
            except ValueError:
                ConsoleOutput().print_error("Error: Invalid command")
            except Exception as err:
                ConsoleOutput().print_error(f"Error: {err}")

        self.__book.save_data()
        self.__notes.save_data()

    def stop(self):
        """
        Stop the console bot loop.
        """
        self.__is_running = False


if __name__ == "__main__":
    console_bot = ConsoleBot()
    console_bot.start()
