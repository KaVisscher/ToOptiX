class Conductivity():

    def __init__(self, conductivity=None, temperature=None):

        self.__conductivity = conductivity
        self.__temperature = temperature

    def __str__(self):
        return_string = "Conductivity: " + str(self.__conductivity) + \
            " Temperature: " + str(self.__temperature) + "\n"

        return return_string

    def set_conductivity (self, young_module):
        self.__conductivity = young_module

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def get_temperature(self):
        return self.__temperature

    def get_conductivity (self):
        return self.__conductivity
