from collections import defaultdict
import math
import os
# import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# Prefix 'd': dictionary

sample = 'E0326-2-1'
dia = 169
datadir = os.environ['appdata'] + r'\Instr\Agilent4156C'

area = math.pi * (dia/2)**2  # um^2
d_V = defaultdict(list)  # Voltage
d_J = defaultdict(list)  # Current density (A/um^2)
d_RA = defaultdict(list)  # Resistance area product (ohm um^2)
for fname in [fname_all for fname_all in os.listdir(datadir) if
              fname_all.startswith('double-sweep') and
              'D{}'.format(dia) in fname_all and
              sample in fname_all]:
    with open(datadir + '\\' + fname) as f:
        tmp = f.name.split('_')
        X = int(tmp[3][1:])
        Y = int(tmp[4][1:])
        D = float(tmp[5][1:])
        read = f.read().split()
        newV = [float(t) for t in read[0].split(',')]
        newJ = [float(J)/area for J in read[1].split(',')]
        newR = [(V/J if abs(V) > 0.010 else None) for (V, J) in zip(newV, newJ)]
        d_V[(X, Y, D)] += newV
        d_J[(X, Y, D)] += newJ
        d_RA[(X, Y, D)] += newR
        print(X, Y, D)


Xmin = 1
Xmax = 11
Ymin = 1
Ymax = 4

numX = Xmax - Xmin + 1
numY = Ymax - Ymin + 1
f, axarr = plt.subplots(numY, numX, figsize=(numX, numY), facecolor='w')
f.subplots_adjust(top=1, bottom=0, left=0, right=1, wspace=0, hspace=0)
for (rowi, coli) in [(rowi, coli) for rowi in range(numY) for coli in range(numX)]:
    print(rowi, coli)
    # (rowi, coli) X, Y
    # (00)XminYmax ...              (09)XmaxYmax
    # ...
    # (08)Xmin(Ymin+1) ...
    # (09)XminYmin 19(Xmin+1)Ymin ... (99)XmaxYmin
    X = coli + Xmin
    Y = Ymax - rowi
    p = axarr[rowi, coli].plot(d_V[(X, Y, dia)], d_J[(X, Y, dia)], 'b')
    # p = axarr[rowi, coli].plot(d_V[(X, Y, dia)], d_RA[(X, Y, dia)], 'r')
    axarr[rowi, coli].set_xticks([])
    axarr[rowi, coli].set_yticks([])
    axarr[rowi, coli].set_xlim([-0.5, 0.5])
    axarr[rowi, coli].set_ylim([-1e-11, 1e-11])  # J [A/um^2]
    # axarr[rowi, coli].set_ylim([0, 2e12])  # RA [ohm um^2]
# plt.show()
plt.savefig(os.path.expanduser('~') + r'\Desktop\tmp.png', dpi=300, transparent=True)

print(0)
