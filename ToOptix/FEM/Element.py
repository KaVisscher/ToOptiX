

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
