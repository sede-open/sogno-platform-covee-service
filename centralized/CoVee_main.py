from cases.LV_SOGNO import LV_SOGNO
from cases.case_10_nodes import case_10_nodes
from control_strategies.Quadratic_Control import Quadratic_Control
from control_strategies.Linear_Control import Linear_Control
from control_strategies.runPF import runPF
from csv_files.read_profiles import read_profiles
from csv_files.save_results import save_results
import csv
import os
import numpy as np


# set the case
# ======================================================================
activate_battery = "true"
activate_power_curtailment = "true"
control_type = "quadratic"

# # SOGNO
# # =======================================================================
ppc = LV_SOGNO()
num_customers = [0,2,1,1,1,2,6,1,3,3,2,4,2,1,2,3,1,2,5,2,4,4]
node_with_battery = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
SOC_init = [50]*len(node_with_battery)

# case 6 nodes
# =======================================================================
# ppc = case_10_nodes()
# num_customers = [0,2,1,1,1,2,6,1,3,3]
# node_with_battery = [1,2,3,4,5,6,7,8,9]
# SOC_init = [50]*len(node_with_battery)

# read profiles from CSV files
# =======================================================================
profiles = read_profiles()
[PV_list, P_load_list] = profiles.read_csv()

# Initialize Power Flow
# ========================================================================
power_flow = runPF(ppc, [PV_list, P_load_list])
grid_data = power_flow.system_info()

nodes_PV = grid_data[7]
num_bus = grid_data[4]

# Initialize control
# =========================================================================
if control_type == "quadratic":
    control = Quadratic_Control(grid_data, node_with_battery, num_customers, SOC_init)
    control.initialize_control()
    reactive_power = control.reactive_power
    active_power_PV = control.active_power_PV
    active_power_battery_list = control.active_power_battery_list
    active_power_battery = control.active_power_battery

elif control_type == "linear":
    control = Linear_Control(grid_data)
    reactive_power = control.reactive_power
    
    active_power_battery_list = [0.0]*num_bus
    active_power_PV = control.active_power_PV
    active_power_battery = [0.0]*num_bus 
else:
    print("wrong control definition")
    quit()

voltage_list = []
reactive_power_list = []
active_power_list = []
active_power_batt_list = []
iterations = []

for k in range(0,int(1*len(PV_list))):
    # RUN PF 
    # ==============================================================================================
    [v_gen, p_PV, q_PV, p_batt, v_tot] = power_flow.run_Power_Flow(k, PV_list, reactive_power, 
                                                            active_power_battery_list, P_load_list, active_power_PV)
    # COORDINATED VOLTAGE CONTROL
    # ================================================================================================
    if control_type == "quadratic":
        [reactive_power, active_power_battery, active_power_battery_list, active_power_PV] = control.control_(k, PV_list, q_PV, v_gen, 
                                                                                                                    active_power_PV, active_power_battery, v_tot, activate_battery,activate_power_curtailment)
    elif control_type == "linear":
        if k%2 == 0:
            [reactive_power, active_power] = control.control_(k, PV_list, -np.array(reactive_power), v_gen, 
                                                    -np.array(active_power_PV))

            reactive_power = reactive_power 
        else:
            pass
    else:
        pass    

    print("Q_PV", reactive_power)
    print("voltage", v_tot.tolist())

    voltage_list.append(v_tot.tolist())
    reactive_power_list.append(np.asarray(reactive_power).tolist())
    active_power_list.append(np.asarray(p_PV).tolist())
    active_power_batt_list.append(np.asarray(active_power_battery).tolist())
    iterations.append(k)

# save the simulation results in csv
# ======================================================================
save_results = save_results(voltage_list, reactive_power_list, active_power_list, active_power_batt_list, iterations)
save_results.save_csv()

print('simulation finished')