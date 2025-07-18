# PyContacts
![Logo_PyContacts](https://github.com/nussa909/project-book-of-contacts/images/Logo_PyContacts.png)
 PyContacts is a personal assistant for managing contacts and notes, developed as part of a team educational project within the Python Programming course.

# Features
The personal assistant is developed with a command-line interface. It saves data to disk, so it is not lost after a restart. The prompt_toolkit library is used for handling inputs and prompts, while rich is used to provide a user-friendly interface.

**The personal assistant can**

+ Save contacts with names, addresses, phone numbers, emails, and birthdays.

+ Show upcoming birthdays (e.g., within 7 days).

+ Validate names, addresses, Ukrainian phone numbers, emails during input.

+ Save, search (strict, non-strict), edit, and delete contacts.

+ Save, search notes by tags, edit, and delete notes.

+ Add "tags" to notes.


# Installation

PyContacts is tested for Python 3.13 and above.

 **Clone the repo**:
```git clone https://github.com/nussa909/project-book-of-contacts.git
cd project-book-of-contacts 
```
**Creating a virtual environment (optional)**:
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
**Installing dependencies**:
```pip3 install -r requirements.txt
```
**Run**:
```python3 ./src/main.py # Linux/macOS
python3 .\src\main.py # Windows
```

# Usage
Usage from command-line
pip installation enables PyContact's command-line utility. Type the following directly into your terminal:

**Add Contact**:
Enter command: add
name: Tom
phones: 380938744552, 380678744551
email Tom@gmail.com 
address: Ukraine, Kyiv, Some St 45 
birthday: 18.03.1990
Mandatory parameters:name, +1 parameter from the existing  (phones, email, address, birthday)

**Find Contact by any parameter**:
Enter command: find
find criteria: name
name: _any from the existing paramers (name, phones, email, address, birthday)_

**Change Contact by any parameter**:
Enter command: change
find criteria: phones
phones: _any from the existing paramers (name, phones, email, address, birthday)_

**Remove Contact by name**:
remove -name Joe Dow

**Show all Contacts**:
-all

**Add Note**:
add_note -text Note message -tags #tag1,#tag2

**Edit Note**:
change_note -id note_id -old old message -new new message

**Remove Note**:
remove_note -id note_id

**Add Tag to Note**:
add_tag -id note_id -tag #tag

**Remove Tag from Note**:
remove_tag -id note_id -tag #tag

**Find Note by Tag**:
find_notes -tag #tag

**Show Notes sorted by Tag**:
show_notes -sort #tag


> "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.
> And the only way to do great work is to love what you do.
> If you haven't found it yet, keep looking. Don't settle.
> As with all matters of the heart, you'll know when you find it."
> — _Steve Jobs, Stanford University, 2005_


