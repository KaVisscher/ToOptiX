class ElementSet():

    def __init__(self, name=None, elements=set()):

        self.__name = name
        self.__element = elements

    def get_name(self):
        return self.__name

    def get_elements(self):
        return self.__element

    def set_name(self, name):
        self.__name = name

    def set_elements(self, elements):
        self.__element = elements


    def add_element(self, element):
        self.__element.add(element)
