
from collections import UserList


class Note:
    current_id = 0

    @staticmethod
    def sort_by_title(note):
        return (note.header.lower())

    def __init__(self, header: str, text: str, tags={}):
        self.id = Note.__get_next_id()
        self.header = header
        self.text = text
        self.tags = set(tags)

    def add_tag(self, tag):
        if not tag in self.tags:
            self.tags.add(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    @classmethod
    def __get_next_id(cls):
        cls.current_id += 1
        return cls.current_id

    def __str__(self):
        return f"#{self.id}:{self.header}\ntags:{list(self.tags)}\n{self.text}"

    def __repr__(self):
        return f"#{self.id}:{self.header}"


class Notebook(UserList):

    def add_note(self, note: Note):
        self.data.append(note)

    def remove_note(self, note: Note):
        self.data.remove(note)

    def find_note_by_tags(self, tags):
        tags = set(tags)
        return [note for note in self.data if tags & note.tags]

    def find_note_by_id(self, id: int):
        for note in self.data:
            if note.id == id:
                return note

    def get_notes(self):
        return self.data

    def __str__(self):
        return f"Notebook:\n{"\n".join(str(note) for note in self.data)}"

# note = Note("Покупки", "Купити молоко та яйця",{"important"})
# note.add_tag("buy")
# print(note)

# # note.remove_tag("important")
# print(note)

# note2 = Note("email password", "email: my_email@gmail.com, pass:1234")
# note2.add_tag("important")

# notebook = Notebook()
# notebook.add_note(note)
# notebook.add_note(note2)

# print(notebook)

# print(notebook.find_note_by_tags(["buy","none"]))
# print(notebook.find_note_by_tags(["important"]))
# print(notebook.find_note_by_tags(["high"]))
