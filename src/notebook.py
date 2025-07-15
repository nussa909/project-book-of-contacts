
from collections import UserList

class Note:
    def __init__(self, header:str, text:str, tags = {}):
        self.header = header
        self.text = text
        self.tags = tags

    def is_tag_added(self, tag):
        return tag in self.tags

    def add_tag(self, tag):
        if not self.is_tag_added(tag):
            self.tags.append(tag)

    def remove_tag(self, tag):
        if self.is_tag_added(tag):
            self.tags.remove(tag)

    def __str__(self):
        return f"{self.header}\ntags:{self.tags}\n{self.text}"
    
    def __repr__(self):
        return f"{self.header}"


class Notebook(UserList):

    def add_note(self, note:Note):
        pass        

    def edit_note(self, note:Note):
        pass

    def remove_note(self, note:Note):
        pass

    def find_note_by_tags(self, tags:str):
        pass
    