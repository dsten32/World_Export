"""read a dir and create a list of world objects from the contents"""
import os
from os.path import isfile, join, getctime, getmtime
from open_levelname import get_world_name, change_world_name
import time
from WorldClass import World

def getWorlds():
    level_name_file = "levelname.txt"
    level_dat_file = "level.dat"
    world_params = "world_manager_params.ini"
    world_dirName = "minecraft_worlds"
    world_list = []
    archived_worlds_list = []

    for foldername in os.listdir(world_dirName):
        """gets the contents of the world dir and creates world objects
        need to make created and modified times to account for daylight savings"""
        #somehow lost the
        if not isfile(join(world_dirName, foldername)):
            world_name = get_world_name(join(*[world_dirName, foldername, level_name_file]))
            world_obj = World(world_name, created=getctime(join(*[world_dirName, foldername])), modified=getmtime(join(*[world_dirName, foldername, level_dat_file])))
            tags_path = join(*[world_dirName, foldername, world_params])
            tags = []
            #if the world_manager_params file exists get the tags from it
            if os.path.exists(tags_path):
                with open(join(*[world_dirName, foldername, world_params]), 'r') as params:
                    for line in params:
                        if line.startswith('TAGS='):
                            # tags = params.readline()
                            tags = [tag for tag in line[line.find('[')+1:line.find(']')].split(',')]
                            world_obj.tags.extend(tags)
                            # break

            #add the world directory name as an instance variable, will use later for getting the image
            world_obj.dir = foldername
            world_list.append(world_obj)
            # print(foldername, world_name)
        elif foldername.split(".")[1] == "mcworld":
            archived_worlds_list.append(foldername.split(".")[0])

    #sort worlds by name
    world_list.sort() #key=lambda world: world.name
    return world_list

# for world in world_list:
#     print(world.name, world.created, world.last_used, world.tags)
#
# print("---")
#
# #sort by created date
# world_list.sort(key=lambda world: world.created_seconds) #key=lambda world: world.name
# for world in world_list:
#     print(world.name, world.created, world.last_used, world.tags)
#
# print("---")
# #sort by used date
# world_list.sort(key=lambda world: world.modified) #key=lambda world: world.name
# for world in world_list:
#     print(world.name, world.created, world.last_used, world.tags)
#
# for arc in archived_worlds_list:
#     print(arc)
def getArchived():
    level_name_file = "levelname.txt"
    level_dat_file = "level.dat"
    world_dirName = "minecraft_worlds"
    world_list = []
    archived_worlds_list = []

    for foldername in os.listdir(world_dirName):
        """gets the contents of the world dir and creates world objects
        need to make created and modified times to account for daylight savings"""
        if isfile(join(world_dirName, foldername)) and foldername.split(".")[1] == "mcworld":
            # world_name = get_world_name(join(*[world_dirName, foldername, level_name_file]))
            # world_obj = World(world_name, created=getctime(join(*[world_dirName, foldername])), modified=getmtime(join(*[world_dirName, foldername, level_dat_file])))
            # world_obj.tags.append("personal")
            # world_list.append(world_obj)
            # print(foldername, world_name)
        # elif foldername.split(".")[1] == "mcworld":
            archived_worlds_list.append((foldername.split(".")[0],time.asctime(time.gmtime(getmtime(join(*[world_dirName, foldername]))))))

    #sort worlds by name
    archived_worlds_list.sort() #key=lambda world: world.name
    return archived_worlds_list
