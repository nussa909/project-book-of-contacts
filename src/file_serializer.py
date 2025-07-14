import pickle


class SerializedObject:
    def __init__(self, filename, object):
        self.__filename = filename
        loaded_obj = self.load_data()
        self.object = loaded_obj if loaded_obj != None else object

    def save_data(self):
        with open(self.__filename, "wb") as f:
            pickle.dump(self.object, f)

    def load_data(self):
        try:
            with open(self.__filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("File not found")
            return None