
class SolidSection:

    def __init__(self, material=None, elset=None):

        self.__material = material
        self.__elset = elset

    def get_material(self):
        return self.__material

    def get_elset(self):
        return self.__elset

    def set_material(self, material):
        self.__material = material

    def set_elset(self, elset):
        self.__elset = elset