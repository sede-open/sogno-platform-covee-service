import csv
import os
import numpy as np
import matplotlib.pyplot as plt

V_base = 380
P_base = 10e3

plt.rcParams["font.family"] = "serif"
plt.rcParams["figure.figsize"] = (15,7.5)
plt.rcParams.update({'font.size': 26})
plt.rc('legend', fontsize=20, loc='upper right')    # legend fontsize

cwd = os.getcwd()
wd = os.path.join(cwd, 'csv_files/results')
wd.replace('\\', '/')

# Time
# ============================================================
with open(os.path.join(wd, 'time.csv')) as csv_file:
    time = csv.reader(csv_file, delimiter=',')
    x = list(time)
    time = np.array(x).astype("float")*1/360*4

t = []

for i in range(int(time.shape[0])-1):
    t.append(time[i][0])

# Voltage Average
# ============================================================
with open(os.path.join(wd, 'voltage.csv')) as csv_file:
    distributed = csv.reader(csv_file, delimiter=',')
    x = list(distributed)
    distributed = np.array(x).astype("float")*V_base


for j in range(distributed.shape[1]):
    globals()["bus_" + str(j)] = []
    for i in range(int(distributed.shape[0]) - 1):
        globals()["bus_" + str(j)].append(distributed[i][j])

N = int(600/40)
for j in range(distributed.shape[1]):
    globals()["bus_" + str(j)]= np.convolve(globals()["bus_" + str(j)], np.ones((N,))/N, mode='same')

limitMAX = [1.05*V_base]*(int(distributed.shape[0])-1)
limitMIN = [0.95*V_base]*(int(distributed.shape[0])-1)
limitMAX2 = [1.03*V_base]*(int(distributed.shape[0])-1)
limitMIN2 = [0.97*V_base]*(int(distributed.shape[0])-1)

plt.figure(1)
for j in range(distributed.shape[1]):
    plt.plot(t[10:(int(distributed.shape[0])-10)], globals()["bus_" + str(j)][10:(int(distributed.shape[0])-10)],'grey')
plt.plot(t[10:(int(distributed.shape[0])-10)], bus_19[10:(int(distributed.shape[0])-10)],'deepskyblue', label='bus 20')
plt.plot(t[10:(int(distributed.shape[0])-10)], bus_20[10:(int(distributed.shape[0])-10)],'chartreuse', label='bus 21')
plt.plot(t[10:(int(distributed.shape[0])-10)], bus_21[10:(int(distributed.shape[0])-10)],'red', label='bus 22')
plt.plot(t[10:(int(distributed.shape[0])-10)], limitMAX[10:(int(distributed.shape[0])-10)],'k', label='limitMAX')
plt.plot(t[10:(int(distributed.shape[0])-10)], limitMIN[10:(int(distributed.shape[0])-10)],'k', label='limitMIN')
# # plt.plot(t, limitMAX2,'k', label='limitMAX')
# plt.plot(t, limitMIN2,'k', label='limitMIN')
axes = plt.gca()
axes.set_ylim([0.93*V_base, 1.07*V_base])
plt.xlabel("Time [h]")
plt.ylabel("Voltage [V]")
plt.legend()
# w, h = plt.figaspect(2.)
# plt.figure(figsize=(w,h))
# plt.show()
plt.savefig('/home/ubuntu/covee-control/plots/voltage_controlled.eps')
plt.savefig('/home/ubuntu/covee-control/plots/voltage_controlled.png')


# Reactive Power
# ============================================================
with open(os.path.join(wd, 'reactive_power.csv')) as csv_file:
    q_distributed = csv.reader(csv_file, delimiter=',')
    x = list(q_distributed)
    q_distributed = np.array(x).astype("float")*P_base

for j in range(q_distributed.shape[1]):
    globals()["q_" + str(j)] = []
    for i in range(int(q_distributed.shape[0]) - 1):
        globals()["q_" + str(j)].append(q_distributed[i][j])

plt.figure(2)
for j in range(q_distributed.shape[1]):
    plt.plot(t, globals()["q_" + str(j)],'grey')
plt.plot(t, q_19,'deepskyblue', label='bus 20')
plt.plot(t, q_20,'chartreuse', label='bus 21')
plt.plot(t, q_21,'red', label='bus 22')
axes = plt.gca()
#axes.set_ylim([0.97, 1.08])
plt.xlabel("Time [h]")
plt.ylabel("Reactive Power [VAR]")
plt.legend()
# w, h = plt.figaspect(2.)
# plt.figure(figsize=(w,h))
#plt.show()
plt.savefig('/home/ubuntu/covee-control/plots/reactive_power.eps')
plt.savefig('/home/ubuntu/covee-control/plots/reactive_power.png')

# Active Power
# ============================================================
with open(os.path.join(wd, 'active_power.csv')) as csv_file:
    p_distributed = csv.reader(csv_file, delimiter=',')
    x = list(p_distributed)
    p_distributed = np.array(x).astype("float")*P_base

for j in range(p_distributed.shape[1]):
    globals()["p_" + str(j)] = []
    for i in range(int(p_distributed.shape[0]) - 1):
        globals()["p_" + str(j)].append(p_distributed[i][j])

plt.figure(3)
for j in range(p_distributed.shape[1]):
    plt.plot(t, globals()["p_" + str(j)],'grey')
plt.plot(t, p_19,'deepskyblue', label='bus 20')
plt.plot(t, p_20,'chartreuse', label='bus 21')
plt.plot(t, p_21,'red', label='bus 22')
axes = plt.gca()
#axes.set_ylim([0.97, 1.08])
plt.xlabel("Time [h]")
plt.ylabel("Active Power [W]")
plt.legend()
#w, h = plt.figaspect(2.)
#plt.figure(figsize=(w,h))
plt.savefig('/home/ubuntu/covee-control/plots/active_power.eps')
plt.savefig('/home/ubuntu/covee-control/plots/active_power.png')


# Battery Active Power
# ============================================================
with open(os.path.join(wd, 'active_power_batt.csv')) as csv_file:
    p_distributed = csv.reader(csv_file, delimiter=',')
    x = list(p_distributed)
    p_distributed = np.array(x).astype("float")*P_base

for j in range(p_distributed.shape[1]):
    globals()["p_" + str(j)] = []
    for i in range(int(p_distributed.shape[0]) - 1):
        globals()["p_" + str(j)].append(p_distributed[i][j])


plt.figure(4)
for j in range(p_distributed.shape[1]):
    plt.plot(t, globals()["p_" + str(j)],'grey')
plt.plot(t, p_20,'chartreuse', label='bus 21')
plt.plot(t, p_19,'deepskyblue', label='bus 20')
plt.plot(t, p_21,'red', label='bus 22')
axes = plt.gca()
#axes.set_ylim([0.97, 1.08])
plt.xlabel("Time [h]")
plt.ylabel("Active Power Batt [W]")
plt.legend()
#w, h = plt.figaspect(2.)
#plt.figure(figsize=(w,h))
plt.savefig('/home/ubuntu/covee-control/plots/active_power_batt.eps')
plt.savefig('/home/ubuntu/covee-control/plots/active_power_batt.png')

# # LOAD
# # ============================================================
# cwd = os.getcwd()
# wd = os.path.join(cwd, 'csv_files/Profiles/Simple_test_profiles')
# wd.replace("\\", "/")
# with open(os.path.join(wd, 'LOAD_profile_LV_SOGNO.csv')) as csv_file:
#     load = csv.reader(csv_file, delimiter=',')
#     x = list(load)
#     load = np.array(x[0:2160]).astype("float")*P_base

# for j in range(load.shape[1]):
#     globals()["Load_" + str(j)] = []
#     for i in range(int(load.shape[0]) - 1):
#         globals()["Load_" + str(j)].append(load[i][j])

# plt.figure(5)
# # for j in range(load.shape[1]):
# #     plt.plot(t, globals()["Load_" + str(j)],'grey')
# plt.plot(t, Load_11,'chartreuse', label='Load 12')
# plt.plot(t, Load_15,'deepskyblue', label='Load 16')
# plt.plot(t, Load_19,'red', label='Load 20')
# axes = plt.gca()
# #axes.set_ylim([0.97, 1.08])
# #plt.xlabel("Time [h]")
plt.xlabel("Iterations")
# plt.ylabel("Load [W]")
# plt.legend()
# # w, h = plt.figaspect(2.)
# # plt.figure(figsize=(w,h))
# # plt.show()
# plt.savefig('/home/ubuntu/covee-control/plots/load.eps')
# plt.savefig('/home/ubuntu/covee-control/plots/load.png')

