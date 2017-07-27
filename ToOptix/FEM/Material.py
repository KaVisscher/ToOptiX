class Material():

    def __init__(self, name):

        self.__name = name
        self.__young_module = []
        self.__poisson_ratio = []
        self.__conductivity = []

    def __str__(self):
        return_string = "material: " + str(self.__name) + "\n"

        for young_module in self.__young_module:
            return_string += young_module.__str__()
        for poisson_ratio in self.__poisson_ratio:
            return_string += poisson_ratio.__str__()
        for conductivity in self.__conductivity:
            return_string += conductivity.__str__()

        return return_string

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_young_module(self, young_module):
        if not isinstance(young_module, list):
            self.__young_module = [young_module]
        else:
            self.__young_module = young_module

    def set_poisson_ratio(self, poisson_ratio):
        if not isinstance(poisson_ratio , list):
            self.__poisson_ratio  = [poisson_ratio ]
        else:
            self.__poisson_ratio = poisson_ratio

    def set_conductivity(self, conductivity):
        if not isinstance(conductivity, list):
            self.__young_module = [conductivity]
        else:
            self.__conductivity = conductivity

    def add_young_module(self, young_module):
        self.__young_module.append(young_module)

    def add_poisson_ratio(self, poisson_ratio):
        self.__poisson_ratio.append(poisson_ratio)

    def add_conductivity(self, conductivity):
        self.__conductivity.append(conductivity)

    def get_young_module(self):
        return self.__young_module

    def get_poisson_ratio(self):
        return self.__poisson_ratio

    def get_conductivity(self):
        return self.__conductivity
