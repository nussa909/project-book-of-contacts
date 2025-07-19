import pickle


class SerializedObject:
    """
    Class for serializing and deserializing objects to and from a file using pickle.
    """

    def __init__(self, filename, object):
        """
        Initialize the SerializedObject with a filename and an object.

        :param filename: Name of the file to store the serialized object.
        :param object: The object to serialize if no data is loaded from file.
        """
        self.__filename = filename  # Name of the file for serialization
        loaded_obj = self.load_data()
        self.object = loaded_obj if loaded_obj != None else object  # The object being managed

    def save_data(self):
        """
        Save the current object to the file using pickle.
        """
        with open(self.__filename, "wb") as f:
            pickle.dump(self.object, f)

    def load_data(self):
        """
        Load and return the object from the file using pickle.

        :return: The loaded object, or None if the file does not exist.
        """
        try:
            with open(self.__filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("File not found")
            return None
