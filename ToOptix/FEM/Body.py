class Body():

    def __init__(self, id, node_dictonary=None, element_dictonary=None, solid_sections=None):

        self.__id = id
        self.__node = node_dictonary
        self.__element = element_dictonary
        self.__solid_sections = solid_sections


    def __str__(self):
        return_string = "body id: " + str(self.__id) + "\n"
        for key in self.__element:
            return_string += self.__element[key].__str__()
        return return_string

    def set_solid_sections(self, solid_sections):
        self.__solid_sections = solid_sections

    def get_solid_sections(self):
        return self.__solid_sections

    def __add_nodes(self, element):
        for node in element.get_nodes():
            self.__node[node.get_id] = node

    def set_id(self, id):
        self.__id = id

    def set_elements(self, elements):
        self.__element = {}
        for element in elements:
            self.__element[element.get_id()] = element

    def get_id(self):
        return self.__id

    def get_node(self, id):
        return self.__node[id]

    def get_element(self, id):
        return self.__element[id]

    def get_all_nodes(self):
        nodes = []
        for key in self.__node:
            nodes.append(self.__node[key])
        return nodes

    def set_node_u1(self, id, u1):
        self.__node[id].set_u1(u1)

    def set_node_u2(self, id, u2):
        self.__node[id].set_u2(u2)

    def set_node_temperature(self, id, temperature):
        self.__node[id].set_temperature(temperature)


    def set_node_u3(self, id, u3):
        self.__node[id].set_u3(u3)

    def set_energy_density(self, id, energy):
        self.__element[id].set_energy_density(energy)

    def set_heat_flux(self, id, heat_flux):
        self.__element[id].set_heat_flux(heat_flux)

    def get_all_elements(self):
        elements = []
        for key in self.__element:
            elements.append(self.__element[key])
        return elements
