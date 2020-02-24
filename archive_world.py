"""take the world folder, rename to match the levelname.txt and zip. Change the
 zip extention to .mcworld and delete original folder"""
from zipfile import ZipFile
import re
import os
from os.path import isfile, join, exists
import shutil
from open_levelname import get_world_name
from worlds import world_dirName


def archive_world(world_name):
    # check if we are in the worlds folder
    #todo should change this so that the user's worlds folder in saved in some sort of persistence and then use full path
    if not os.getcwd().split('\\')[-1] == world_dirName:
        os.chdir(world_dirName)
    print("Starting archiving")

    # changing so that the function checks the world name provided by the gui,
    # if the path to the levelname.txt checks out then continue,
    # else cycle through world dirs to find the right world. Got to be a better way to do this.
    if exists(join(world_name, "levelname.txt")):
        print("world found")
        # get world name from levelname.txt, remove '§.' modifiers and compare to world to archive
        world_name = re.sub('Â§.', '', get_world_name(join(world_name, "levelname.txt")))
        world_path = world_name
        # os.rename(join(world_dirName,world_dir),join(world_dirName,world_name))
        # look to see if archived world with same name exists
        if exists(world_path + ".mcworld"):
            pass
        else:
            with ZipFile(world_path + ".mcworld", "w") as world_archive:
                for folderName, subfolders, filenames in os.walk(world_name):
                    for filename in filenames:
                        # create complete filepath of file in directory
                        filePath = os.path.join(folderName, filename)
                        # Add file to zip
                        world_archive.write(filePath)
        # delete world folder after creating zipped file
        print(world_path)
        shutil.rmtree(world_path)
    else:
        for foldername in os.listdir():
            if not os.path.isfile(os.path.join(foldername)):
                # get world name from levelname.txt, remove '§.' modifiers and compare to world to archive
                world_name = re.sub('Â§.', '', get_world_name(join(*[foldername, "levelname.txt"])))
                if world_name == world_name:
                    os.rename(foldername, world_name)
                    world_path = world_name
                    with ZipFile(world_path + ".mcworld", "w") as world_archive:
                        for folderName, subfolders, filenames in os.walk(world_path):
                           for filename in filenames:
                               #create complete filepath of file in directory
                               filePath = os.path.join(folderName,filename)
                               print("file:",filePath)
                               # Add file to zip
                               world_archive.write(filePath)


def restore_world(world):
    print(os.getcwd())
    if not os.getcwd().split('\\')[-1] == world_dirName:
        os.chdir(world_dirName)
    with ZipFile(world + ".mcworld", 'r') as zippy:
        zippy.extractall()

    os.remove(world + ".mcworld")

