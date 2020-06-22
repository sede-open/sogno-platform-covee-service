import control_strategies.quadratic_control as quadratic_control
from control_strategies.runPF import runPF
import numpy as np

class Quadratic_Control():

    def __init__(self, grid_data, node_with_battery, num_customers, SOC_init):
        self.grid_data = grid_data	
        self.num_PV = self.grid_data[7]
        self.num_bus = self.grid_data[4]
        self.node_with_battery = node_with_battery
        self.num_customers = num_customers
        self.SOC_init = SOC_init            

        self.control_reactive_power = quadratic_control.Quadratic_Reactive_Power(grid_data)
        [self.reactive_power, self.alpha, self.mu_min] = self.control_reactive_power.initialize_control()

        self.control_active_power_PV = quadratic_control.Quadratic_Active_Power_PV(grid_data)
        [self.active_power_PV, self.alpha_PV] = self.control_active_power_PV.initialize_control()

        self.control_active_power_batt = quadratic_control.Quadratic_Active_Power_Batt(grid_data, node_with_battery, num_customers, SOC_init)
        [self.active_power_battery_list, self.active_power_battery, self.alpha_P, self.xi_min] = self.control_active_power_batt.initialize_control()

        iter_calculation = quadratic_control.iteration_calculation(grid_data, node_with_battery, num_customers, SOC_init)
        self.lim = iter_calculation.calculate_alpha()
        self.lim_p = iter_calculation.calculate_alphaP()

    def initialize_control(self):
        

        both = set(self.node_with_battery).intersection(self.num_PV)
        indices_batt = [self.node_with_battery.index(x) for x in both]
        indices_PV = [self.num_PV.index(x) for x in both]

        # Set the parameters
        # ========================================================================
        self.K1 = 1.0
        for i in range(int(len(self.num_PV))):
            self.alpha[i] = self.K1*self.lim
            self.alpha_PV[i] = self.K1*self.lim
        self.K2 = 1.0
        for i in range(int(len(self.node_with_battery))):
            self.alpha_P[i] = self.K2*self.lim
    
    def control_(self, k, PV_list, q_PV, v_gen, active_power_PV, active_power_battery, v_tot, activate_battery,activate_power_curtailment):
        ############# RUN QUADRATIC VOLTAGE CONTROL ###############################################
        # By changing the ration alpha/alpha_p we can control if we want use
        # more the PV or the batteries for the regulation (for example depending on the SOC)

        self.reactive_power = q_PV
        self.active_power_PV = active_power_PV
        self.active_power_battery = active_power_battery

        # REACTIVE POWER CONTROL PV
        # ================================================================================================
        [self.reactive_power, self.mu_min] = self.control_reactive_power.Voltage_Control(k, PV_list, q_PV, v_gen, self.alpha)

        # ACTIVE POWER CONTROL PV
        # ================================================================================================
        if activate_power_curtailment == "true":
            self.active_power_PV = self.control_active_power_PV.Voltage_Control(k, PV_list, active_power_PV, v_gen, self.alpha_PV)
            for i in range(len(self.num_PV)):	
                if i == 0:	
                    if self.mu_min[i+1] != 0 and self.xi_min[i+1] !=0:	
                        self.alpha_PV[i] = self.K1*self.lim	
                    else:	
                        self.alpha_PV[i] = 0.0	
                elif i in range(len(self.num_PV)-1):	
                    if (self.mu_min[i-1] != 0 and self.xi_min[i-1] !=0) or (self.mu_min[i+1] != 0 and self.xi_min[i+1] !=0):	
                        self.alpha_PV[i] = self.K1*self.lim	
                    else:	
                        self.alpha_PV[i] = 0.0	
                elif i == len(self.num_PV)-1:	
                    if self.mu_min[i-1] != 0 and self.xi_min[i-1] !=0: 	
                        self.alpha_PV[i] = self.K1*self.lim	
                    else:	
                        self.alpha_PV[i] = 0.0               	
                else:	
                    pass
        else:
            pass       

        if activate_battery == "true":
            # COORDINATED ACTIVE POWER CONTROL (BATT)
            # ==========================================================================================================================================
            [self.active_power_battery_list, self.active_power_battery, self.xi_min]  = self.control_active_power_batt.Voltage_Control(k, 
                                                                                                PV_list, self.active_power_battery, v_tot.tolist(), self.alpha_P)  
            
            for i in range(len(self.num_PV)):
                if self.mu_min[i] !=0 and i != 0:
                    self.alpha_P[i] = self.K1*self.lim
                else:
                    self.alpha_P[i] = 0.0001   
        else:
            pass


        return self.reactive_power, self.active_power_battery, self.active_power_battery_list, self.active_power_PV


        




