from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, DummyCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from enum import Enum
from exceptions import InputError, error_handler


class Command(Enum):
    HELP = "help"
    ADD = "add"
    CHANGE = "change"
    REMOVE = "remove"
    FIND = "find"
    SHOW_DETAILS = "show"
    ALL = "all"
    BIRTHDAYS = "birthdays"
    ADD_NOTE = "add_note"
    REMOVE_NOTE = "remove_note"
    CHANGE_NOTE = "change_note"
    FIND_NOTES = "find_notes"
    ADD_TAGS = "add_tags"
    REMOVE_TAGS = "remove_tags"
    SHOW_NOTES = "show_notes"
    CLOSE = "close"
    EXIT = "exit"


class ContactKeys(Enum):
    NAME = "name"
    PHONE = "phone"
    EMAIL = "email"
    ADDRESS = "address"
    BIRTHDAY = "birthday"
    OLD_PHONE = "old_phone"
    NEW_PHONE = "new_phone"


class NoteKeys(Enum):
    ID = "id"
    TITLE = "title"
    TEXT = "text"
    TAGS = "tags"
    TAG = "tag"


class FirstWordCompleter(Completer):
    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        if ' ' in document.text_before_cursor:
            return

        current_word = document.get_word_before_cursor()
        for word in self.words:
            if word.startswith(current_word):
                yield Completion(word, start_position=-len(current_word))


style = Style.from_dict({
    "prompt": "#884444",
    "command": "#00aa00",
    "params": "#0003aa",
})


class Builder:
    def __init__(self, session):
        self.session = session
        self.result = {}

    def prompt(self, prompt):
        val = self.session.prompt(prompt, completer=DummyCompleter())
        return val if val.strip() else None

    def get_property(self, prompt, key):
        colored_prompt = FormattedText([("class:params", prompt)])
        value = self.prompt(colored_prompt)
        if value:
            value = value.strip()
            self.result.update({key: value})

    def what(self, prompt, completer_list):
        completer = FirstWordCompleter(completer_list)
        property = self.session.prompt(
            prompt, completer=completer)
        property = property.strip()
        return property

    def build(self):
        return self.result


class ContactBuilder(Builder):
    def get_name(self):
        self.get_property("name:", ContactKeys.NAME.value)

    def get_phone(self):
        self.get_property("phones:", ContactKeys.PHONE.value)

    def get_email(self):
        self.get_property("email:", ContactKeys.EMAIL.value)

    def get_address(self):
        self.get_property("address:", ContactKeys.ADDRESS.value)

    def get_birthday(self):
        self.get_property("birthday:", ContactKeys.BIRTHDAY.value)


class AddBuilder(ContactBuilder):
    def build(self):
        self.get_name()
        self.get_phone()
        self.get_email()
        self.get_address()
        self.get_birthday()
        return self.result


class ChangeBuilder(ContactBuilder):
    def old_phone(self):
        self.get_property("old phone:", ContactKeys.OLD_PHONE.value)

    def new_phone(self):
        self.get_property("new phone:", ContactKeys.NEW_PHONE.value)

    def build(self):
        self.get_name()
        property_to_edit = self.what("what property are you gonna change:",
                                     [ContactKeys.PHONE.value, ContactKeys.EMAIL.value, ContactKeys.ADDRESS.value, ContactKeys.BIRTHDAY.value])
        match property_to_edit:
            case ContactKeys.PHONE.value:
                self.old_phone()
                self.new_phone()
            case ContactKeys.EMAIL.value:
                self.get_email()
            case  ContactKeys.ADDRESS.value:
                self.get_address()
            case ContactKeys.BIRTHDAY.value:
                self.get_birthday()
            case _:
                raise InputError("Invalid param")

        return self.result


class RemoveBuilder(ContactBuilder):
    def build(self):
        self.get_name()
        return self.result


class FindBuilder(ContactBuilder):
    def build(self):
        find_criteria = self.what(
            "find criteria:", [ContactKeys.NAME.value, ContactKeys.PHONE.value, ContactKeys.EMAIL.value, ContactKeys.ADDRESS.value, ContactKeys.BIRTHDAY.value])
        match find_criteria:
            case ContactKeys.NAME.value:
                self.get_name()
            case ContactKeys.PHONE.value:
                self.get_phone()
            case ContactKeys.EMAIL.value:
                self.get_email()
            case ContactKeys.ADDRESS.value:
                self.get_address()
            case ContactKeys.BIRTHDAY.value:
                self.get_birthday()
            case _:
                raise InputError("Invalid input")
        return self.result


class ShowDetailsBuilder(ContactBuilder):
    def build(self):
        filter = self.what("filter criteria:", [
                           ContactKeys.PHONE.value, ContactKeys.EMAIL.value, ContactKeys.ADDRESS.value, ContactKeys.BIRTHDAY.value])
        self.get_name()
        match filter:
            case ContactKeys.PHONE.value:
                self.get_phone()
            case ContactKeys.EMAIL.value:
                self.get_email()
            case ContactKeys.ADDRESS.value:
                self.get_address()
            case ContactKeys.BIRTHDAY.value:
                self.get_birthday()
            case _:
                raise InputError("Invalid input")
        return self.result


class NoteBuilder(Builder):
    def get_id(self):
        self.get_property("id:", NoteKeys.ID.value)

    def get_title(self):
        self.get_property("title:", NoteKeys.TITLE.value)

    def get_text(self):
        self.get_property("text:", NoteKeys.TEXT.value)

    def get_tags(self):
        self.get_property("tags:", NoteKeys.TAGS.value)

    def get_tag(self):
        self.get_property("tag:", NoteKeys.TAG.value)


class AddNoteBuilder(NoteBuilder):
    def build(self):
        self.get_title()
        self.get_text()
        self.get_tags()
        return self.result


class ChangeNoteBuilder(NoteBuilder):
    def build(self):
        self.get_id()
        self.get_title()
        self.get_text()
        return self.result


class RemoveNoteBuilder(NoteBuilder):
    def build(self):
        self.get_id()
        return self.result


class AddTagBuilder(NoteBuilder):
    def build(self):
        self.get_id()
        self.get_tag()
        return self.result


class RemoveTagBuilder(NoteBuilder):
    def build(self):
        self.get_id()
        self.get_tag()
        return self.result


class FindNotesBuilder(NoteBuilder):
    def build(self):
        self.get_tags()
        return self.result


class CommandPrompt:
    def __init__(self):
        self.session = PromptSession(style=style)
        self.result = ()

    def get_builder(self, command):

        match command:
            case Command.ADD.value:
                return AddBuilder(self.session)
            case Command.CHANGE.value:
                return ChangeBuilder(self.session)
            case Command.REMOVE.value:
                return RemoveBuilder(self.session)
            case Command.FIND.value:
                return FindBuilder(self.session)
            case Command.SHOW_DETAILS.value:
                return ShowDetailsBuilder(self.session)
            case Command.ADD_NOTE.value:
                return AddNoteBuilder(self.session)
            case Command.REMOVE_NOTE.value:
                return RemoveNoteBuilder(self.session)
            case Command.CHANGE_NOTE.value:
                return ChangeNoteBuilder(self.session)
            case Command.FIND_NOTES.value:
                return FindNotesBuilder(self.session)
            case Command.ADD_TAGS.value:
                return AddTagBuilder(self.session)
            case Command.REMOVE_TAGS.value:
                return RemoveTagBuilder(self.session)
            case _:
                return Builder(self.session)

    def dump_prompt(self):
        self.session.prompt(
            "Press Enter to continue:")

    @error_handler
    def prompt(self):
        command_completer = FirstWordCompleter(
            [command.value for command in Command])

        cmd = self.session.prompt(
            "Enter command:", completer=command_completer)

        params = {}
        if cmd:
            cmd = cmd.strip().lower()
            builder = self.get_builder(cmd)
            params = builder.build()

        return (cmd, params)
