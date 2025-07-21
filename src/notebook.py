
from collections import UserList
import re


class Note:
    """
    Represents a note in a notebook.

    Attributes:
        id (int): Unique identifier for the note.
        title (str): Title of the note.
        text (str): Text content of the note.
        tags (set): Set of tags associated with the note.
    """
    current_id = 0

    @staticmethod
    def sort_by_title(note: "Note") -> str:
        '''
        Sort notes by their title in lowercase.

        Args:
            note (Note): The note to sort by title.
        Returns:
            str: The title of the note in lowercase.
        '''
        return (note.title.lower())

    def __init__(self, title: str, text: str, tags={}):
        self.id = Note.__get_next_id()
        self.title = title.capitalize()
        self.text = text.capitalize()
        self.tags = {tag.lower() for tag in tags}

    def add_tag(self, tag: str):
        '''
        Add a tag to the note.
        This method adds a tag to the note's set of tags if it is not already present.

        Args:
            tag (str): The tag to add to the note.
        '''
        if not tag in self.tags:
            self.tags.add(tag.lower())

    def remove_tag(self, tag: str):
        '''
        Remove a tag from the note.
        This method removes a tag from the note's set of tags if it exists.

        Args:
            tag (str): The tag to remove from the note.
        '''
        res = False
        if tag in self.tags:
            self.tags.remove(tag)
            res = True

        return res

    @classmethod
    def __get_next_id(cls):
        '''
        Get the next unique ID for a note.
        This class method increments the current ID and returns it.
        Returns:
            int: The next unique ID for a note.
        '''
        cls.current_id += 1
        return cls.current_id

    def __lt__(self, other):
        '''
        Compare two notes based on their IDs.
        This method is used to compare notes when sorting or ordering them.
        Args:
            other (Note): The other note to compare with.
        Returns:
            bool: True if this note's ID is less than the other note's ID, otherwise False.
        '''
        return self.id < other.id

    def __str__(self):
        '''
        String representation of the note.
        This method returns a formatted string that includes the note's ID, header, tags, and text.
        Returns:
            str: A formatted string representation of the note.
        '''
        return f"#{self.id}:{self.title}\ntags:{list(self.tags)}\n{self.text}"

    def __repr__(self):
        '''
        Representation of the note for debugging.
        This method returns a formatted string that includes the note's ID, header, tags, and text.
        Returns:
            str: A formatted string representation of the note for debugging.
        '''
        return f"\n#{self.id}:{self.title}\ntags:{list(self.tags)}\n{self.text}"


class Notebook(UserList):
    ''' 
    A class representing a collection of notes.
    This class extends UserList to provide a list-like interface for managing notes.
    It allows adding, removing, and searching for notes by tags or ID.
    Attributes:
        data (list): A list of Note objects representing the notes in the notebook.
    '''
    def add_note(self, note: Note):
        '''
        Add a note to the notebook.
        This method appends a Note object to the notebook's data list.
        '''
        self.data.append(note)

    def remove_note(self, note: Note):
        '''
        Remove a note from the notebook.
        This method removes a Note object from the notebook's data list.
        '''
        self.data.remove(note)

    def find_note_by_tags(self, tags):
        '''
        Find notes in the notebook by their tags.
        This method returns a list of Note objects that have at least one tag in common with the given tags.

        Args:
            tags (set): A set of tags to search for.

        Returns:
            list: A list of Note objects that match the given tags.
        '''
        tags = set(tags)
        return [note for note in self.data if tags & note.tags]

    def find_note_by_id(self, id: int):
        '''
        Find a note in the notebook by its ID.
        This method returns the Note object with the given ID, or None if not found.

        Args:
            id (int): The ID of the note to find.

        Returns:
            Note: The Note object with the given ID, or None if not found.
        '''
        for note in self.data:
            if note.id == id:
                return note


    def find_note(self, query: str, field_type: str) -> list[Note]:
        """
        Find notes by a query string in a specified field (title or text).
        Supports SQL-like wildcards: % for any sequence, _ for any single character.

        Args:
            query (str): The search query, may contain wildcards.
            field_type (str): The field to search ('title' or 'text').

        Returns:
            list[Note]: List of matching Note objects.
        """
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
        '''
        Get all notes in the notebook.
        This method returns a list of all Note objects in the notebook.

        Returns:
            list: A list of all Note objects in the notebook.
        '''
        return [note for note in sorted(self.data)]

    def __setstate__(self, state):
        '''
        Restore the notebook's state from a saved state.
        This method updates the notebook's attributes with the given state.
        Args:
            state (dict): A dictionary containing the saved state of the notebook.
        '''
        self.__dict__.update(state)
        if self.data:
            Note.current_id = max(note.id for note in self.data)

    def __str__(self):
        '''
        String representation of the notebook. 
        This method returns a formatted string that includes all notes in the notebook.
        
        Returns:
            str: A formatted string representation of the notebook.
        '''
        return f"Notebook:\n{"\n".join(str(note) for note in self.data)}"
