from addressbook import AddressBook, Record
from notebook import Notebook, Note
from file_serializer import SerializedObject
from exceptions import error_handler, InputError
from console_prompt import Command as ECommand
from console_prompt import CommandPrompt
from console_output import ConsoleOutput


############################ bot's commands #########################################
@error_handler
def add_contact(kwards, book):
    # add -name Joe Dow -phone 01233456789 -email joeDow@gmail.com -address Kyiv, Some St 45 -birthday 12.04.2000
    name = kwards.get("name")
    phone = kwards.get("phone")
    email = kwards.get("email")
    address = kwards.get("address")
    birthday = kwards.get("birthday")

    if not name or len(kwards) <= 1:
        raise InputError(
            "add : no name of contact or too less parameters were entered")

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
        record.add_email(email)

    if address:
        record.add_address(address)

    if birthday:
        record.add_birthday(birthday)

    ConsoleOutput().print_msg(message)


@error_handler
def change_contact(kwards, book):
    # TODO: change -phone -name Joe Dow -old 0123456789 -new 9876543210
    pass


@error_handler
def remove_contact(kwards, book):
    # TODO: remove -name Joe Dow
    pass


@error_handler
def find_contact(kwards, book):
    # TODO: find [-phone|-email|-address|-birthday|-name] <value>
    pass


@error_handler
def show_details(kwards, book):
    # TODO: show [-phone|-email|-address|-birthday] -name Joe Dow
    pass


@error_handler
def show_all_contacts(kwards, book):
    return ConsoleOutput().print_object_list(book.get_all_contacts())


@error_handler
def birthdays(kwards, book):
    ConsoleOutput().print_msg("People to congratulate next week:")
    ConsoleOutput().print_map(("Name", "Birthday"), book.get_upcoming_birthdays())


@error_handler
def show_help(kwards = None, _ = None):
    command_map = {
        "hello": "Greet the user",
        "help": "Show commands description",
        "add": "Add new contact",
        "change": "Edit contact",
        "remove": "Remove the contact",
        "find": "Find contact by selected criteria",
        "all": "Display all contacts",
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

    ConsoleOutput().print_msg("Note added")


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

    ConsoleOutput().print_msg(message)


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

    ConsoleOutput().print_msg(message)


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

    ConsoleOutput().print_msg(message)


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

    ConsoleOutput().print_msg(message)


@error_handler
def show_notes(kwards, notebook):
    notes = notebook.get_notes()
    ConsoleOutput().print_object_list(sorted(notes, key=lambda note: (
        ", ".join(sorted(list(note.tags))) if note.tags else "",
        note.id)))


@error_handler
def find_notes(kwards, notebook):
    # find_notes -tags #tag1,#tag2
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
        ConsoleOutput().print_msg("Welcome to the assistant bot!")
        show_help()
        self.__is_running = True
        while self.__is_running:
            command, args = CommandPrompt().prompt()
            command = command.strip().lower()

            try:
                index = self.__commands.index(command)
                self.__commands[index](args)
            except ValueError:
                ConsoleOutput().print_error("Error: Invalid command")

            CommandPrompt().dump_prompt()
            ConsoleOutput().clear()

        self.__book.save_data()
        self.__notes.save_data()

    def stop(self):
        self.__is_running = False


if __name__ == "__main__":
    console_bot = ConsoleBot()
    console_bot.start()
