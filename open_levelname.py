
def get_world_name(file):
    """open the levelname.txt, and read the value"""
    with open(file, 'r') as f:
        world_name = f.read()
        return world_name


def change_world_name(file, name):
    """open the levelname.txt, and replace the value"""
    with open(file, 'w') as f:
        world_name = name
        f.write(world_name)

# file_name = "AnUzXbHhFgA=/levelname.txt"

# with open(file, 'r') as f:
#     name = f.read()
#     print("read file name :" + name)
#
# for i in open(file).readlines():
#     old_name = i
#     print(i)


"""change the levelname and close the file"""
# new_name = i + " -changed"
#
# with open(file, 'w') as f:
#     f.write(new_name)
