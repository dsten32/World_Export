import numpy as np
import pandas as pd
import os
from os.path import join
import re
from datetime import datetime


# print(datContent)
def get_lastPlayed(path):
    # print("last played function dir:", os.getcwd())
    # print(join(os.getcwd(), path))
    """open level.dat, find the 4 chars after LastPlayed and convert to datetime and return"""
    with open(join(os.getcwd(), path), 'r') as level:
        file = re.sub('\n', '', level.read())

        last_played = re.search(r'(?<=LastPlayed).{4}', file).group(0)
        # print("from level.dat got value:", last_played)

        hexarr = []
        for c in last_played:
            hexarr.insert(0, hex(ord(c)).lstrip("0x"))

        timestamp = int("".join(hexarr), 16)
        daime = datetime.fromtimestamp(timestamp)

        return timestamp


def get_alltags(path):
    """open level.dat and do searches for all tags, return list of tags"""
    with open(join(os.getcwd(), path), 'r') as level:
        # read in level.dat file, remove any newline chars so the re.search will work
        file = re.sub('\n', '', level.read())

        # get experimental tag hex value, via translating to character ord,
        # then to hex value then strip 0x off left side and casting to int using base 16
        is_experimental_hex = re.search(r'(?<=experimentalgameplay).{1}', file).group(0)
        is_experimental = 0 if is_experimental_hex == '\x00' else int(hex(ord(is_experimental_hex)).lstrip("0x"), 16)
        experimental_tag = "Experimental" if is_experimental == 1 else None
        # print("from "+path+" got experimental value:", experimental_tag)

        # get gametype tag hex value, via translating to character ord,
        # then to hex value then strip 0x off left side and casting to int using base 16
        game_type_hex = re.search(r'(?<=GameType).{1}', file).group(0)
        gametype = 0 if game_type_hex == '\x00' else int(hex(ord(game_type_hex)).lstrip("0x"), 16)
        gametype_tag = "Survival" if gametype == 0 else "creative" if gametype == 1 else "adventure" if gametype == 2 else None
        # print("from "+path+" got gametype value:", gametype_tag)

        # get multiplayer tag hex value, via translating to character ord,
        # then to hex value then strip 0x off left side and casting to int using base 16
        multiplayer_hex = re.search(r'(?<=MultiplayerGame).{1}', file).group(0)
        multiplayer = 0 if multiplayer_hex == '\x00' else int(hex(ord(multiplayer_hex)).lstrip("0x"), 16)
        multiplayer_tag = "Multiplayer" if multiplayer == 1 else None
        # print("from "+path+" got multiplayer value:", multiplayer_tag)

        # get pvp tag hex value, via translating to character ord,
        # then to hex value then strip 0x off left side and casting to int using base 16
        pvp_hex = re.search(r'(?<=pvp).{1}', file).group(0)
        pvp = 0 if pvp_hex == '\x00' else int(hex(ord(pvp_hex)).lstrip("0x"), 16)
        pvp_tag = "PvP" if pvp == 1 else None
        # print("from "+path+" got pvp value:", pvp_tag)

        # print("all together now:", list((experimental_tag, gametype_tag, multiplayer_tag, pvp_tag)))
        # return list of tags after filtering Nones
    return list(filter(None, list((experimental_tag, gametype_tag, multiplayer_tag, pvp_tag))))

