import os.path
import FEM

class ReadINP():

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


     def __read_node(self):
        i_file = open(self.__filename, "r")
        node_dic = {}
        read_node = False
        for line in i_file:
            if line[-1] == "\n":
                line = line[0:-1]
            # Coments and line does not exist
            if len(line) == 0:
                continue
            elif len(line) >= 2:
                if line[0:1] =="**":
                    continue

            # Stop reading
            if line[0] == "*":
                read_node = False

            if read_node:
                 words = line.split(", ")
                 node_dic[int(words[0])] = FEM.Node(int(words[0]), float(words[1]), float(words[2]), float(words[3]))

            # Check if node key is found and not *NODE PRINT ...
            if "*NODE" in line.upper():
                words = line.split(",")
                for word in words:
                    word_no_space = word.split(" ")
                    for word2 in word_no_space:
                        if word2.upper() == "*NODE":
                            read_node = True
                        if "FILE" in word2.upper():
                            read_node = False
                        if "PRINT" in word2.upper():
                            read_node = False
        return node_dic

     def __read_element(self, node_dic):
         i_file = open(self.__filename, "r")
         elem_dic ={}
         read_element = False
         for line in i_file:
             if line[-1] == "\n":
                 line = line[0:-1]
             # Coments and line does not exist
             if len(line) == 0:
                 continue
             elif len(line) >= 2:
                 if line[0:1] == "**":
                     continue

             # Stop reading
             if line[0] == "*":
                 read_element= False

             if read_element:
                 words = line.split(", ")
                 first_word = True
                 node_list = []
                 for word in words:
                     if first_word:
                         elem_id = int(word)
                         first_word = False
                     else:
                         node_list.append(node_dic[int(word)])
                 elem_dic[elem_id] = FEM.Element(elem_id, node_list)

             # Check if node key is found and not *NODE PRINT ...

             if "*ELEMENT" in line.upper():
                 words = line.split(",")
                 for word in words:
                     new_word = word.split(" ")
                     for word_no_space in new_word:
                         if word_no_space.upper() == "*ELEMENT":
                             read_element = True
         return elem_dic

     def __read_material(self):
         material_list = []
         read_material = False
         read_elastic = False
         read_conductivity = False
         i_file = open(self.__filename, "r")
         first_material = True
         for line in i_file:
             if line[-1] == "\n":
                 line = line[0:-1]
             # Coments and line does not exist
             if len(line) == 0:
                 continue
             elif len(line) >= 2:
                 if line[0:1] == "**":
                     continue

             # Stop reading
             if line[0] == "*":
                 read_material = False
                 read_elastic = False
                 read_conductivity = False


             if read_elastic:
                 words = line.split(",")
                 if len(words) <= 2:
                     young_module = FEM.YoungModule(float(words[0]), 0)
                     poisson_ratio = FEM.PoissonRatio(float(words[1]), 0)
                 else:
                     young_module = FEM.YoungModule(float(words[0]), words[2])
                     poisson_ratio = FEM.PoissonRatio(float(words[1]), words[2])
                 mat.add_young_module(young_module)
                 mat.add_poisson_ratio(poisson_ratio)

             if read_conductivity:
                 words = line.split(",")
                 if len(words) <= 1:
                    conductivity = FEM.Conductivity(float(words[0]), 0)
                 else:
                    conductivity = FEM.Conductivity(float(words[0]), words[1])
                 mat.add_conductivity(conductivity)

             # Check if node key is found and not *NODE PRINT ...
             if "*MATERIAL" in line.upper():

                 words = line.split(",")
                 for word in words:
                     new_word = word.split(" ")
                     for word_no_space in new_word:
                         if word_no_space.upper() == "*MATERIAL":
                             read_material = True

                 if read_material:
                     if not first_material:
                         material_list.append(mat)
                     first_material = False
                     words = line.split(", ")
                     material_name = ""
                     for word in words:
                         if "NAME" in word.upper():
                             word_no_equal = word.split("=")
                             material_name = word_no_equal[1]
                     mat = FEM.Material(material_name)

             if "*ELASTIC" in line.upper():
                  read_elastic = True
             if "*CONDUCTIVITY" in line.upper():
                  read_conductivity = True

         material_list.append(mat)
         return material_list

     def __read_element_sets(self, elem_dic):
         i_file = open(self.__filename, "r")
         elem_sets = []
         read_element_set = False
         set_type_is_elset = True
         for line in i_file:
             if line[-1] == "\n":
                 line = line[0:-1]
             # Coments and line does not exist
             if len(line) == 0:
                 continue
             elif len(line) >= 2:
                 if line[0:1] == "**":
                     continue

             # Stop reading
             if line[0] == "*":
                 read_element_set = False

             if read_element_set:
                 words = line.split(",")

                 if set_type_is_elset:
                     for word in words:
                         if word.isdigit():
                            elem_set.add_element(elem_dic[int(word)])
                 else:
                     elem_set.add_element(elem_dic[int(words[0])])


             # Check if node key is found and not *NODE PRINT ...
             if "*ELSET" in line.upper():
                 set_type_is_elset = True
                 read_element_set = True
                 words = line.split(",")
                 new_word = words[1].split("=")
                 elset_name = self.__remove_char_on_black_list(new_word[1])
                 elem_set = FEM.ElementSet(elset_name)
                 elem_sets.append(elem_set)

             if "*ELEMENT" in line.upper():
                 if "ELSET" in line.upper():
                     set_type_is_elset = False
                     read_element_set = True
                     words = line.split(",")
                     for word in words:
                         if "ELSET" in word.upper():
                             new_word = word.split("=")
                             elset_name = self.__remove_char_on_black_list(new_word[1])
                     elem_set = FEM.ElementSet(elset_name)
                     elem_sets.append(elem_set)

         return elem_sets

     def __read_solid_section(self, materials, elem_sets):
         i_file = open(self.__filename, "r")
         solid_sections= []
         for line in i_file:
             if line[-1] == "\n":
                 line = line[0:-1]
             # Coments and line does not exist
             if len(line) == 0:
                 continue
             elif len(line) >= 2:
                 if line[0:1] == "**":
                     continue

             # Check if node key is found and not *NODE PRINT ...
             if "*SOLID SECTION" in line.upper():
                 solid_section = FEM.SolidSection()
                 words = line.split(",")
                 for word in words:
                     if "ELSET" in word.upper():
                         new_word = word.split("=")
                         elset_name = self.__remove_char_on_black_list(new_word)
                     if "MATERIAL" in word.upper():
                         new_word = word.split("=")
                         material_name = self.__remove_char_on_black_list(new_word[1])
                 for material in materials:

                     if material.get_name() == material_name:
                         solid_section.set_material(material)
                 for elset in elem_sets:
                     if elset.get_name() == elset_name:
                         solid_section.set_elset(elset)
                 solid_sections.append(solid_section)

         return solid_sections


     def read(self):

        if not os.path.isfile(self.__filename):
            raise ValueError("Given file does not exist %f", self.__filename)

        node_dic = self.__read_node()
        elem_dic = self.__read_element(node_dic)
        materials = self.__read_material()
        elem_sets = self.__read_element_sets(elem_dic)
        solid_sections = self.__read_solid_section(materials, elem_sets)
        fe_body = FEM.Body(1, node_dic, elem_dic, solid_sections)
        return fe_body













