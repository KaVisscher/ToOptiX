import FEM

class WriterINP():


    def __init__(self):

        print ("")


    def modify_file_for_static_topo(self, input_file_name, output_file_name, fem_object=None):

        ifile = open(input_file_name, 'r')
        ofile = open(output_file_name, "w")
        node_print_is_written = False
        write_one_time_solid_section = True
        for line in ifile:
            if line[-1] == "\n":
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
            if line[-1] == "\n":
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
            if line[-1] == "\n":
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
            if line[-1] == "\n":
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














