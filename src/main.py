from addressbook import AddressBook, Record
from notebook import Notebook, Note
from file_serializer import SerializedObject
from exceptions import error_handler, InputError


############################ bot's commands #########################################
@error_handler
def add_contact(kwards, book):
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

    return message


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
    return f"{book}"


@error_handler
def birthdays(kwards, book):
    print("People to congratulate next week:")
    return '\n'.join(f"{name} : {birthday}" for name, birthday in book.get_upcoming_birthdays().items())


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
    pass


@error_handler
def remove_tag(kwards, notebook):
    # TODO: remove_tag id_note -tag #tag
    pass


@error_handler
def show_notes(kwards, notebook):
    # TODO: show_notes -sort #tag -filter #tag
    pass


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
        self.command = command
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
        self.__commands = [Command("help", show_help, self.__book.object),
                           Command("add", add_contact, self.__book.object),
                           Command("change", change_contact,
                                   self.__book.object),
                           Command("remove", remove_contact,
                                   self.__book.object),
                           Command("find", find_contact, self.__book.object),
                           Command("show", show_details, self.__book.object),
                           Command("all", show_all_contacts,
                                   self.__book.object),
                           Command("birthdays", birthdays, self.__book.object),
                           Command("add_note", add_note, self.__notes.object),
                           Command("remove_note", remove_note,
                                   self.__notes.object),
                           Command("change_note", change_note,
                                   self.__notes.object),
                           Command("find_notes", find_notes,
                                   self.__notes.object),
                           # TODO: add note's commands
                           Command("close", say_bye, self),
                           Command("exit", say_bye, self)]
        self.__is_running = False

    def start(self):
        print("Welcome to the assistant bot!")
        self.__is_running = True
        while self.__is_running:
            user_input = input("Enter a command: ")
            command, *args = self.__parse_input(user_input)

            try:
                index = self.__commands.index(command)
                print(self.__commands[index](args))
            except ValueError:
                print("Invalid command.")

        self.__book.save_data()
        self.__notes.save_data()

    def stop(self):
        self.__is_running = False

    def __parse_input(self, user_input):
        param_dct = {}
        cmd, *args = user_input.split("-")
        cmd = cmd.strip().lower()

        for item in args:
            params = item.split()
            param_dct.update({params[0]: " ".join(params[1:])})

        return cmd, param_dct


if __name__ == "__main__":
    console_bot = ConsoleBot()
    console_bot.start()


# add -name Joe Dow -phone 01233456789 -email joeDow@gmail.com -address Kyiv, Some St 45 -birthday 12.04.2000
# def parse_input_ext(user_input):
#     param_dct = {}
#     cmd, *args = user_input.split("-")
#     cmd = cmd.strip().lower()

#     for item in args:
#         params = item.split()
#         param_dct.update({params[0]: " ".join(params[1:])})

#     return cmd, param_dct


# book = AddressBook()
# input_text = "add -name Joe Dow -phone 0123456789,2222222222 -email joeDow@gmail.com -address Kyiv, Some St 45 -birthday 12.04.2000"
# cmd, params = parse_input_ext(input_text)
# print(cmd, params)

# add_contact(params, book)
# print(book)

# input_text = "show -phone -name Jow Dow"
# cmd, params = parse_input_ext(input_text)
# print(cmd, params)

# notebook = Notebook()

# user_input = "add_note -title headline -text Note message -tags #tag2,#tag1,personal"
# cmd, kwargs = parse_input_ext(user_input)
# add_note(kwargs, notebook)
# # print(notebook)

# user_input = "add_note -title Покупки -text Купить хлеб и молоко -tags buy,important"
# cmd, kwargs = parse_input_ext(user_input)
# add_note(kwargs, notebook)
# print(notebook)

# print("*"*10)
# user_input = "remove_note -id 1"
# cmd, kwargs = parse_input_ext(user_input)
# remove_note(kwargs, notebook)
# print(notebook)

# print("*"*10)
# user_input = "change_note -id 1 -title Email password -text my_mail@gmail.com, pass:1234"
# cmd, kwargs = parse_input_ext(user_input)
# change_note(kwargs, notebook)
# print(notebook)

# user_input = "add_note -title abc -text my_mail@gmail.com, pass:1234 -tags important"
# cmd, kwargs = parse_input_ext(user_input)
# add_note(kwargs, notebook)
# print(notebook)

# print("*"*10)
# user_input = "find_notes -tags buy,important"
# cmd, kwargs = parse_input_ext(user_input)
# res = find_notes(kwargs, notebook)
# print(res)
