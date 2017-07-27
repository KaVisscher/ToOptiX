class FESystem():

    def __init__(self):

        self.__type = None
        self.__file_path = None
        self.__weight_factor = 1.0

    def set_type(self, type):
        self.__type = type

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def get_type(self):
        return self.__type

    def get_file_path(self):
        return self.__file_path

    def set_weight_factor(self, weight_factor):
        self.__weight_factor = weight_factor

    def get_weight_factor(self):
        return self.__weight_factor


