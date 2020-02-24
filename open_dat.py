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

def get_levelTags(path):
    """get all the level.dat info that needs to be a world tag and return a list, individual functions will get each tag? or should combine to one? opening and closing the file for each seems dumb"""
    return list(get_experimental(path), get_gametype(path), get_pvp(path), get_multiplayergame(path))
    pass






def get_alltags(path):
    """open level.dat and do searches for all tags, return list of tags"""

    with open(join(os.getcwd(),path), 'r') as level:
    	# get experimental tag
        file = re.sub('\n', '', level.read())
		
        is_experimental = re.search(r'(?<=experimentalgameplay).{1}', file).group(0)
        print("from level.dat got experimental value:", is_experimental)
		
        experimental_tag = "Experimental" if experimental == 1 else None
        
        # get gametype tag
        gametype = re.search(r'(?<=GameType).{1}', file).group(0)
        print("from level.dat got gametype value:", gametype)

        gametype_tag = "survival" if gametype == 0 else "creative" if gametype == 1 else "adventure" if gametype == 2 else None
		
        # get multiplayer tag
        multiplayer = re.search(r'(?<=MultiplayerGame).{1}', file).group(0)
        print("from level.dat got multiplayer value:", multiplayer)

        multiplayer_tag = "multiplayer" if multiplayer == 1 else None
		
        # get pvp tag
        pvp = re.search(r'(?<=pvp).{1}', file).group(0)
        print("from level.dat got pvp value:", pvp)

        pvp_tag = "pvp" if pvp == 1 else None
        
        # return list of tags after filtering Nones
    return list(filter(None, list(experimental_tag, gametype_tag, multiplayer_tag, pvp_tag)))






#individual functions, test above and delete these
def get_experimental(path):
    """open level.dat, find the char after experimentalgameplay and return "Experimental" if = 1"""
    with open(join(os.getcwd(),path), 'r') as level:
        file = re.sub('\n', '', level.read())


        experimental = re.search(r'(?<=experimentalgameplay).{1}', file).group(0)
        print("from level.dat got value:", experimental)

    return "Experimental" if experimental == 1 else None
        
        
def get_gametype(path):
    """open level.dat, find the char after GameType and return 0="survival", 1="creative", 2="adventure" """
    pass
    
    

def get_multiplayergame(path):
    """open level.dat, find the char after MultiplayerGame and return 0=None, 1="multiplayer" """
    pass 
    
    
def get_pvp(path):
    """open level.dat, find the char after pvp return 0=None, 1="pvp" """
    pass 
    
