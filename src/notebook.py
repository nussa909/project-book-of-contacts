
from collections import UserList
import re


class Note:
    current_id = 0

    @staticmethod
    def sort_by_title(note):
        return (note.title.lower())

    def __init__(self, title: str, text: str, tags={}):
        self.id = Note.__get_next_id()
        self.title = title.capitalize()
        self.text = text.capitalize()
        self.tags = {tag.lower() for tag in tags}

    def add_tag(self, tag):
        if not tag in self.tags:
            self.tags.add(tag.lower())

    def remove_tag(self, tag):
        res = False
        if tag in self.tags:
            self.tags.remove(tag)
            res = True

        return res

    @classmethod
    def __get_next_id(cls):
        cls.current_id += 1
        return cls.current_id

    def __lt__(self, other):
        return self.id < other.id

    def __str__(self):
        return f"#{self.id}:{self.title}\ntags:{list(self.tags)}\n{self.text}"

    def __repr__(self):
        return f"\n#{self.id}:{self.title}\ntags:{list(self.tags)}\n{self.text}"


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

    def find_note(self, query: str, field_type: str) -> list[Note]:

        def like(pattern: str, text: str) -> bool:
            regex = '^' + re.escape(pattern).replace('%',
                                                     '.*').replace('_', '.') + '$'
            return re.match(regex, text) is not None

        matching_records = []
        search_value = query.lower()

        if field_type not in ['title', 'text']:
            return matching_records

        for note in self.data:
            field_value = None

            if field_type == 'title' and note.title:
                field_value = note.title
            elif field_type == 'text' and note.text:
                field_value = note.text

            if field_value:
                if like(search_value, field_value.lower()):
                    matching_records.append(note)

        return matching_records

    def get_notes(self):
        return [note for note in sorted(self.data)]

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.data:
            Note.current_id = max(note.id for note in self.data)

    def __str__(self):
        return f"Notebook:\n{"\n".join(str(note) for note in self.data)}"
