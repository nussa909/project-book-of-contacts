
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
            print(f"ValidationError: {err}")
        except PhoneNotFoundError as err:
            print(f"PhoneNotFoundError: {err}")
        except InputError as err:
            print(f"InputError: {err}")
        except KeyError as err:
            print(f"KeyError: {err}")
        except ValueError as err:
            print(f"ValueError: {err}")
        except Exception as err:
            print(f"Exception: {err}")
    return inner
