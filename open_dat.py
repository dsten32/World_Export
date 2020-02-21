import numpy as np
import pandas as pd

# loadfile = np.fromfile('level.dat')

# loadtext = np.loadtxt('level.dat')
# datContent = [i.strip().split() for i in open("level.dat").readlines()]
#
# datContent = pd.read_csv('level.dat')
# open the level.dat and read each line. still need to correct some characters that are not correctly
# formatting to hex eg Ã, Ï, ], Í, Ì
for i in open("levelS.dat").readlines():
    print(i.split())


# print(datContent)