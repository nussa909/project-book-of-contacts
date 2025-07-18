from addressbook import AddressBook, Record
from notebook import Notebook, Note
from file_serializer import SerializedObject
from exceptions import error_handler, InputError
from console_prompt import Command as ECommand
from console_prompt import CommandPrompt


############################ bot's commands #########################################
@error_handler
def add_contact(kwards, book):
    # add -name Joe Dow -phone 01233456789 -email joeDow@gmail.com -address Kyiv, Some St 45 -birthday 12.04.2000
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

    return message


@error_handler
def change_contact(kwards, book):
    # TODO: change -phone -name Joe Dow -old 0123456789 -new 9876543210
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
            raise InputError("change - both old and new phone numbers must be provided")
   
    record = book.find(name)
    if record is None:
        raise InputError(f"change - contact '{name}' not found")
    
    if old_phone and new_phone:
        if record.find_phone(new_phone):
            raise InputError(f"change - new phone '{new_phone}' already exists for contact '{name}'")   
        if not record.change_phone(old_phone, new_phone):
            raise InputError(f"change - old phone '{old_phone}' not found for contact '{name}'")

    if email:
        record.change_email(email)

    if address:
        record.change_address(address)

    if birthday:
        record.change_birthday(birthday)

    return "Contact updated"


@error_handler
def remove_contact(kwards, book):
    name = kwards.get("name")
    if not name:
        raise InputError("remove - no name of contact was entered")
    return book.remove(name) and f"Contact '{name}' removed" or f"Contact '{name}' not found"


@error_handler
def find_contact(kwards, book):
    name = kwards.get("name")
    phone = kwards.get("phone")
    email = kwards.get("email")
    address = kwards.get("address")
    birthday = kwards.get("birthday")
    if len(kwards) == 0:
        raise InputError("find - too less parameters were entered")
    
    if name:
        return book.find_records(name, 'name')
    if phone:
        return book.find_records(phone, 'phone')
    if email:
        return book.find_records(email, 'email')
    if address:
        return book.find_records(address, 'address')
    if birthday:
        return book.find_records(birthday, 'birthday')




@error_handler
def show_details(kwards, book):
    # TODO: show [-phone|-email|-address|-birthday] -name Joe Dow
    pass


@error_handler
def show_all_contacts(kwards, book):
    return f"{book}"


@error_handler
def birthdays(kwards, book):
    days = kwards.get("days", 7)
    print(f"People to congratulate next {days} days:")
    return '\n'.join(f"{name} : {birthday}" for name, birthday in book.get_upcoming_birthdays(days).items())


@error_handler
def show_help(kwards, _):
    # TODO: update and make it colorful
    message = """Possible commands:
    hello - greeting
    help - show help message
    add <name> <phone> <birthday> - add new contact
    change <name> <old phone> <new phone> <birthday> - modify existing contact
    phone <name> - print phone for dedicated contact
    all - print all contacts
    add-birthday <name> <birthday> - add birthday to contact
    show-birthday <name> - show birthday for dedicated contact
    birthdays - show contact who will celebrate birthday in next 7 days
    close/exit - exit bot
    """
    return message


@error_handler
def add_note(kwards, notebook):
    # add_note -title headline -text Note message -tags #tag1,#tag2
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

    return "Note added"


@error_handler
def change_note(kwards, notebook):
    # change_note -id note_id -title new title -text new text
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

    return message


@error_handler
def remove_note(kwards, notebook):
    # remove_note -id note_id
    id = int(kwards.get("id"))

    if not id:
        raise InputError("remove_note : id of note was not provided")

    note = notebook.find_note_by_id(id)
    message = "Note was removed"
    if note:
        notebook.remove_note(note)
    else:
        message = "Note was not found"

    return message


@error_handler
def add_tag(kwards, notebook):
    # add_tag -id note_id -tag #tag

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

    return message


@error_handler
def remove_tag(kwards, notebook):
    # remove_tag id_note -tag #tag
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

    return message


@error_handler
def show_notes(kwards, notebook):
    notes = notebook.get_notes()
    return sorted(notes, key=lambda note: (
        ", ".join(sorted(list(note.tags))) if note.tags else "",
        note.id
    ))


@error_handler
def find_notes(kwards, notebook):
    # find_notes -tags #tag1,#tag2
    tags_str = kwards.get("tags")

    tags = {}
    if tags_str:
        tags_str = tags_str.lower().strip()
        tags = set(tags_str.split(","))

    res = notebook.find_note_by_tags(tags)
    return sorted(res, key=Note.sort_by_title)


@error_handler
def say_bye(kwards, bot):
    bot.stop()
    return "Good bye!"
##############################################################################


class Command:

    def __init__(self, command, func, receiver):
        self.command = command.value
        self.func = func
        self.receiver = receiver

    def __eq__(self, command):
        return self.command == command

    def __call__(self, args):
        return self.func(args, self.receiver)


class ConsoleBot:

    def __init__(self):
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
                                   self.__book.object),
                           Command(ECommand.BIRTHDAYS, birthdays,
                                   self.__book.object),
                           Command(ECommand.ADD_NOTE, add_note,
                                   self.__notes.object),
                           Command(ECommand.REMOVE_NOTE, remove_note,
                                   self.__notes.object),
                           Command(ECommand.CHANGE_NOTE, change_note,
                                   self.__notes.object),
                           Command(ECommand.FIND_NOTES, find_notes,
                                   self.__notes.object),
                           Command(ECommand.ADD_TAGS, add_tag,
                                   self.__notes.object),
                           Command(ECommand.REMOVE_TAGS, remove_tag,
                                   self.__notes.object),
                           Command(ECommand.SHOW_NOTES, show_notes,
                                   self.__notes.object),
                           Command(ECommand.CLOSE, say_bye, self),
                           Command(ECommand.EXIT, say_bye, self)]
        self.__is_running = False

    def start(self):
    
        print("Welcome to the assistant bot!")
        self.__is_running = True
        while self.__is_running:
            command, args = CommandPrompt().prompt()
            command = command.strip().lower()

            try:
                index = self.__commands.index(command)
                print(self.__commands[index](args))
            except ValueError:
                print("Invalid command.")

        self.__book.save_data()
        self.__notes.save_data()

    def stop(self):
        self.__is_running = False


if __name__ == "__main__":
    console_bot = ConsoleBot()
    console_bot.start()
