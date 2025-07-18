from console_output import ConsoleOutput


class ValidationError(Exception):
    pass


class PhoneNotFoundError(Exception):
    pass


class InputError(Exception):
    pass


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            ConsoleOutput().print_error(f"Validation error!: {err}")
        except PhoneNotFoundError as err:
            ConsoleOutput().print_error(f"Phone not found!: {err}")
        except InputError as err:
            ConsoleOutput().print_error(f"Input error!: {err}")
        except KeyError as err:
            ConsoleOutput().print_error(f"Error!: {err}")
        except ValueError as err:
            ConsoleOutput().print_error(f"Error!: {err}")
        except Exception as err:
            ConsoleOutput().print_error(f"Error: {err}")
    return inner
