"""take the world folder, rename to match the levelname.txt and zip. Change the
 zip extention to .mcworld and delete original folder"""
from zipfile import ZipFile
import os
import shutil
from open_levelname import get_world_name

def archive_world(world_dir):
    #changing so that the function checks the world name provided by the giu,
    # if the path to the levelname.txt checks out then continue,
    # else cycle through world dirs to find the right world. Got to be a better way to do this.
    
    world_name = get_world_name(os.path.join(world_dir,"levelname.txt"))
    os.rename(world_dir,world_name)
    world_dir = world_name

    with ZipFile(world_name + ".mcworld", "w") as world_archive:
        for folderName, subfolders, filenames in os.walk(world_dir):
           for filename in filenames:
               #create complete filepath of file in directory
               filePath = os.path.join(folderName, filename)
               # Add file to zip
               world_archive.write(filePath)

    shutil.rmtree(world_dir)


def restore_world(world):
    with ZipFile(world + ".mcworld", 'r') as zippy:
        zippy.extractall()

    os.remove(world + ".mcworld")

