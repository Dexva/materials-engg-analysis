# Imports
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
import csv

# Define constants
PLA_CROSS_AREA = 0.00248 * 0.00173 # DAVIS - PLA
PLA_DOGBONE_LENGTH = 0.02166
ABS_CROSS_AREA = 0.00249 * 0.00166 # NEO - ABS
ABS_DOGBONE_LENGTH = 0.02386

# Read from .csv file
pla_strain = []
pla_stress = []
abs_strain = []
abs_stress = []

with open('ENGG X-MAGPANTAY.csv') as csv_file: # PLA Data
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            pass
        else:
            pla_strain.append(float(row[1])/PLA_DOGBONE_LENGTH)
            pla_stress.append(float(row[2])/PLA_CROSS_AREA)
        line_count += 1
pla_strain = np.array(pla_strain)
pla_stress = np.array(pla_stress)

with open('ENGG X-MAMARIL.csv') as csv_file: # ABS Data
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            pass
        else:
            abs_strain.append(float(row[1])/ABS_DOGBONE_LENGTH)
            abs_stress.append(float(row[2])/ABS_CROSS_AREA)
        line_count += 1
abs_strain = np.array(abs_strain)
abs_stress = np.array(abs_stress)

# Finding peak stress (y-value)
max_pla_stress = pla_stress[0] 
max_pla_index = 0
for i in range(len(pla_stress)):
    if pla_stress[i] > max_pla_stress:
        max_pla_stress = pla_stress[i]
        max_pla_index = i

max_abs_stress = abs_stress[0] 
max_abs_index = 0
for i in range(len(abs_stress)):
    if abs_stress[i] > max_abs_stress:
        max_abs_stress = abs_stress[i]
        max_abs_index = i

# Set labels
plt.title("Stress-Strain Plot for PLA and ABS Samples")
plt.xlabel("Strain [dimensionless]")
plt.ylabel("Stress [N m^-2]")

# Plot stress-strain curves
plt.plot(pla_strain,pla_stress,linewidth=3.0,color='orange') # PLA plot
plt.plot(abs_strain,abs_stress,linewidth=3.0,color='blue') # ABS plot

# Plot approximated elastic regions and regression lines
pla_strain_reg = []
pla_stress_reg = []
for i in range(max_pla_index):
    if pla_stress[i] > 0.1E7:
        pla_strain_reg.append(pla_strain[i])
        pla_stress_reg.append(pla_stress[i])
coef = np.polyfit(pla_strain_reg, pla_stress_reg, 1)
print(coef)
poly1d_fn = np.poly1d(coef)
plt.plot(pla_strain_reg, pla_stress_reg, 'y.', pla_strain_reg, poly1d_fn(pla_strain_reg), '--k', linewidth=3.0)

abs_strain_reg = []
abs_stress_reg = []
for i in range(max_abs_index):
    if abs_stress[i] > 0.1E7:
        abs_strain_reg.append(abs_strain[i])
        abs_stress_reg.append(abs_stress[i])
coef2 = np.polyfit(abs_strain_reg, abs_stress_reg, 1)
print(coef2)
poly1d_fn2 = np.poly1d(coef2)
plt.plot(abs_strain_reg, abs_stress_reg, 'y.', abs_strain_reg, poly1d_fn2(abs_strain_reg), '--k', linewidth=3.0)

# Plot ultimate tensile strength points and lines
plt.axvline(x=pla_strain[max_pla_index], color='orange', linestyle='dotted') # Max PLA stress vertical line
plt.axvline(x=abs_strain[max_abs_index], color='blue', linestyle='dotted') # Max ABS stress vertical line
plt.axhline(y=pla_stress[max_pla_index], color='orange', linestyle='dotted') # Max PLA stress horizontal line
plt.axhline(y=abs_stress[max_abs_index], color='blue', linestyle='dotted') # Max ABS stress horizontal line
plt.plot(pla_strain[max_pla_index], pla_stress[max_pla_index],'ro') # Max stress point
plt.plot(abs_strain[max_abs_index], abs_stress[max_abs_index],'ro') # Max stress point
plt.legend(["PLA", "ABS"], loc ="upper right")

plt.show()

## Percent elongation readout
# for i in range(len(pla_strain)): # PLA
#     if i > max_pla_index and pla_stress[i]<0.1E7:
#         print(pla_strain[i])
#         break

# for i in range(len(abs_strain)): # ABS
#     if i > max_abs_index and abs_stress[i]<0.1E7:
#         print(abs_strain[i])
#         break

## Ultimate tensile strength readout
# print("PLA:")
# print(pla_strain[max_pla_index])
# print(pla_stress[max_pla_index])
# print("ABS:")
# print(abs_strain[max_abs_index])
# print(abs_stress[max_abs_index])
