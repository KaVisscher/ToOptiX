import Phraser

from . import Geometry
import os
import numpy as np
import logging


def run_optimization(volfrac, penal, workDir, solverPath, matSets, iterations, StructIsActive, staticPath, weightStatic, thermIsActive, heatPath, weightTherm):


    #---------------Input Path

    work_path = workDir
    result_path = work_path + "/STL_Results/"
    solver_path = solverPath

    all_fe_systems = []
    if StructIsActive:
        s_fe_system = TopologyOptimization.FESystem()
        s_fe_system.set_type('static')
        s_fe_system.set_file_path(staticPath)
        s_fe_system.set_weight_factor(weightStatic)
        all_fe_systems.append(s_fe_system)

    if thermIsActive:

        t_fe_system = TopologyOptimization.FESystem()
        t_fe_system.set_type('heat_transfer')
        t_fe_system.set_file_path(heatPath)
        t_fe_system.set_weight_factor(weightTherm)
        all_fe_systems.append(t_fe_system)



    #------------------Input Path

    # Logging file
    if os.path.isfile(work_path + 'Topo.log'):
        os.remove(work_path + 'Topo.log')

    if not os.path.isdir(work_path):
        os.mkdir(work_path)

    if not os.path.isdir(result_path):
        os.mkdir(result_path)

    logging.basicConfig(filename=work_path + 'Topo.log', level=logging.INFO)
    logging.info(' Topology optimization started')
    logging.info(' Source code written by DMST')


    # Import files and create FEM objects
    ccx_phraser = Phraser.ReadINP()
    # Get a file for the phraser (just for building up the element and material settings)
    ccx_phraser.set_filename(all_fe_systems[0].get_file_path())
    femObj_topo = ccx_phraser.read()


    # Start compaction
    for element in femObj_topo.get_all_elements():
        element.set_compaction(1.0)

    # Define design space (in this case all elements are useds
    design_space = TopologyOptimization.DesignSpace()
    design_space.set_elements(femObj_topo.get_all_elements())
    #design_space.remove_elements_from_file('NoDesignSpace.inp')

    # Define material law for topology optimization
    # There can be several different material definitions
    material = femObj_topo.get_solid_sections()[0].get_material()
    material_function = TopologyOptimization.MaterialFunction(material, femObj_topo.get_all_elements())
    material_function.set_material_steps(matSets)
    material_function.set_exponent(penal)


    optimizer = TopologyOptimization.BasicOptimization()
    optimizer.set_maximum_change_per_iteration(0.2)
    optimizer.set_minimum_compaction_ratio(volfrac)
    optimizer.set_compaction_reduction((1.0-volfrac)/iterations)
    optimizer.set_exponent(penal)


    #------------ Start optimization loop
    converged = False
    mid_sens_list = []
    print("start optimization")
    logging.info(" 1) iteration, 2) Sensitivity optimization criteria in %, 3) compaction control ratio in % 4) compaction ratio convergence")
    logging.info(" 2) Should be near 0.0%, 3) Should be near 100% 4) Should be exact 0.0% (converges first)")
    log_string = '{:>8s}, {:>12s}, {:>12s}, {:>12s}'.format("1)", "2)", "3)", "4)")
    logging.info(log_string)
    iteration = 0

    filter_structure = TopologyOptimization.FilterStructure()
    filter_structure.create_filter_structure(femObj_topo)

    heat_transfer = False
    static_analysis = True
    ccx_writer = Phraser.WriterINP()


    while (not converged):
        iteration += 1
        femObj_topo.set_solid_sections(material_function.get_solid_section())

        optimizer.refresh_sensitivity(design_space)
        for system in all_fe_systems:
            if system.get_type() == "static":
                # ---------  Run static part
                # Calculate system for displacement
                ccx_writer.modify_file_for_static_topo(system.get_file_path(), work_path + 'StaticSysTopo.inp', femObj_topo)
                cmd_topo_static = solver_path + " " + work_path + "StaticSysTopo"
                os.system(cmd_topo_static)

                # Read results for boundarys
                result_reader = Phraser.ReadDAT(work_path + 'StaticSysTopo.dat')
                result_reader.add_displacement(femObj_topo)

                # Calculate energy density
                cmd_sens_static = solver_path + " "  + work_path + 'StaticSensTopo'
                ccx_writer.modify_file_add_displacement_boundaries(system.get_file_path(),  work_path + 'StaticSensTopo.inp', femObj_topo)
                os.system(cmd_sens_static)

                # Read results for energy density
                result_reader = Phraser.ReadDAT(work_path + 'StaticSensTopo.dat')
                result_reader.add_energy_density(femObj_topo)
                optimizer.set_sensitivity_as_energy_density(design_space, system)

            if system.get_type() == "heat_transfer":
                # ------- Run thermal part
                # Calculate system for temperature
                ccx_writer.modify_file_for_heat_transfer_topo(system.get_file_path(), work_path + 'ThermSysTopo.inp', femObj_topo)
                cmd_topo_therm = solver_path + ' ' + work_path + 'ThermSysTopo'
                os.system(cmd_topo_therm)

                # Read results for boundarys
                result_reader = Phraser.ReadDAT(work_path + 'ThermSysTopo.dat')
                result_reader.add_temperature(femObj_topo)

                # Calculate heat flux
                cmd_sens_therm = solver_path + ' ' + work_path + 'ThermSensTopo'
                ccx_writer.modify_file_add_temperature_boundaries(system.get_file_path(), work_path + 'ThermSensTopo.inp', femObj_topo)
                os.system(cmd_sens_therm)

                # Read results for heat flux
                result_reader = Phraser.ReadDAT(work_path + 'ThermSensTopo.dat')
                result_reader.add_heat_flux(femObj_topo)
                optimizer.set_sensitivity_as_heat_flux(design_space, system)
        optimizer.fix_sensitivity()


        # Start optimizer
        optimizer.set_design_variables_as_compaction(design_space)
        print("filter sensitivity")
        #optimizer.filter_sensitivity(design_space, filter_structure)
        print("start optimization")
        optimizer.optimize()
        print("end optimization")

        optimizer.set_new_design_variable_as_new_compaction(design_space)
        # Optimization Criteria
        mid_sens_list.append(np.abs(np.mean(optimizer.get_sensitivity())))
        if len(mid_sens_list) > 1:
            sens_opti_criteria = ((mid_sens_list[len(mid_sens_list) - 1] -
                              mid_sens_list[len(mid_sens_list) - 2]) /
                              mid_sens_list[len(mid_sens_list) - 1])
            log_string = '{:8d}, '.format(iteration)
            log_string += "%10.6e, " % (abs(sens_opti_criteria) * 100.0)
            log_string += "%10.6e, " % (100.0 * np.mean(optimizer.get_design_variables())
                                        / optimizer.get_compaction_ratio())
            log_string += "%10.6e, " % (abs(optimizer.get_compaction_ratio() -
                                            optimizer.get_minimum_compaction_ratio()) * 100.0)

            logging.info(log_string)

            if abs(sens_opti_criteria) < optimizer.get_criteria_for_sensitivity() \
                    and optimizer.compaction_reduction_is_complete() and optimizer.get_compaction_ratio_criteria():
                converged = True

        # Output for STL
        if iteration % 1== 0:
            res_elem = []
            for elem in femObj_topo.get_all_elements():
                if elem.get_compaction() > 0.5:
                    res_elem.append(elem)

            topo_surf = Geometry.Surface()
            topo_surf.create_surface_on_elements(res_elem)
            stl_file = Phraser.STL(1)
            topo_part = Geometry.Solid(1, topo_surf.triangles)
            stl_file.parts.append(topo_part)
            print ("Exporting result result elements", len(res_elem))
            if os.path.isfile('STL_res_' + str(iteration) + '.stl'):
                os.remove('STL_res_' + str(iteration) + '.stl')
            stl_file.write(result_path + 'STL_res_' + str(iteration) + '.stl')

    logging.info(' Topology optimization finished')

    res_elem = []
    for elem in femObj_topo.get_all_elements():
        if elem.get_compaction() > 0.5:
            res_elem.append(elem)

    topo_surf = Geometry.Surface()
    topo_surf.create_surface_on_elements(res_elem)
    stl_file = Phraser.STL(1)
    topo_part = Geometry.Solid(1, topo_surf.triangles)
    stl_file.parts.append(topo_part)
    print ("Exporting result result elements", len(res_elem))
    if os.path.isfile('STL_res_last.stl'):
        os.remove('STL_res_last.stl')
    stl_file.write('STL_res_last.stl')





