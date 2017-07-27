class YoungModule():

    def __init__(self, young_module=None, temperature=None):

        self.__young_module = young_module
        self.__temperature = temperature

    def __str__(self):
        return_string = "YoungModule: " + str(self.__young_module) + \
            " Temperature: " + str(self.__temperature) + "\n"

        return return_string

    def set_young_module(self, young_module):
        self.__young_module = young_module

    def set_temperature(self,temperature):
        self.__temperature = temperature

    def get_temperature(self):
        return self.__temperature

    def get_young_module(self):
        return self.__young_module
