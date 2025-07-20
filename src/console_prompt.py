from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, DummyCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from enum import Enum
from exceptions import InputError

command_descriptions = {
    "help":        "Show commands description",
    "add":         "Add new contact",
    "change":      "Edit contact",
    "remove":      "Remove the contact",
    "find":        "Find contact by selected criteria (use % and _ as wildcards)",
    "show":        "Show detailed contact info",
    "all":         "Display all contacts/notes(contacts by default)",
    "birthdays":   "Show upcoming birthdays next input days (default 7)",
    "add_note":    "Add new note",
    "remove_note": "Remove dedicated note",
    "change_note": "Edit dedicated note",
    "find_notes":  "Find notes by selected criteria",
    "add_tags":    "Add tag to selected note",
    "remove_tags": "Remove tag from selected note",
    "show_notes":  "Display notes sorted by tags",
    "exit":        "Exit the application",
    "close":       "Exit the application",
}

class Command(Enum):
    """
    Enum representing available commands for the contact and note management system.
    """
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
    """
    Enum representing keys for contact properties.
    """
    NAME = "name"           # Contact's name
    PHONE = "phone"         # Contact's phone number(s)
    EMAIL = "email"         # Contact's email address
    ADDRESS = "address"     # Contact's physical address
    BIRTHDAY = "birthday"   # Contact's birthday
    OLD_PHONE = "old_phone"  # Old phone number for change operations
    NEW_PHONE = "new_phone"  # New phone number for change operations
    DAYS = "days"           # Number of days for birthday search


class NoteKeys(Enum):
    """
    Enum representing keys for note properties.
    """
    ID = "id"       # Note identifier
    TITLE = "title"  # Note title
    TEXT = "text"   # Note text content
    TAGS = "tags"   # Tags associated with the note
    TAG = "tag"     # Single tag for add/remove operations


class FirstWordCompleter(Completer):
    """
    Custom completer that suggests completions for the first word in the prompt.
    """

    def __init__(self, words: list, command_descr: dict = None):
        """
        Initialize with a list of words for completion.
        :param words: List of words to complete.
        """
        self.words = words
        self.command_descr = command_descr or {}

    def get_completions(self, document, complete_event):
        """
        Yield possible completions for the first word.
        :param document: The prompt_toolkit document object.
        :param complete_event: The completion event.
        """
        if ' ' in document.text_before_cursor:
            return

        current_word = document.get_word_before_cursor()
        for word in self.words:
            if word.startswith(current_word):
                yield Completion(word, start_position=-len(current_word),  display_meta=self.command_descr.get(word, ""))


style = Style.from_dict({
    "prompt": "#884444",
    "command": "#00aa00",
    "params": "#0003aa",
    'completion-menu.completion.current': 'bold underline fg:white bg:ansiblue',
    'completion-menu.meta.completion.current': 'italic fg:white bg:ansiblue'
})


class Builder:
    """
    Base builder class for collecting user input properties.
    """

    def __init__(self, session):
        """
        Initialize with a prompt session.
        :param session: PromptSession object.
        """
        self.session = session
        self.result = {}

    def prompt(self, prompt):
        """
        Prompt the user for input.
        :param prompt: Prompt text.
        :return: User input or None.
        """
        val = self.session.prompt(prompt, completer=DummyCompleter())
        return val if val.strip() else None

    def get_property(self, prompt, key):
        """
        Get a property value from the user and store it in the result.
        :param prompt: Prompt text.
        :param key: Key to store the value under.
        """
        colored_prompt = FormattedText([("class:params", prompt)])
        value = self.prompt(colored_prompt)
        if value:
            value = value.strip()
            self.result.update({key: value})

    def what(self, prompt, completer_list):
        """
        Prompt the user to select a property from a list.
        :param prompt: Prompt text.
        :param completer_list: List of options for completion.
        :return: Selected property.
        """
        completer = FirstWordCompleter(completer_list)
        property = self.session.prompt(
            prompt, completer=completer)
        property = property.strip()
        return property

    def build(self):
        """
        Return the collected result dictionary.
        :return: Dictionary of collected properties.
        """
        return self.result


class ContactBuilder(Builder):
    """
    Builder for collecting contact properties.
    """

    def get_name(self):
        """Prompt for contact name."""
        self.get_property("name:", ContactKeys.NAME.value)

    def get_phone(self):
        """Prompt for contact phone(s)."""
        self.get_property("phones:", ContactKeys.PHONE.value)

    def get_email(self):
        """Prompt for contact email."""
        self.get_property("email:", ContactKeys.EMAIL.value)

    def get_address(self):
        """Prompt for contact address."""
        self.get_property("address:", ContactKeys.ADDRESS.value)

    def get_birthday(self):
        """Prompt for contact birthday."""
        self.get_property("birthday:", ContactKeys.BIRTHDAY.value)

    def get_days(self):
        """Prompt for number of days for birthday search."""
        self.get_property("days:", ContactKeys.DAYS.value)


class AddBuilder(ContactBuilder):
    """
    Builder for adding a new contact.
    """

    def build(self):
        """Collect all properties for a new contact."""
        self.get_name()
        self.get_phone()
        self.get_email()
        self.get_address()
        self.get_birthday()
        return self.result


class ChangeBuilder(ContactBuilder):
    """
    Builder for changing contact properties.
    """

    def old_phone(self):
        """Prompt for old phone number."""
        self.get_property("old phone:", ContactKeys.OLD_PHONE.value)

    def new_phone(self):
        """Prompt for new phone number."""
        self.get_property("new phone:", ContactKeys.NEW_PHONE.value)

    def build(self):
        """
        Collect properties for changing a contact.
        Prompts for the property to change and its new value.
        """
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
    """
    Builder for removing a contact.
    """

    def build(self):
        """Collect name for contact removal."""
        self.get_name()
        return self.result


class FindBuilder(ContactBuilder):
    """
    Builder for finding contacts by criteria.
    """

    def build(self):
        """
        Prompt for find criteria and collect corresponding property.
        """
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


class BirthdaysBuilder(ContactBuilder):
    """
    Builder for searching contacts by upcoming birthdays.
    """

    def build(self):
        """Prompt for number of days to search for birthdays."""
        self.get_days()
        return self.result


class ShowDetailsBuilder(ContactBuilder):
    """
    Builder for showing contact details with filter criteria.
    """

    def build(self):
        """
        Prompt for filter criteria and contact name.
        """
        filter = self.what("filter criteria:", [
                           ContactKeys.PHONE.value, ContactKeys.EMAIL.value, ContactKeys.ADDRESS.value, ContactKeys.BIRTHDAY.value])
        self.get_name()
        self.result.update({'filter': filter})
        return self.result


class NoteBuilder(Builder):
    """
    Builder for collecting note properties.
    """

    def get_id(self):
        """Prompt for note ID."""
        self.get_property("id:", NoteKeys.ID.value)

    def get_title(self):
        """Prompt for note title."""
        self.get_property("title:", NoteKeys.TITLE.value)

    def get_text(self):
        """Prompt for note text."""
        self.get_property("text:", NoteKeys.TEXT.value)

    def get_tags(self):
        """Prompt for note tags."""
        self.get_property("tags:", NoteKeys.TAGS.value)

    def get_tag(self):
        """Prompt for a single tag."""
        self.get_property("tag:", NoteKeys.TAG.value)


class AllBuilder(Builder):
    """
    Builder for selecting between contacts and notes.
    """

    def build(self):
        """Prompt for 'contacts' or 'notes' selection."""
        property = self.what("contacts or notes:", ["contacts", "notes"])
        if property:
            property = property.strip()
            self.result.update({property: None})
        return self.result


class AddNoteBuilder(NoteBuilder):
    """
    Builder for adding a new note.
    """

    def build(self):
        """Collect all properties for a new note."""
        self.get_title()
        self.get_text()
        self.get_tags()
        return self.result


class ChangeNoteBuilder(NoteBuilder):
    """
    Builder for changing note properties.
    """

    def build(self):
        """Collect properties for changing a note."""
        self.get_id()
        self.get_title()
        self.get_text()
        return self.result


class RemoveNoteBuilder(NoteBuilder):
    """
    Builder for removing a note.
    """

    def build(self):
        """Collect note ID for removal."""
        self.get_id()
        return self.result


class AddTagBuilder(NoteBuilder):
    """
    Builder for adding a tag to a note.
    """

    def build(self):
        """Collect note ID and tag to add."""
        self.get_id()
        self.get_tag()
        return self.result


class RemoveTagBuilder(NoteBuilder):
    """
    Builder for removing a tag from a note.
    """

    def build(self):
        """Collect note ID and tag to remove."""
        self.get_id()
        self.get_tag()
        return self.result


class FindNotesBuilder(NoteBuilder):
    """
    Builder for finding notes by tags.
    """

    def build(self):
        """Prompt for tags to search notes."""
        self.get_tags()
        return self.result


class CommandPrompt:
    """
    Main class for prompting user commands and parameters.
    """

    def __init__(self):
        """
        Initialize the command prompt with history and style.
        """
        history = FileHistory('command_history.txt')
        self.session = PromptSession(style=style, history=history)
        self.result = ()

    def get_builder(self, command):
        """
        Get the appropriate builder for the given command.
        :param command: Command string.
        :return: Builder instance.
        """
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
            case Command.BIRTHDAYS.value:
                return BirthdaysBuilder(self.session)
            case Command.ALL.value:
                return AllBuilder(self.session)
            case _:
                return Builder(self.session)

    def prompt(self):
        """
        Prompt the user for a command and its parameters.
        :return: Tuple of command and parameters dictionary.
        """
        command_completer = FirstWordCompleter(
            [command.value for command in Command], command_descriptions)
        
        kb = KeyBindings()
        @kb.add('enter')
        def _(event):
            buf = event.current_buffer
            # check if the buffer is not empty
            if not buf.text.strip(): 
                event.app.exit(result=buf.text)
                return 
            if buf.complete_state and buf.complete_state.current_completion:
                buf.apply_completion(buf.complete_state.current_completion)
                event.app.exit(result=buf.text)     
            else:
                buf.complete_next()
                event.app.exit(result=buf.text)

        cmd = self.session.prompt(
            "Enter command:", completer=command_completer, key_bindings=kb,complete_while_typing=True)

        params = {}
        if cmd:
            cmd = cmd.strip().lower()
            builder = self.get_builder(cmd)
            params = builder.build()

        return (cmd, params)
