import numpy as np
import pandas as pd
import os
from os.path import join
import re
from datetime import datetime


# loadfile = np.fromfile('level.dat')

# loadtext = np.loadtxt('level.dat')
# datContent = [i.strip().split() for i in open("level.dat").readlines()]
#
# datContent = pd.read_csv('level.dat')
# open the level.dat and read each line. still need to correct some characters that
# are not correctly formatting to hex eg Ã, Ï, ], Í, Ì
# for i in open("levelS.dat").readlines():
#     print(i.split())


# print(datContent)
def get_lastPlayed(path):
    print("last played function dir:", os.getcwd())
    print(join(os.getcwd(),path))
    """open level.dat, find the 4 chars after LastPlayed and convert to datetime and return"""
    with open(join(os.getcwd(),path), 'r') as level:
        file = re.sub('\n', '', level.read())


        last_played = re.search(r'(?<=LastPlayed).{4}', file).group(0)
        print("from level.dat got value:", last_played)

        hexarr = []
        for c in last_played:
            hexarr.insert(0, hex(ord(c)).lstrip("0x"))

        timestamp = int("".join(hexarr), 16)
        daime = datetime.fromtimestamp(timestamp)

        return timestamp
