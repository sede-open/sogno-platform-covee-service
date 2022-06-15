import csv
import os
import numpy as np
import matplotlib.pyplot as plt

V_base = 1
P_base = 10e3

plt.rcParams["font.family"] = "serif"
plt.rcParams["figure.figsize"] = (15,7.5)
plt.rcParams.update({'font.size': 26})
plt.rc('text', usetex=True)
plt.rc('legend', fontsize=20, loc='upper right')    # legend fontsize

cwd = os.getcwd()
wd = os.path.join(cwd, 'results_mpc')
wd.replace('\\', '/')


# Voltage 
# ============================================================
with open(os.path.join(wd, 'results_powerflow/csv_files/voltage.csv')) as csv_file:
    distributed = csv.reader(csv_file, delimiter=',')
    x = list(distributed)
    distributed = np.array(x).astype("float")*V_base

lenght = distributed.shape[1]-1


t = np.matrix(distributed)[:,lenght]
v = distributed

min_leght = len(t)

limitMAX = np.array([1.0495]*min_leght)
limitMIN = np.array([0.9]*min_leght)
limitMAX_20 = np.array([1.07]*min_leght)

plt.figure(1)
plt.plot(limitMAX,c = "khaki",linewidth=8, label=r"$\mathbf{V}_{max}$")
for r in range(3,lenght):
    plt.plot( np.matrix(v)[:,r][0:min_leght]*1.005,linewidth=2, marker="*", c = "dimgray")
plt.plot(np.matrix(v)[:,r-1][0:min_leght]*1.005,linewidth=2, marker="*", c = "dimgray", label=r"$\mathbf{V}$")
plt.plot( np.matrix(v)[:,r][0:min_leght]*1.005,linewidth=2, marker="*", c = "indigo", label=r"$\mathbf{V}$"+" DG n.6")
# plt.plot(t["t" + str(r)][0:min_leght],limitMAX,'k', label=r"$\mathbf{V}_{max}$")
axes = plt.gca()
axes.set_ylim([1.00, 1.060])
plt.xlabel("Iterations")
plt.ylabel("Voltage [p.u.]")
plt.legend(facecolor='white', framealpha=1)
plt.savefig(wd+'/voltage.eps')
plt.savefig(wd+'/voltage.png')


plt.rc('legend', fontsize=20, loc='lower left')    # legend fontsize
# Reactive Power
# ============================================================
with open(os.path.join(wd, 'results_MPC/csv_files/results/reactive_power_list_pred_1.csv')) as csv_file:
    distributed = csv.reader(csv_file, delimiter=',')
    x = list(distributed)
    distributed = np.array(x).astype("float")*V_base

lenght = distributed.shape[1]-1


t = np.matrix(distributed)[:,lenght]
v = distributed

min_leght = len(t)

flex_receive_reactive = np.transpose(np.matrix([list(np.hstack([[0.0]*4,[-0.1]*5])),
                                                list(np.hstack([[0.0]*4,[-0.13]*5])),
                                                list(np.hstack([[0.0]*4,[-0.12]*5]))] ))

plt.figure(2)
for k in range(np.shape(flex_receive_reactive)[1]):
    plt.plot( flex_receive_reactive[0:min_leght][:,k]*1.005,c = "khaki", linewidth=4)
plt.plot( flex_receive_reactive[0:min_leght][:,k]*1.005,c = "khaki", linewidth=4, label = "Flexibility Response")
for r in range(lenght):
    plt.plot( np.matrix(v)[:,r][0:min_leght]*1.005,linewidth=2, marker="*", c = "dimgray")
plt.plot(np.matrix(v)[:,r-1][0:min_leght]*1.005,linewidth=2, marker="*", c = "dimgray", label=r"$ \mathbf{Q}_{DG}$")
plt.plot( np.matrix(v)[:,r][0:min_leght]*1.005,linewidth=2, marker="*", c = "indigo", label=r"$ \mathbf{Q}_{DG}$"+" DG n."+str(r+1))

# plt.plot(t["t" + str(r)][0:min_leght],limitMAX,'k', label=r"$\mathbf{V}_{max}$")
axes = plt.gca()
plt.xlabel("Iterations")
plt.ylabel("Reactive Power [p.u.]")
plt.legend(facecolor='white', framealpha=1)
plt.savefig(wd+'/reactive_power.eps')
plt.savefig(wd+'/reactive_power.png')

# Active Power
# ============================================================
with open(os.path.join(wd, 'results_MPC/csv_files/results/active_power_list_pred_1.csv')) as csv_file:
    distributed = csv.reader(csv_file, delimiter=',')
    x = list(distributed)
    distributed = np.array(x).astype("float")*V_base

lenght = distributed.shape[1]-1


t = np.matrix(distributed)[:,lenght]
v = distributed

min_leght = len(t)

flex_receive_reactive = np.transpose(np.matrix([list(np.hstack([[0.0]*4,[-0.01]*5])),
                                                list(np.hstack([[0.0]*4,[-0.03]*5])),
                                                list(np.hstack([[0.0]*4,[-0.04]*5]))] ))

plt.figure(3)
for k in range(np.shape(flex_receive_reactive)[1]):
    plt.plot( flex_receive_reactive[0:min_leght][:,k]*1.005,c = "khaki", linewidth=4)
plt.plot( flex_receive_reactive[0:min_leght][:,k]*1.005,c = "khaki", linewidth=4, label = "Flexibility Response")
for r in range(lenght):
    plt.plot( np.matrix(v)[:,r][0:min_leght]*1.005,linewidth=2, marker="*", c = "dimgray")
plt.plot(np.matrix(v)[:,r-1][0:min_leght]*1.005,linewidth=2, marker="*", c = "dimgray", label=r"$ \mathbf{P}^{curt}_{DG}$")
plt.plot( np.matrix(v)[:,r][0:min_leght]*1.005,linewidth=2, marker="*", c = "indigo", label=r"$ \mathbf{P}^{curt}_{DG}$"+" DG n."+str(r+1))

# plt.plot(t["t" + str(r)][0:min_leght],limitMAX,'k', label=r"$\mathbf{V}_{max}$")
axes = plt.gca()
plt.xlabel("Iterations")
plt.ylabel("Active Power [p.u.]")
plt.legend(facecolor='white', framealpha=1)
plt.savefig(wd+'/active_power.eps')
plt.savefig(wd+'/active_power.png')


# Flexibility Trigger
# ============================================================
with open(os.path.join(wd, 'results_MPC/csv_files/results/flex_receive_list.csv')) as csv_file:
    distributed = csv.reader(csv_file, delimiter=',')
    x = list(distributed)
    distributed = np.array(x).astype("float")*V_base

lenght = distributed.shape[1]-1


t = np.matrix(distributed)[:,lenght]
v = distributed

min_leght = len(t)

plt.figure(4)

plt.plot( np.matrix(v)[:,0][0:min_leght],linewidth=2, marker="*", c = "indigo")

# plt.plot(t["t" + str(r)][0:min_leght],limitMAX,'k', label=r"$\mathbf{V}_{max}$")
axes = plt.gca()
plt.xlabel("Iterations")
plt.ylabel("Flexibilty response received")
# plt.legend(facecolor='white', framealpha=1)
plt.savefig(wd+'/flex_received.eps')
plt.savefig(wd+'/flex_received.png')