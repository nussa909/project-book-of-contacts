import pickle

class SerializedObject:
    ''' A class for serializing and deserializing an object to/from a file using pickle.
    This class provides methods to save an object to a file and load it back.
    Attributes:
        __filename (str): The name of the file to save/load the object.
        object (object): The object to be serialized/deserialized.
    '''
    def __init__(self, filename, object):
        '''
        Initialize the SerializedObject with a filename and an object.
        If the file exists, it loads the object from the file; otherwise, it uses the provided object.
        Args:
            filename (str): The name of the file to save/load the object.
            object (object): The object to be serialized/deserialized.
        ''' 
        self.__filename = filename
        loaded_obj = self.load_data()
        self.object = loaded_obj if loaded_obj != None else object

    def save_data(self):
        '''
        Save the object to a file using pickle. 
        This method opens the file in binary write mode and dumps the object into it.
        Raises:
            IOError: If there is an error writing to the file.
        '''
        with open(self.__filename, "wb") as f:
            pickle.dump(self.object, f)

    def load_data(self):
        '''
        Load the object from a file using pickle.
        This method opens the file in binary read mode and loads the object from it.
        Returns:
            object: The loaded object, or None if the file does not exist.
        '''
        try:
            with open(self.__filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("File not found")
            return None
