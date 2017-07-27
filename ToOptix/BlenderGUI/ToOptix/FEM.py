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




class Element():

    def __init__(self, id, nodes=None):

        self.__id = id
        self.__x_center = 0.0
        self.__y_center = 0.0
        self.__z_center = 0.0
        self.__node = None
        self.__compaction = 1.0
        self.__energy_density = None
        self.__heat_flux = None
        self.set_nodes(nodes)



    def __str__(self):
        return_string = "elem id: " + str(self.__id) + "\n"
        for node in self.__node:
            return_string += node.__str__()
        return return_string

    def set_id(self, id):
        self.__id = id

    def __calculate_element_center(self):
        count = 0
        x_center = 0.0
        y_center = 0.0
        z_center = 0.0
        for node in self.__node:
            count += 1
            x_center += node.get_x()
            y_center += node.get_y()
            z_center += node.get_z()
        self.__x_center = x_center / count
        self.__y_center = y_center / count
        self.__z_center = z_center / count

    def set_nodes(self, nodes):
        self.__node = nodes
        self.__calculate_element_center()




    def get_nodes(self):
        return self.__node

    def get_id(self):
        return self.__id

    def get_compaction(self):
        return self.__compaction

    def set_compaction(self, compaction):
        self.__compaction = compaction

    def get_energy_density(self):
        return self.__energy_density

    def set_energy_density(self, energy_density):
        self.__energy_density = energy_density

    def set_heat_flux(self, heat_flux):
        self.__heat_flux = heat_flux

    def get_heat_flux(self):
        return self.__heat_flux

    def get_x_center(self):
        return self.__x_center

    def get_y_center(self):
        return self.__y_center

    def get_z_center(self):
        return self.__z_center

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


class Node(object):

    def __init__(self, id, x=None, y=None, z=None):

        self.__id = id
        self.__x = x
        self.__y = y
        self.__z = z
        self.__u1 = None
        self.__u2 = None
        self.__u3 = None
        self.__temperature = None

    def __str__(self):
        return "node id: " + str(self.__id) + " x: " + str(self.__x) + \
                " y: " + str(self.__y) +  " z: " + str(self.__z) + "\n"

    def set_id(self, id):
        self.__id = id

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_z(self, z):
        self.__z = z

    def get_id(self):
        return self.__id

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z

    def get_u1(self):
        return self.__u1

    def get_u2(self):
        return self.__u2

    def get_u3(self):
        return self.__u3

    def set_u1(self, u1):
        self.__u1 = u1

    def set_u2(self, u2):
        self.__u2 = u2

    def set_u3(self, u3):
        self.__u3 = u3

    def set_temperature(self, temperature):
        self.__temperature = temperature
    def get_temperature(self):
        return self.__temperature


class PoissonRatio():

    def __init__(self, poisson_ratio=None, temperature=None):

        self.__poisson_ratio = poisson_ratio
        self.__temperature = temperature

    def __str__(self):
        return "PoissonRatio: " + str(self.__poisson_ratio) + \
            " Temperature: " + str(self.__temperature) + "\n"

    def set_poisson_ratio(self, poisson_ratio):
        self.__poisson_ratio = poisson_ratio

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def get_temperature(self):
        return self.__temperature

    def get_poisson_ratio(self):
        return self.__poisson_ratio



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

