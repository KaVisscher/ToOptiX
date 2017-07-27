class ReadDAT():

    def __init__(self, filename=None):

        self.__filename = filename

    def set_filename(self, filename):
        self.__filename = filename

    def __remove_char_on_black_list(self, string):
        black_list = [" ", ",", "="]
        new_string = ""
        for char in string:
            if not char in black_list:
                new_string += char
        return new_string

    def __remove_empty_elements(self, list):
        new_list = []
        for elem in list:
            if elem == "":
                continue
            new_list.append(elem)
        return new_list


    def add_temperature(self, fem_object):
        i_file = open(self.__filename, "r")
        read_disp = False
        for line in i_file:
            if line[-1] == "\n":
                line = line[0:-1]
            # Coments and line does not exist
            if len(line) == 0:
                continue
            elif len(line) >= 2:
                if line[0:1] == "**":
                    continue

            if "TEMPERATURES" in line.upper():
                read_disp = True
                continue

            if read_disp:
                words = line.split(" ")
                words = self.__remove_empty_elements(words)
                node_id = int(words[0])
                fem_object.set_node_temperature(node_id, float(words[1]))

    def add_displacement(self, fem_object):
        i_file = open(self.__filename, "r")
        read_disp = False
        for line in i_file:
            if line[-1] == "\n":
                line = line[0:-1]
            # Coments and line does not exist
            if len(line) == 0:
                continue
            elif len(line) >= 2:
                if line[0:1] == "**":
                    continue

            if "DISPLACEMENTS" in line.upper():
                read_disp = True
                continue

            if read_disp:
                words = line.split(" ")
                words = self.__remove_empty_elements(words)
                node_id = int(words[0])
                fem_object.set_node_u1(node_id, float(words[1]))
                fem_object.set_node_u2(node_id, float(words[2]))
                fem_object.set_node_u3(node_id, float(words[3]))


    def add_energy_density(self, fem_object):
        i_file = open(self.__filename, "r")

        read_energy = False
        for line in i_file:
            if line[-1] == "\n":
                line = line[0:-1]
            # Coments and line does not exist
            if len(line) == 0:
                continue
            elif len(line) >= 2:
                if line[0:1] == "**":
                    continue

            if "INTERNAL ENERGY" in line.upper():
                read_energy = True
                continue

            if read_energy:
                words = line.split(" ")
                words = self.__remove_empty_elements(words)
                elem_id = int(words[0])
                fem_object.set_energy_density(elem_id, float(words[2]))


    def add_heat_flux(self, fem_object):
        i_file = open(self.__filename, "r")

        read_energy = False
        for line in i_file:
            if line[-1] == "\n":
                line = line[0:-1]
            # Coments and line does not exist
            if len(line) == 0:
                continue
            elif len(line) >= 2:
                if line[0:1] == "**":
                    continue

            if "HEAT FLUX" in line.upper():
                read_energy = True
                continue

            if read_energy:
                words = line.split(" ")
                words = self.__remove_empty_elements(words)
                elem_id = int(words[0])
                heat_flux = (float(words[2])**2 + float(words[3])**2 + float(words[4])**2) ** 0.5
                fem_object.set_heat_flux(elem_id, heat_flux)



