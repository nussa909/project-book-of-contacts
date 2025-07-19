from console_output import ConsoleOutput


class ValidationError(Exception):
    """
    Exception raised for validation errors.
    """
    pass


class PhoneNotFoundError(Exception):
    """
    Exception raised when a phone number is not found.
    """
    pass


class InputError(Exception):
    """
    Exception raised for invalid user input.
    """
    pass


def error_handler(func):
    """
    Decorator for handling exceptions and printing error messages to the console.

    :param func: Function to wrap with error handling.
    :return: Wrapped function with error handling.
    """
    def inner(*args, **kwargs):
        """
        Inner function that executes the wrapped function and handles exceptions.

        :param args: Positional arguments for the wrapped function.
        :param kwargs: Keyword arguments for the wrapped function.
        :return: Result of the wrapped function or None if an exception occurs.
        """
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
