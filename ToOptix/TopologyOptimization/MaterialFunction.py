import copy
import FEM


class MaterialFunction:

    def __init__(self, material=None, elements=None):

        self.__material = material
        self.__element = elements
        self.__steps = 20
        self.__exponent = 3.0
        self.__sets = None

    def set_material_steps(self, steps):
        self.__steps = steps

    def get_material_steps(self):
        return self.__steps

    def set_exponent(self, exponent):
        self.__exponent = exponent

    def get_exponent(self):
        return self.__exponent

    def __get_element_sets_according_to_compaction(self):
        all_set = [set()]
        for x in range(self.__steps - 1):
            all_set.append(set())
        for element in self.__element:
            if int(self.__steps * element.get_compaction()) - 1 < 0:
                set_num = 0
            else:
                set_num = int(self.__steps * element.get_compaction()) - 1
            all_set[set_num].add(element)
        self.__sets = all_set


    def get_solid_section(self):

        self.__get_element_sets_according_to_compaction()
        solid_sections = []
        for mat_numb in range(self.__steps):
            if not len(self.__sets[mat_numb]) == 0:
                new_material = copy.deepcopy(self.__material)
                # Change material propertys according to the given material function (law)
                # Structural material settings
                for young_modul in new_material.get_young_module():
                    young_modul.set_young_module(young_modul.get_young_module() *
                                                 (1.0 - (float(self.__steps - mat_numb - 1))
                                                  / float(self.__steps)) ** self.__exponent)

                for poisson_ratio in new_material.get_poisson_ratio():
                    poisson_ratio.set_poisson_ratio(poisson_ratio.get_poisson_ratio())

                # Heat exchange  material settings
                for conductivity in new_material.get_conductivity():
                    conductivity.set_conductivity(conductivity.get_conductivity() *
                                                  (1.0 - (float(self.__steps - mat_numb - 1))
                                                   / float(self.__steps)) ** self.__exponent)
                new_material.set_name(new_material.get_name() + "_" + str(mat_numb))
                solid_sections.append(FEM.SolidSection(new_material,
                                                       FEM.ElementSet("topo_mat_" + str(mat_numb), self.__sets[mat_numb])))
        return solid_sections












