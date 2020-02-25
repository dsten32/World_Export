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
    # could create a lookup table of world names and paths on start up? could speed things up when hundreds of worlds,
    # one file to open and read instead of hundreds.
    # original_world_name = ''
    if exists(join(world_name, "levelname.txt")):
        print("world found:", join(world_name, "levelname.txt"))
        # get world name from levelname.txt, remove '§.' modifiers and compare to world to archive
        original_world_name = get_world_name(join(world_name, "levelname.txt"))
        world_name = re.sub('Â§.', '', original_world_name)
        world_path = world_name
        # os.rename(join(world_dirName,world_dir),join(world_dirName,world_name))
        # look to see if archived world with same name exists
        if exists(world_path + ".mcworld"):
            while exists(world_path + ".mcworld"):
                if re.search('\(\d\)', world_path):  # == "world (3).mcworld":
                    print("result of regex:", re.search('(\()(\d)(\))', world_path).group(2))

                    world_path = re.sub(re.search('\(\d\)', world_path).group(0),
                                        str(int(re.search('(\()(\d)(\))', world_path).group(2)) + 1), world_path)

                    original_world_name = re.sub(re.search('\(\d\)', original_world_name).group(0),
                                        str(int(re.search('(\()(\d)(\))', original_world_name).group(2)) + 1), original_world_name)
                    print("after search and replace:", world_path)
                else:
                    world_path += " (1)"
                    original_world_name += " (1)"

        # rename dir to account for existing archived worlds with same name
        os.rename(world_name, world_path)
        print(join(world_path + "\levelname.txt"))
        # update world name in levelname.txt
        print(exists(world_path + "\levelname.txt"))
        with open(world_path + "\levelname.txt", 'w') as f:
            updated_world_name = original_world_name
            f.write(updated_world_name)

        with ZipFile(world_path + ".mcworld", "w") as world_archive:
            for folderName, subfolders, filenames in os.walk(world_path):
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
    world_dir = world
    # print(os.getcwd())
    # check we are in theright dir
    #todo, use the full file path to world folder
    if not os.getcwd().split('\\')[-1] == world_dirName:
        os.chdir(world_dirName)
    #--------------------------

    if exists(world_dir):
        while exists(world_dir):
            if re.search('\(\d\)', world_dir):  # == "world (3).mcworld":
                print("result of regex:", re.search('(\()(\d)(\))', world_dir).group(2))

                world_dir = re.sub(re.search('\(\d\)', world_dir).group(0),
                                    str(int(re.search('(\()(\d)(\))', world_dir).group(2)) + 1), world_dir)
                print("after search and replace:", world_dir)
            else:
                world_dir += " (1)"

    #-------------------
    #todo, rename folder in zipfile to world_dir, then extract else will
    # overwrite the world we've just determined already exists
    with ZipFile(world + ".mcworld", 'r') as zippy:
        zippy.extractall()

    os.remove(world + ".mcworld")

