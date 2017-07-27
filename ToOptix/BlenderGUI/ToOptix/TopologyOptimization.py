import numpy as np
import copy
from . import FEM


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













class FilterStructure():


    def __init__(self):


        # Each element has some other elements with an weight

        # structure[elemID] = [[scaling_vector], [Referenced elements]]
        self.__structure = {}
        self.__scaling_values = {}
        # elements_on_node[node.id] = [elem1, elem2 ... ] all elements which are acting on this node
        self.__element_on_node = {}
        self.__weight_of_current_element = 0.75
        self.__filter_area = None

    def __find_elements_on_nodes(self):

        # Found a reference for node to elements
        for element in self.__filter_area.get_all_elements():
            for node in element.get_nodes():
                try:
                    self.__element_on_node[node.get_id()].add(element)
                except:
                    self.__element_on_node[node.get_id()] = set()
                    self.__element_on_node[node.get_id()].add(element)

    def create_filter_structure(self, filter_area):
        self.__filter_area = filter_area
        self.__find_elements_on_nodes()
        # Elements in that this filter should be used
        for element in self.__filter_area.get_all_elements():
            # Create a set for all elements which are near this element
            element_in_region = set()

            # Calculate the referenced center point for calulating the distances
            xc = element.get_x_center()
            yc = element.get_y_center()
            zc = element.get_z_center()
            for node in element.get_nodes():
                element_in_region = element_in_region | self.__element_on_node[node.get_id()]

            inverse_distance_to_neighbour_elements = []
            neighbour_elements = []
            for neighbour_element in element_in_region:
                # If the current element is the same as neighbour --> no neighbour
                if element.get_id() == neighbour_element.get_id():
                    continue
                xc1 = neighbour_element.get_x_center()
                yc1 = neighbour_element.get_y_center()
                zc1 = neighbour_element.get_z_center()
                inverse_distance_to_neighbour_elements.append(1 / ((xc1 - xc) ** 2 + (yc1 - yc) ** 2 + (zc1 - zc) ** 2) ** 0.5)
                neighbour_elements.append(neighbour_element)

            # For normizing the inverse distances, the scaling factor can be used directly
            normize_distances = 0
            for distance in inverse_distance_to_neighbour_elements:
                normize_distances = distance + normize_distances

            inverse_distance_normized = []
            for dist_n in inverse_distance_to_neighbour_elements:
                inverse_distance_normized.append((1 - self.__weight_of_current_element) * 1 / normize_distances * (dist_n))
            inverse_distance_normized.append(self.__weight_of_current_element)
            # Add current element which is weighned by a factor
            neighbour_elements.append(element)
            self.__structure[element.get_id()] = neighbour_elements
            self.__scaling_values[element.get_id()] = np.array(inverse_distance_normized)

    def get_scaling_values(self, element_ID):
        return self.__scaling_values[element_ID]

    def get_filter_elements_on_element(self, element_ID):
        return self.__structure[element_ID]

class FESystem():

    def __init__(self):

        self.__type = None
        self.__file_path = None
        self.__weight_factor = 1.0

    def set_type(self, type):
        self.__type = type

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def get_type(self):
        return self.__type

    def get_file_path(self):
        return self.__file_path

    def set_weight_factor(self, weight_factor):
        self.__weight_factor = weight_factor

    def get_weight_factor(self):
        return self.__weight_factor



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

class BasicOptimization():

    def __init__(self):

        self.__design_variable = None
        self.__convergence_max = 0.001
        self.__sensitivity = None
        self.__sensitivity_built_up = None
        self.__exponent = 5.0
        self.__max_change = 0.2 # Default parameter
        self.__compaction_ratio = 1.0
        self.__comp_reduction = 0.1
        self.__minimum_compaction_ratio = 0.3
        self.__compaction_reduction_complete = False
        self.__sensitivity_optimization_criteria = 0.001
        self.__weight_factor_static = 1.0
        self.__weight_factor_heat_transfer = 1.0
        self.__first_run = True
        self.__old_sensitivity = None
        self.__compaction_ratio_is_reached = False


    def set_exponent(self, exponent):
        self.__exponent = exponent


    def set_weight_factor_heat_transfer(self, factor):
        self.__weight_factor_heat_transfer = factor

    def set_weight_factor_static(self, factor):
        self.__weight_factor_static = factor

    def set_minimum_compaction_ratio(self, mininimum_compaction_ratio):
        self.__minimum_compaction_ratio = mininimum_compaction_ratio

    def get_minimum_compaction_ratio(self):
        return self.__minimum_compaction_ratio

    def get_criteria_for_sensitivity(self):
        return self.__sensitivity_optimization_criteria

    def compaction_reduction_is_complete(self):
        return self.__compaction_reduction_complete


    def set_maximum_change_per_iteration(self, change):
        self.__max_change = change

    def set_compaction_reduction(self, comp_reduction):
        self.__comp_reduction = comp_reduction

    def get_compaction_ratio(self):
        return self.__compaction_ratio

    def __reduce_compaction(self):
        if self.__compaction_ratio - self.__comp_reduction <= self.__minimum_compaction_ratio:
            self.__compaction_ratio = self.__minimum_compaction_ratio
            self.__compaction_reduction_complete = True
        else:
            self.__compaction_ratio -= self.__comp_reduction

    def set_new_design_variable_as_new_compaction(self, design_space):
        des_count = 0
        for element in design_space.get_all_elements():
            element.set_compaction(self.__design_variable[des_count])
            des_count += 1

    def fix_sensitivity(self):
        self.__sensitivity = self.__sensitivity_built_up

    def set_design_variables_as_compaction(self, design_space):
        compaction = []
        for element in design_space.get_all_elements():
            compaction.append(element.get_compaction())
        self.__design_variable = np.array(compaction)


    def set_sensitivity_as_energy_density(self, design_space, fe_system):
        new_sens = []
        for element in design_space.get_all_elements():
             new_sens.append(element.get_energy_density())
        median = np.median(new_sens)
        self.__sensitivity_built_up += fe_system.get_weight_factor() * 1.0/median * np.array(new_sens)

    def set_sensitivity_as_heat_flux(self, design_space, fe_system):
        new_sens = []
        for element in design_space.get_all_elements():
            new_sens.append(element.get_heat_flux())
        median = np.median(new_sens)
        self.__sensitivity_built_up += fe_system.get_weight_factor() * 1.0/median * np.array(new_sens)


    def refresh_sensitivity(self, design_space):
        sensitivity_built_up = []
        for element in design_space.get_all_elements():
            sensitivity_built_up.append(0.0)
        self.__sensitivity_built_up = np.array(sensitivity_built_up)

    def get_sensitivity(self):
        return self.__sensitivity

    def get_design_variables(self):
        return self.__design_variable


    def optimize(self):
        self.__reduce_compaction()
        # Negative for static
        # Positive for heat transfer
        sensitivity = np.abs(0.5 * (self.__exponent) * (self.__design_variable) ** (self.__exponent - 1) * self.__sensitivity)
        if min(sensitivity) <= 0:
            sensitivity += abs(min(sensitivity))
        l_upper = max(sensitivity) # Asymptotes upper one
        l_lower = min(sensitivity) # Asymptotes lower one

        #if self.__first_run:
        #    self.__old_sensitivity = sensitivity
        #else:
        # Slowing down direct optimization
        #    sensitivity = 0.5 * (self.__old_sensitivity + sensitivity)

        new_design_variable = 1.0

        while(abs(l_upper - l_lower) > (l_upper * self.__convergence_max)):

            l_mid = 0.5 * (l_lower + l_upper)
            # Values between 0 and 1
            # SIMP method

            #new_design_variable = np.maximum(0.0,
            #                                 np.maximum(self.__design_variable - self.__max_change,
            #                                            np.minimum(1.0,
            #                                                       np.minimum(self.__design_variable + self.__max_change,
            #                                                self.__design_variable * (sensitivity / l_mid) ** 0.5))))
            # BESO-Method
            new_design_variable =np.maximum(0.00001, np.sign(sensitivity - l_mid))

            if np.mean(new_design_variable) - self.__compaction_ratio > 0.0:
                l_lower = l_mid
            else:
                l_upper = l_mid
        if abs(np.mean(new_design_variable) - self.__compaction_ratio) > 0.01:
            self.__compaction_ratio_is_reached = False
        else:
            self.__compaction_ratio_is_reached = True
        print("medium design variable")
        print(np.mean(new_design_variable))
        self.__design_variable = new_design_variable

    def get_compaction_ratio_criteria(self):
        return self.__compaction_ratio_is_reached



    def filter_sensitivity(self, design_space, filter_structure):
        print ("filter sensitivity")

        # Save old sensitivity for new ordering
        count = 0
        save_old_sensitivitys = {}
        for element in design_space.get_all_elements():
            save_old_sensitivitys[element.get_id()] = self.__sensitivity[count]
            count += 1
        count = 0
        new_sensitivity = []
        for element in design_space.get_all_elements():
            scaling_values = filter_structure.get_scaling_values(element.get_id())
            sensitivity_array = []
            for filter_element in filter_structure.get_filter_elements_on_element(element.get_id()):
                sensitivity_array.append(save_old_sensitivitys[filter_element.get_id()])
            new_sensitivity.append(np.dot(scaling_values, np.array(sensitivity_array)))
            count += 1
        self.__sensitivity = np.array(new_sensitivity)
        
        
    def filter_compaction(self, design_space, filter_structure):
        print ("filtering compaction")
        
        # Save old sensitivity for new ordering
        count = 0
        save_old_compaction = {}
        for element in design_space.get_all_elements():
            save_old_compaction[element.get_id()] = self.__design_variable[count]
            count += 1
        count = 0
        new_compaction = []
        for element in design_space.get_all_elements():
            scaling_values = filter_structure.get_scaling_values(element.get_id())
            compaction_array = []
            for filter_element in filter_structure.get_filter_elements_on_element(element.get_id()):
                compaction_array.append(save_old_compaction[filter_element.get_id()])
            new_density = np.dot(scaling_values, np.array(compaction_array))
            if new_density >= 1.0:
                new_density = 1.0
            new_compaction.append(new_density)
            count += 1
        self.__sensitivity = np.array(new_compaction)


















