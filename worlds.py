"""read a dir and create a list of world objects from the contents"""
import re
import os
from os.path import isfile, join, getctime, getmtime
from open_levelname import get_world_name, change_world_name
from open_dat import get_lastPlayed, get_alltags, get_archived_level_data, get_loaded_level_data
import time
from WorldClass import World

world_dirName = "C:/Users/dsten/PycharmProjects/World_Export/minecraft_worlds/"
# "minecraft_worlds"


def getWorlds():
    level_name_file = "levelname.txt"
    level_dat_file = "level.dat"
    world_params = "world_manager_params.ini"
    world_list = []
    archived_worlds_list = []

    for foldername in os.listdir(world_dirName):
        """gets the contents of the world dir and creates world objects
		need to make created and modified times to account for daylight savings"""
        if not isfile(join(world_dirName, foldername)):
            # change world name to remove any '§.' modifiers before adding to world object

            world_name = re.sub('Â§.', '', get_world_name(join(*[world_dirName, foldername, level_name_file])))
            world_data = get_loaded_level_data(join(*[world_dirName, foldername]))
            # debug get last played
            # print(join(*[world_dirName, foldername, level_dat_file]))
            world_obj = World(world_data[0], created=getctime(join(*[world_dirName, foldername])), modified=world_data[1])  # modified=getmtime(join(*[world_dirName, foldername, level_dat_file])))
            tags_path = join(*[world_dirName, foldername, world_params])
            tags = []
            # if the world_manager_params file exists get the tags from it
            if os.path.exists(tags_path):
                with open(join(*[world_dirName, foldername, world_params]), 'r') as params:
                    for line in params:
                        if line.startswith('TAGS='):
                            # tags = params.readline()
                            tags = [tag.strip() for tag in line[line.find('[') + 1:line.find(']')].split(',')]
                            world_obj.tags.extend(tags)

            # add level.dat values to world_obj tag list
            world_obj.tags.extend(get_alltags(join(*[world_dirName, foldername, level_dat_file])))
            world_obj.tags.extend(world_data[2])

            # todo add the world directory name as an instance variable, will use later for getting the image
            world_obj.dir = foldername
            world_list.append(world_obj)
        elif foldername.split(".")[-1] == "mcworld":
            archived_worlds_list.append(foldername[0:-8])

    # sort worlds by name
    world_list.sort()
    return world_list



def getArchived():
    level_name_file = "levelname.txt"
    level_dat_file = "level.dat"
    world_dirName = "C:/Users/dsten/PycharmProjects/World_Export/minecraft_worlds/"  # "minecraft_worlds"

    world_list = []
    archived_worlds_list = []

    # todo world icon image
    for foldername in os.listdir(world_dirName):
        """gets the contents of the world dir and creates world objects
		need to make created and modified times to account for daylight savings"""
        if isfile(join(world_dirName, foldername)) and foldername.split(".")[-1] == "mcworld":
            world_data = get_archived_level_data(join(*[world_dirName, foldername]))
            world_obj = World(world_data[0], created=getctime(join(*[world_dirName, foldername])), modified=world_data[1])
            world_obj.tags.extend(world_data[2])
            archived_worlds_list.append(world_obj)

    # sort worlds by name
    archived_worlds_list.sort()
    return archived_worlds_list
