from rich.console import Console
from rich.table import Table
from rich.text import Text


class ConsoleOutput:
    """
    Singleton class for handling console output using Rich library.
    Provides methods for printing tables, messages, errors, and clearing the console.
    """
    __instance = None

    def __new__(cls):
        """
        Create or return the singleton instance of ConsoleOutput.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """
        Initialize the ConsoleOutput instance with a Rich Console object.
        """
        self.__console = Console()

    def __print_str(self, msg, style):
        """
        Print a styled string message to the console.

        :param msg: Message to print.
        :param style: Rich style string for formatting.
        """
        text = Text()
        text.append(msg, style=style)
        self.__console.print(text)

    def print_map(self, titles, map: dict):
        """
        Print a dictionary as a two-column table.

        :param titles: Tuple containing column titles (title1, title2).
        :param map: Dictionary to display.
        """
        table = Table()
        if map:
            title1, title2 = titles
            table.add_column(title1, style="blue",
                             justify="right", no_wrap=True)
            table.add_column(title2, style="green", no_wrap=True)

            for key, value in map.items():
                table.add_row(str(key), str(value))

            self.__console.print(table)
        else:
            self.__print_str(
                "No items to display", style="bold blue")

    def print_object_list(self, data: list):
        """
        Print a list of objects as a table, using their __dict__ attributes.

        :param data: List of objects to display.
        """
        table = Table(show_lines=True)
        if data:
            data_dct = [dt.__dict__ for dt in data]
            for column_name in data_dct[0].keys():
                table.add_column(column_name.title(), justify="left",
                                 style="blue", no_wrap=True)

            for row in data_dct:
                args = [str(item) for item in row.values()]
                table.add_row(*args)

            self.__console.print(table)
        else:
            self.__print_str(
                "No items to display", style="bold blue")

    def print_msg(self, msg):
        """
        Print a success or informational message in green.

        :param msg: Message to print.
        """
        self.__print_str(msg, style="bold green")

    def print_error(self, msg):
        """
        Print an error message in red.

        :param msg: Error message to print.
        """
        self.__print_str(msg, style="bold red")

    def clear(self):
        """
        Clear the console screen.
        """
        self.__console.clear()

    def print_map_with_title(self, title: str, data: dict):
        """
        Print a dictionary as a table with a title.

        :param title: Title of the table.
        :param data: Dictionary with data to print.
        """
        table = Table(title=title, show_header=False)
        table.add_column("Field", style="blue", no_wrap=True)
        table.add_column("Value", style="green", no_wrap=True)

        for key, value in data.items():
            table.add_row(str(key), str(value))

        self.__console.print(table)
