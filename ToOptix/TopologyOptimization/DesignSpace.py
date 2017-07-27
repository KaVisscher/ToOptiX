class DesignSpace():

    def __init__(self):

        self.__elements = []


    def set_elements(self, elements):
        self.__elements = elements

    def get_all_elements(self):
        return self.__elements

    def remove_elements_from_file(self, filename):

        element_remove_list = []

        i_file = open(filename, "r")
        for line in i_file:
            line = line[0:-1]
            # Coments and line does not exist
            if len(line) == 0:
                continue
            elif len(line) >= 2:
                if line[0:1] =="**":
                    continue
            words = line.split(", ")
            for word in words:
                if word.isdigit():
                    element_remove_list.append(int(word))

        new_design_space = []
        for element in self.__elements:
            if element.get_id() in element_remove_list:
                continue
            else:
                new_design_space.append(element)
        self.__elements = new_design_space
