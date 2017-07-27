import os
import os.path
from . import FEM
from . import Geometry
import re


class WriterINP():


    def __init__(self):

        print ("")


    def modify_file_for_static_topo(self, input_file_name, output_file_name, fem_object=None):

        ifile = open(input_file_name, 'r')
        ofile = open(output_file_name, "w")
        node_print_is_written = False
        write_one_time_solid_section = True
        for line in ifile:
            line = line[0:-1]

            if "*STEP" in line.upper():
                node_print_is_written = False

            if "*NODE PRINT" in line.upper():
                ofile.write("*NODE PRINT, NSET=allNodesTopoOpti\n")
                ofile.write("U\n")
                node_print_is_written = True
                continue
            if "*END STEP" in line.upper() and not node_print_is_written:
                ofile.write("*NODE PRINT, NSET=allNodesTopoOpti\n")
                ofile.write("U\n")
                node_print_is_written = True

            if "*SOLID SECTION" in line.upper():
                if write_one_time_solid_section:
                    ofile.write("*NSET, NSET=allNodesTopoOpti\n")
                    count_8 = 0
                    for node in fem_object.get_all_nodes():
                        count_8 += 1
                        if count_8 == 8:
                            ofile.write("\n")
                            count_8 = 0
                        ofile.write(str(node.get_id()) + ", ")
                    ofile.write("\n")
                    write_one_time_solid_section = False
                    for solid_section in fem_object.get_solid_sections():
                        elset = solid_section.get_elset()
                        material = solid_section.get_material()
                        # Write solid section
                        ofile.write("*Solid Section, elset=" + elset.get_name() +
                                    ", material=" + material.get_name() + "\n")
                        # Write element sets
                        ofile.write("*elset, elset=" + elset.get_name() + "\n")
                        count_8 = 0
                        for element in elset.get_elements():
                            if count_8 == 8:
                                count_8 = 0
                                ofile.write("\n")
                                ofile.write(str(element.get_id()) + ",")
                            else:
                                ofile.write(str(element.get_id()) + ",")
                                count_8 += 1
                        ofile.write("\n")
                        # Write materials
                        ofile.write("*Material, name=" + material.get_name() + "\n")
                        ofile.write("*Elastic\n")
                        mat_count = 0
                        poss_ratio = material.get_poisson_ratio()
                        for young_modul in material.get_young_module():
                            ofile.write(str(young_modul.get_young_module()) + ", " +
                                        str(poss_ratio[mat_count].get_poisson_ratio()) + "," +
                                        str(young_modul.get_temperature()) + "\n")
                            mat_count += 1
                        ofile.write("*Conductivity\n")
                        for conductivity in material.get_conductivity():
                            ofile.write(str(conductivity.get_conductivity()) + ", " +
                                        str(conductivity.get_temperature()) + "\n")

                continue
            ofile.write(line + "\n")




    def modify_file_for_heat_transfer_topo(self, input_file_name, output_file_name, fem_object=None):

        ifile = open(input_file_name, 'r')
        ofile = open(output_file_name, "w")
        node_print_is_written = False
        write_one_time_solid_section = True
        for line in ifile:
            line = line[0:-1]

            if "*STEP" in line.upper():
                node_print_is_written = False

            if "*NODE PRINT" in line.upper():
                ofile.write("*NODE PRINT, NSET=allNodesTopoOpti\n")
                ofile.write("NT\n")
                node_print_is_written = True
                continue
            if "*END STEP" in line.upper() and not node_print_is_written:
                ofile.write("*NODE PRINT, NSET=allNodesTopoOpti\n")
                ofile.write("NT\n")
                node_print_is_written = True

            if "*SOLID SECTION" in line.upper():
                if write_one_time_solid_section:
                    ofile.write("*NSET, NSET=allNodesTopoOpti\n")
                    count_8 = 0
                    for node in fem_object.get_all_nodes():
                        count_8 += 1
                        if count_8 == 8:
                            ofile.write("\n")
                            count_8 = 0
                        ofile.write(str(node.get_id()) + ", ")
                    ofile.write("\n")
                    write_one_time_solid_section = False
                    for solid_section in fem_object.get_solid_sections():
                        elset = solid_section.get_elset()
                        material = solid_section.get_material()
                        # Write solid section
                        ofile.write("*Solid Section, elset=" + elset.get_name() +
                                    ", material=" + material.get_name() + "\n")
                        # Write element sets
                        ofile.write("*elset, elset=" + elset.get_name() + "\n")
                        count_8 = 0
                        for element in elset.get_elements():
                            if count_8 == 8:
                                count_8 = 0
                                ofile.write("\n")
                                ofile.write(str(element.get_id()) + ",")
                            else:
                                ofile.write(str(element.get_id()) + ",")
                                count_8 += 1
                        ofile.write("\n")
                        # Write materials
                        ofile.write("*Material, name=" + material.get_name() + "\n")
                        ofile.write("*Elastic\n")
                        mat_count = 0
                        poss_ratio = material.get_poisson_ratio()
                        for young_modul in material.get_young_module():
                            ofile.write(str(young_modul.get_young_module()) + ", " +
                                        str(poss_ratio[mat_count].get_poisson_ratio()) + "," +
                                        str(young_modul.get_temperature()) + "\n")
                            mat_count += 1
                        ofile.write("*Conductivity\n")
                        for conductivity in material.get_conductivity():
                            ofile.write(str(conductivity.get_conductivity()) + ", " +
                                        str(conductivity.get_temperature()) + "\n")

                continue
            ofile.write(line + "\n")

    def modify_file_add_displacement_boundaries(self, input_file_name, output_file_name, fem_object=None):

        ifile = open(input_file_name, 'r')
        ofile = open(output_file_name, "w")
        set_boundarys = False
        write_elset_all = True
        ignore_section = False
        el_print_is_written = False

        for line in ifile:
            line = line[0:-1]

            if "*" == line[0] and not "**" == line[0:2]:
                ignore_section = False

            if "*BOUNDARY" in line.upper():
                ignore_section = True

            if ignore_section:
                continue

            if "*END STEP" in line.upper():
                set_boundarys = True

            if set_boundarys:
                set_boundarys = False
                ofile.write("*Boundary\n")
                for node in fem_object.get_all_nodes():
                    ofile.write(str(node.get_id()) + ", 1, 1, " + str(node.get_u1()) + "\n")
                    ofile.write(str(node.get_id()) + ", 2, 2, " + str(node.get_u2()) + "\n")
                    ofile.write(str(node.get_id()) + ", 3, 3, " + str(node.get_u3()) + "\n")

            if "*ELPRINT" in line.upper():
                ofile.write("*ELPRINT, ELSET=allElemTopoOpti\n")
                ofile.write("ENER\n")
                el_print_is_written = True
                continue
            if "*END STEP" in line.upper() and not el_print_is_written:
                ofile.write("*ELPRINT, ELSET=allElemTopoOpti\n")
                ofile.write("ENER\n")
                el_print_is_written= True

            if "*SOLID SECTION" in line.upper():
                if write_elset_all:
                    write_elset_all = False
                    ofile.write("*ELSET, ELSET=allElemTopoOpti\n")
                    count_8 = 0
                    for elem in fem_object.get_all_elements():
                        count_8 += 1
                        if count_8 == 8:
                            ofile.write("\n")
                            count_8 = 0
                        ofile.write(str(elem.get_id()) + ", ")
                    ofile.write("\n")
            ofile.write(line + "\n")



    def modify_file_add_temperature_boundaries(self, input_file_name, output_file_name, fem_object=None):

        ifile = open(input_file_name, 'r')
        ofile = open(output_file_name, "w")
        set_boundarys = False
        write_elset_all = True
        ignore_section = False
        el_print_is_written = False

        for line in ifile:
            line = line[0:-1]

            if "*" == line[0] and not "**" == line[0:2]:
                ignore_section = False

            if "*BOUNDARY" in line.upper():
                ignore_section = True

            if ignore_section:
                continue

            if "*END STEP" in line.upper():
                set_boundarys = True

            if set_boundarys:
                set_boundarys = False
                ofile.write("*Boundary\n")
                for node in fem_object.get_all_nodes():
                    ofile.write(str(node.get_id()) + ", 11, 11, " + str(node.get_temperature()) + "\n")

            if "*ELPRINT" in line.upper():
                ofile.write("*ELPRINT, ELSET=allElemTopoOpti\n")
                ofile.write("HFL\n")
                el_print_is_written = True
                continue
            if "*END STEP" in line.upper() and not el_print_is_written:
                ofile.write("*ELPRINT, ELSET=allElemTopoOpti\n")
                ofile.write("HFL\n")
                el_print_is_written= True

            if "*SOLID SECTION" in line.upper():
                if write_elset_all:
                    write_elset_all = False
                    ofile.write("*ELSET, ELSET=allElemTopoOpti\n")
                    count_8 = 0
                    for elem in fem_object.get_all_elements():
                        count_8 += 1
                        if count_8 == 8:
                            ofile.write("\n")
                            count_8 = 0
                        ofile.write(str(elem.get_id()) + ", ")
                    ofile.write("\n")
            ofile.write(line + "\n")
















class File(object):
    """ File-object

    Example for a file definition

    >>> file1 = File(1, "foo.txt")
    """

    def __init__(self,ID=None, Filepath=None):
        self.__filepath = Filepath
        self.__id = ID

    @property
    def id(self):
        return self.__id

    @ id.setter
    def id(self, ID):
        self.__id = ID

    @property
    def filepath(self):
        return self.__filepath

    @filepath.setter
    def filepath(self, filepath):
        self.__filepath = filepath

class STL(File):
    """ STL-File with geometric data

    :param ID (int): Id of the file
    :param Filepath (str): Path of the file

    Example for creating an stl-object

    >>> file1 = STL(1, "./foo.stl")
    >>> part = file.parts[0]

    .. note::
        The file will automatically import the results if the file is given
        Otherwise you need to call import_stl
    """
    def __init__(self, ID=None, Filepath=None):
        File.__init__(self, ID, Filepath)
        self.__parts = []
        # If file is given the importin will started
        if self.filepath:
            self.read()

    @property
    def parts(self):
        """
        :return: All solid objects which are imported
        """
        return self.__parts

    def write(self, filename):
        """ This method can export the current data into an stl-file

        """
        if os.path.isfile(filename):
            raise ValueError ("File does exist alread %f", filename)
        print("Export stl in", filename)
        o_file = open(filename,"w")
        for part in self.parts:
            solid = part
            o_file.write("solid Exported from DMST-STL\n")
            for triangle in solid.triangles:
                #o_file.write("facet " + str(triangle.normal[0]) + " " + str(triangle.normal[1]) + " " + str(triangle.normal[2]) + "\n")
                o_file.write("outer loop\n")
                for point in triangle.points:
                    o_file.write("vertex " + str(point.get_x()) + " " + str(point.get_y()) + " " + str(point.get_z()) + "\n")
                o_file.write("endloop\n")
                #o_file.write("endfacet\n")
            o_file.write("endsolid\n")

    def read(self):
        """ This method imports the geometry to the parts attribute

        """

        if not os.path.isfile(self.filepath):
            raise ValueError ("Given file doesnt exist %f", self.filepath)
        i_file = open(self.filepath, "r")

        # Patterns which are needed
        s_pat = "solid"
        l_pat = "outer loop"
        f_pat = "facet"
        p_pat = "vertex"

        f_e_pat = "endfacet"
        s_e_pat = "endsolid"
        l_e_pat = "endloop"

        solid_is_found = False
        facet_is_found = False
        loop_is_found = False
        id_s = 0 # ID of the solid
        id_t = 0 # ID for triangles
        id_p = 0 # ID for points

        tmp_p_list = [] # Saves all found points
        id_p_old = 0 #ID for points

        # Reading the file
        for line in i_file:
            line = line[0:-1]

            # Solid is found

            if re.match(s_pat, line, 2):
                id_s +=1
                s = Geometry.Solid(id_s, [])
                self.parts.append(s)
                solid_is_found = True
                continue
            # Solid is closed
            if re.match(s_e_pat, line, 2):
                solid_is_found = False
                continue

            # Facet is found
            if re.match(f_pat, line,2) and solid_is_found:
                id_t += 1
                facet_is_found = True
                t = Geometry.Triangle(id_t, [])
                words = line.split(" ")
                nx = float(words[0])
                ny = float(words[1])
                nz = float(words[2])
                t.normal = [nx, ny, nz]
                s.triangles.append(t)
                continue
            # Facet is closed
            if re.match(f_e_pat, line,2) and solid_is_found and facet_is_found:

                facet_is_found = False
                continue

            # Loop is found
            if re.match(l_pat, line,2) and solid_is_found and facet_is_found:
                loop_is_found = True
                continue
            # Loop is closed
            if re.match(l_e_pat, line,2) and solid_is_found and facet_is_found and loop_is_found:
                loop_is_found = False
                continue

            # Vertex is found
            if re.match(p_pat, line,2) and solid_is_found and facet_is_found and loop_is_found:
                # Finding new point coord
                words = line.split(" ")
                x = float(words[1])
                y = float(words[2])
                z = float(words[3])

                # Checking if point_id exists already
                # If the point_id is found choose the same ID
                p_is_found = False
                controll_count = 0
                for t_p in tmp_p_list:
                    if t_p.x == x and t_p.y == y and t_p.z == z:
                        id_p_old = t_p.id
                        controll_count += 1
                        p_is_found = True
                    if controll_count > 1:
                        raise ValueError("Two same points have different ID s")

                # Creating a new point_id or selectin an old
                if p_is_found:
                    p = Geometry.Point(id_p_old, x, y, z)
                else:
                    id_p += 1
                    p = Geometry.Point(id_p, x, y, z)
                    tmp_p_list.append(p)

                # Resulting point
                t.points.append(p)
        i_file.close()

        if id_s== 0 or id_t== 0 or id_p== 0:
            raise ValueError("Fileformat STL does not match: Define Solid-->Faces-->Vertexes")
        print("STL-File succesfully imported")
        print("Solids: ", id_s)
        print("Triangles", id_t)
        print("Different Vertices", id_p)


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



