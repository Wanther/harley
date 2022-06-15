import numpy as np
import matplotlib.pyplot as plt


def creepfracture(stress, C, a0, a1, a2, T):
    'Calculate creep fracture time'
    return (3600.00 * (10**(((a0 + a1 * np.log10(stress) + a2 * np.log10(stress) * np.log10(stress)) / T) - C)))**(-1)


def yfit(x, poly):
    return np.exp(poly(np.log(x)))


sample_name = '204D-D4-37'
Temperature = 816
N = 8000

C = 14.9249760029308  # 15.691918338
a0 = 26139.4634995320  # 27068.250719
a1 = -2341.98112181595  # -2045.2573528
a2 = -739.1914468118  # -906.37927664
T = Temperature + 273.15

time = []
stress = []
with open('creep/' + sample_name + '.csv', 'r') as file:
    content = file.readlines()
    for cont in content[1:]:
        element = cont.split(',')
        time.append(float(element[0]))
        stress.append(float(element[1]))
file.close()

del content

print('CompleteLoading')


relative_time = []

for i in range(len(time)):
    relative = time[i] - time[0] + 0.02
    relative_time.append(relative)

xx = np.array(relative_time)
# xx = np.array(time)
yy = np.array(stress)
logxx = np.log(xx)
logyy = np.log(yy)
sigma = np.ones(len(xx))
sigma[0] = 10
coeffs = np.polyfit(logxx, logyy, deg=3, w=sigma)

time_fit = np.linspace(0.02, 120+0.02, num=121)
poly = np.poly1d(coeffs)
stress_fit = yfit(time_fit, poly)

'''
creep = creepfracture(stress_fit, C, a0, a1, a2, T)
creep1 = creep.tolist()
d = np.trapz(creep1, time_fit)
creep1.clear()

exp_creep = creepfracture(yy, C, a0, a1, a2, T)
exp_time = xx + 0.02
exp_d = np.trapz(exp_creep, exp_time)


D = d * N
print(poly)
print(d)
print('D = ' + str(D))

exp_D = exp_d * N
print(exp_d)
print('D_exp = ' + str(exp_D))

f = open(sample_name + '_D_report.txt', 'w')
f.write('D' + '\n')
f.write(str(D) + '\n')
f.write('Dexp' + '\n')
f.write(str(exp_D) + '\n')
f.write('Coeffs' + '\n')
f.write(str(coeffs) + '\n')
f.write(str(poly) + '\n')
f.close()
'''
f = open(sample_name + '_FittingCurve.csv', 'w')
f.write('Time,Stress' + '\n')
for i in range(len(time_fit)):
    f.write(str(time_fit[i] + time[0]) + ',' + str(stress_fit[i]) + '\n')

f.close()


plt.figure(1)
plt.scatter(time, stress, s=30, facecolors='none', edgecolors='k', label='Experimental data')
plt.plot(time_fit + time[0], stress_fit, 'r-', linewidth=2)
plt.title(sample_name, fontsize='15')
plt.ylabel('Stress in relaxation (MPa)', fontsize='15')
plt.xlabel('Hold time (s)', fontsize='15')
# plt.xscale('log')
# plt.yscale('log')
plt.show()
