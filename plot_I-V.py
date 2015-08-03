from collections import defaultdict
import os
# import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# Prefix 'd': dictionary

datadir = os.environ['appdata'] + r'\Instr\Agilent4156C'
d_V = defaultdict(list)  # Voltage
d_I = defaultdict(list)  # Current
d_R = defaultdict(list)  # Resistance
for fname in [fname_all for fname_all in os.listdir(datadir) if fname_all.startswith('double-sweep')]:
    with open(datadir + '\\' + fname) as f:
        tmp = f.name.split('_')
        X = int(tmp[3][1:])
        Y = int(tmp[4][1:])
        D = float(tmp[5][1:])
        V = float(tmp[6].split('V')[0])  # '0.1V.csv' -> 0.1
        read = f.read().split()
        newV = [float(t) for t in read[0].split(',')]
        newI = [float(I) for I in read[1].split(',')]
        newR = [V/I for I in newI if I != 0]
        d_V[(X, Y, D, V)].append(newV)
        d_I[(X, Y, D, V)].append(newI)
        d_R[(X, Y, D, V)] += newR

d_R_ave = {}
for XYDv, value in d_R.items():
    d_R_ave[XYDv] = np.mean(value)



# http://matplotlib.org/examples/pylab_examples/subplots_demo.html
# plt.scatter( [ [1,2], [3,4] ] , [ [5,6], [7,8]  ]  )
# plt.semilogy( [ [1,2,3], [4,5,6] ] , [ [7,8,9], [10,11,12] ] )
# plt.semilogy( [ [1,2],[3,4],[5,6] ] )
# plt.semilogy( [1,2],[3,4],[5,6] )  # error
# plt.semilogy( [ [1,2],[3,4] ] )
# plt.semilogy( [1,2],[3,4] )
voltage = 1e-3
dia = 56.3
f, axarr = plt.subplots(4, 10, sharex=True)
f.patch.set_alpha(0.)
# X2Y4 X3Y4 ... X11Y4
# X2Y3 X3Y3 ...
# X2Y2 X3Y2 ...
# X2Y1 X3Y1 ... X11Y1
# plt.title('E0326-2-1 (D 5.54um, X 2-11, Y 1-4) I(A) vs t(s)')
for (rowi, coli) in [(rowi, coli) for rowi in range(4) for coli in range(10)]:
    xi = coli + 2
    yi = 4 - rowi
    for (t, I) in zip(d_V[(xi, yi, dia, voltage)], d_I[(xi, yi, dia, voltage)]):
        try:
            axarr[rowi, coli].semilogy(t, I)
        except Exception:
            print('negative value on rowi:{} coli:{} xi:{} yi:{}'.format(rowi, coli, xi, yi))
# f.subplots_adjust(hspace=0)
f.subplots_adjust(wspace=0)
# f.subplots_adjust(0,0)
# plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
plt.show()
print(0)



# +1mV
fig = plt.figure()
fig.patch.set_alpha(0.)
ax = plt.gca()
ax.set_yscale('log')
plt.title('E0326-2-1 (X=1: Fe 0nm, X=10: 5.45nm)')
plt.xlabel('X')
plt.ylabel('Resistance at 1mV')
for (area, color_) in zip([5.54, 16.7, 56.3], ('r', 'g', 'b')):
    for (XYDv, R_ave) in [(XYDv, R_ave) for (XYDv, R_ave) in d_R_ave.items() if XYDv[2] == area and XYDv[3] == 1e-3 and R_ave > 0]:
        ax.scatter(XYDv[0], R_ave, color=color_)
plt.show()

# -1mV
fig = plt.figure()
fig.patch.set_alpha(0.)
ax = plt.gca()
ax.set_yscale('log')
plt.title('E0326-2-1 (X=1: Fe 0nm, X=10: 5.45nm)')
plt.xlabel('X')
plt.ylabel('Resistance at -1mV')
for (area, color_) in zip([5.54, 16.7, 56.3], ('r', 'g', 'b')):
    for (XYDv, R_ave) in [(XYDv, R_ave) for (XYDv, R_ave) in d_R_ave.items() if XYDv[2] == area and XYDv[3] == -1e-3 and R_ave > 0]:
        ax.scatter(XYDv[0], R_ave, color=color_)
plt.show()

for (XYDv, R_ave) in [(XYDv, R_ave) for (XYDv, R_ave) in d_R_ave.items() if R_ave <= 0]:
    print('Resistance{0}: {1}'.format(XYDv, R_ave))

print(1)


# # debug
# ContactTest_20150716-190541_E0326-2-1_X2_Y2_D5.54_p1mV.csv
# t0 = [0.0, 0.19, 0.3, 0.41, 0.52, 0.63, 0.74, 0.85, 0.96, 1.07, 1.18, 1.29, 1.4, 1.51, 1.62, 1.73, 1.84, 1.95, 2.06, 2.17, 2.28, 2.39, 2.5, 2.61, 2.72, 2.83, 2.94, 3.05, 3.16, 3.27, 3.38, 3.49, 3.6, 3.71, 3.82, 3.93, 4.04, 4.15, 4.26, 4.37, 4.48, 4.59, 4.7, 4.81, 4.92, 5.03, 5.14, 5.25, 5.36, 5.47, 5.58, 5.69, 5.8, 5.91, 6.02, 6.13, 6.24, 6.35, 6.46, 6.57, 6.68, 6.79, 6.9, 7.01, 7.12, 7.23, 7.34, 7.45, 7.56, 7.67, 7.78, 7.89, 8.0, 8.11, 8.22, 8.33, 8.44, 8.55, 8.66, 8.77, 8.88, 8.99, 9.1, 9.21, 9.32, 9.43, 9.54, 9.65, 9.76, 9.87, 9.98, 10.09, 10.2, 10.31, 10.42, 10.53, 10.64, 10.75, 10.86, 10.97]
# i0 = [1.49e-12, 1.5e-12, 1.45e-12, 1.45e-12, 1.46e-12, 1.43e-12, 1.47e-12, 1.48e-12, 1.48e-12, 1.5e-12, 1.46e-12, 1.48e-12, 1.45e-12, 1.46e-12, 1.47e-12, 1.49e-12, 1.48e-12, 1.46e-12, 1.47e-12, 1.47e-12, 1.46e-12, 1.47e-12, 1.47e-12, 1.46e-12, 1.48e-12, 1.49e-12, 1.5e-12, 1.46e-12, 1.48e-12, 1.46e-12, 1.48e-12, 1.45e-12, 1.47e-12, 1.47e-12, 1.48e-12, 1.47e-12, 1.48e-12, 1.46e-12, 1.47e-12, 1.45e-12, 1.46e-12, 1.47e-12, 1.49e-12, 1.46e-12, 1.48e-12, 1.46e-12, 1.47e-12, 1.46e-12, 1.48e-12, 1.46e-12, 1.46e-12, 1.44e-12, 1.46e-12, 1.47e-12, 1.49e-12, 1.48e-12, 1.46e-12, 1.45e-12, 1.48e-12, 1.43e-12, 1.47e-12, 1.47e-12, 1.47e-12, 1.48e-12, 1.46e-12, 1.44e-12, 1.45e-12, 1.47e-12, 1.46e-12, 1.47e-12, 1.47e-12, 1.45e-12, 1.45e-12, 1.45e-12, 1.45e-12, 1.46e-12, 1.45e-12, 1.47e-12, 1.44e-12, 1.46e-12, 1.45e-12, 1.5e-12, 1.47e-12, 1.48e-12, 1.46e-12, 1.48e-12, 1.47e-12, 1.45e-12, 1.47e-12, 1.46e-12, 1.46e-12, 1.45e-12, 1.43e-12, 1.45e-12, 1.45e-12, 1.45e-12, 1.48e-12, 1.46e-12, 1.44e-12, 1.46e-12]
# ContactTest_20150716-190715_E0326-2-1_X2_Y2_D5.54_p1mV.csv
# t1 = [0,0.19,0.3,0.41,0.52,0.63,0.74,0.85,0.96,1.07,1.18,1.29,1.4,1.51,1.62,1.73,1.84,1.95,2.06,2.17,2.28,2.39,2.5,2.61,2.72,2.83,2.94,3.05,3.16,3.27,3.38,3.49,3.6,3.71,3.82,3.93,4.04,4.15,4.26,4.37,4.48,4.59,4.7,4.81,4.92,5.03,5.14,5.25,5.36,5.47,5.58,5.69,5.8,5.91,6.02,6.13,6.24,6.35,6.46,6.57,6.68,6.79,6.9,7.01,7.12,7.23,7.34,7.45,7.56,7.67,7.78,7.89,8,8.11,8.22,8.33,8.44,8.55,8.66,8.77,8.88,8.99,9.1,9.21,9.32,9.43,9.54,9.65,9.76,9.87,9.98,10.09,10.2,10.31,10.42,10.53,10.64,10.75,10.86,10.97]
# i1 = [1.52E-12,1.49E-12,1.5E-12,1.52E-12,1.47E-12,1.48E-12,1.52E-12,1.46E-12,1.47E-12,1.51E-12,1.46E-12,1.46E-12,1.44E-12,1.45E-12,1.47E-12,1.47E-12,1.46E-12,1.45E-12,1.48E-12,1.46E-12,1.46E-12,1.46E-12,1.46E-12,1.46E-12,1.45E-12,1.44E-12,1.45E-12,1.45E-12,1.44E-12,1.44E-12,1.44E-12,1.43E-12,1.46E-12,1.44E-12,1.42E-12,1.44E-12,1.43E-12,1.41E-12,1.44E-12,1.45E-12,1.44E-12,1.4E-12,1.45E-12,1.43E-12,1.44E-12,1.42E-12,1.42E-12,1.41E-12,1.43E-12,1.45E-12,1.43E-12,1.41E-12,1.43E-12,1.4E-12,1.43E-12,1.44E-12,1.4E-12,1.4E-12,1.41E-12,1.42E-12,1.43E-12,1.41E-12,1.45E-12,1.41E-12,1.42E-12,1.45E-12,1.44E-12,1.42E-12,1.43E-12,1.4E-12,1.4E-12,1.37E-12,1.4E-12,1.41E-12,1.42E-12,1.39E-12,1.42E-12,1.38E-12,1.4E-12,1.39E-12,1.44E-12,1.39E-12,1.39E-12,1.41E-12,1.43E-12,1.44E-12,1.39E-12,1.42E-12,1.41E-12,1.4E-12,1.4E-12,1.38E-12,1.42E-12,1.4E-12,1.38E-12,1.36E-12,1.38E-12,1.38E-12,1.39E-12,1.42E-12]
# ContactTest_20150716-190754_E0326-2-1_X2_Y2_D5.54_p1mV.csv
# t2 = [0,0.19,0.3,0.41,0.52,0.63,0.74,0.85,0.96,1.07,1.18,1.29,1.4,1.51,1.62,1.73,1.84,1.95,2.06,2.17,2.28,2.39,2.5,2.61,2.72,2.83,2.94,3.05,3.16,3.27,3.38,3.49,3.6,3.71,3.82,3.93,4.04,4.15,4.26,4.37,4.48,4.59,4.7,4.81,4.92,5.03,5.14,5.25,5.36,5.47,5.58,5.69,5.8,5.91,6.02,6.13,6.24,6.35,6.46,6.57,6.68,6.79,6.9,7.01,7.12,7.23,7.34,7.45,7.56,7.67,7.78,7.89,8,8.11,8.22,8.33,8.44,8.55,8.66,8.77,8.88,8.99,9.1,9.21,9.32,9.43,9.54,9.65,9.76,9.87,9.98,10.09,10.2,10.31,10.42,10.53,10.64,10.75,10.86,10.97]
# i2 = [1.45E-12,1.41E-12,1.47E-12,1.41E-12,1.42E-12,1.42E-12,1.43E-12,1.44E-12,1.42E-12,1.45E-12,1.41E-12,1.42E-12,1.42E-12,1.41E-12,1.41E-12,1.42E-12,1.46E-12,1.42E-12,1.41E-12,1.41E-12,1.4E-12,1.4E-12,1.41E-12,1.42E-12,1.4E-12,1.39E-12,1.41E-12,1.4E-12,1.4E-12,1.39E-12,1.43E-12,1.37E-12,1.41E-12,1.38E-12,1.42E-12,1.39E-12,1.4E-12,1.41E-12,1.4E-12,1.39E-12,1.4E-12,1.38E-12,1.41E-12,1.37E-12,1.39E-12,1.4E-12,1.39E-12,1.39E-12,1.4E-12,1.39E-12,1.38E-12,1.39E-12,1.36E-12,1.4E-12,1.38E-12,1.38E-12,1.36E-12,1.39E-12,1.41E-12,1.38E-12,1.39E-12,1.38E-12,1.37E-12,1.39E-12,1.38E-12,1.4E-12,1.37E-12,1.38E-12,1.39E-12,1.39E-12,1.36E-12,1.37E-12,1.35E-12,1.41E-12,1.38E-12,1.32E-12,1.35E-12,1.4E-12,1.35E-12,1.36E-12,1.37E-12,1.37E-12,1.38E-12,1.38E-12,1.36E-12,1.36E-12,1.37E-12,1.36E-12,1.35E-12,1.36E-12,1.36E-12,1.35E-12,1.39E-12,1.37E-12,1.35E-12,1.34E-12,1.36E-12,1.37E-12,1.4E-12,1.35E-12]

# plt.plot(t0, i0)
# plt.plot(t1, i1)
# plt.show()
# plt.subplot2grid()
