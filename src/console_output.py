from rich.console import Console
from rich.table import Table
from rich.text import Text


class ConsoleOutput:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__console = Console()

    def __print_str(self, msg, style):
        text = Text()
        text.append(msg, style=style)
        self.__console.print(text)

    def print_map(self, titles, map: dict):
        table = Table()

        title1, title2 = titles
        table.add_column(title1, style="blue",
                         justify="right", no_wrap=True)
        table.add_column(title2, style="green", no_wrap=True)

        for key, value in map.items():
            table.add_row(str(key), str(value))

        self.__console.print(table)

    def print_object_list(self, data: list):
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

    def print_msg(self, msg):
        self.__print_str(msg, style="bold green")

    def print_error(self, msg):
        self.__print_str(msg, style="bold red")

    def clear(self):
        self.__console.clear()