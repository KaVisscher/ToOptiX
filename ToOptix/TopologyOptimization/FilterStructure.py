import numpy as np

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
