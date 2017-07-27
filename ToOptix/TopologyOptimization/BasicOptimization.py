import numpy as np

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

        if self.__first_run:
            self.__old_sensitivity = sensitivity
        else:
        # Slowing down direct optimization
            sensitivity = 0.5 * (self.__old_sensitivity + sensitivity)

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


















