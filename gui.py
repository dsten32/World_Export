import tkinter as tk
from tkinter import filedialog, Text, ttk
import os
from os.path import join
from worlds import getWorlds, getArchived

# set up some useful variables to be used elsewhere:
# list of loaded worlds
loaded_world_list = getWorlds()
#list of archived worlds
archived_worlds_list = getArchived()

#methods for treeview
def showLoadedTree():
    loaded_search()
    world_tags = []
    treeView.delete(*treeView.get_children())
    loaded_worlds = loaded_world_list
    for world in loaded_worlds:
        world_tags.extend(world.tags)

    world_tags = list(dict.fromkeys(world_tags))
    print(world_tags)

    button_x_coord = 0.2
    for tag in world_tags:
        button = tk.Button(root, text=tag, bg="grey", fg="black", width=6)#, command=lambda: add_tag(tag))
        button.pack()
        button.place(relx=button_x_coord + 0.1, rely=0.1)
        button_x_coord+=0.1


    for world in loaded_worlds:
        icon = tk.PhotoImage(file=join(*['minecraft_worlds', world.dir, 'world_icon.gif']))
        # print(icon)
        treeView.insert('', 'end', text=world.name,
                        value=(world.last_used,
                                world.created))


def showArchivedTree():
    archived_search()
    treeView.delete(*treeView.get_children())
    archived_worlds = archived_worlds_list
    for world in archived_worlds:
        treeView.insert('', 'end', text=world[0],
                        values=("na",
                                world[1]))

def add_tag(tag):
    print("adding tag",tag) #function seems to run on loading treeview, not on pushing button??
    """add a tag to the worlds selected in the treeview this take the tag button text, will create a params file
     with a list of tags if it doesn't exist or add to the file if it does exist"""
    loaded_worlds = loaded_world_list
    selected_worlds = treeView.selection()
    # need to get the world name from the item using iid, match the world selected
    # with the list of world objects, get needed info and
    # update the tags param file with the new tag.
    for selected_world in selected_worlds:
        for world in loaded_worlds:
            if world.name == treeView.item(selected_world)['text']:
                params_file_path = join(*["minecraft_worlds", world.dir, "world_manager_params.ini"])
                # if the world_manager_params file exists get the tags from it
                if os.path.exists(params_file_path):
                    with open(params_file_path, 'r') as params:
                        for line in params:
                            if line.startswith('TAGS='):
                                # tags = params.readline()
                                tags = [tag for tag in line[line.find('['):line.find(']')].split(',')]
                                break

                    tags.append(tag)
                    with open(params_file_path, 'w') as params:
                        params.write("TAGS="&tags)
                else:
                    with open(params_file_path, 'w') as params:
                        print("creating params")
                        params.write("TAGS="&tag)
                world.tags.append(tag)

        # print(treeView.item(selected_world)['text'])


def sort(treeView, col, reverse):
    """sorts the treeview items by the contents of selected column header,
    may need to change format of modified and used to be more like
    2020-02-01 14:00 (Sat Feb 1 2:00pm)
    so that sorting works as expected. will need to test"""
    itemlist = list(treeView.get_children(''))
    print(itemlist)
    itemlist.sort(reverse=reverse)
    # itemlist.sort(key=lambda x: treeView.set(x, col))
    for index, iid in enumerate(itemlist):
        print(index, iid, treeView.parent(iid))
        treeView.move(iid, treeView.parent(iid), index)

    # re-set heading so that next click will reverse the order
    treeView.heading(col, command=lambda: sort(treeView, col, not reverse))

def on_select(event):
    # on selecting item(s) should be able to import/export depending on
    # archive status, and add remove tags
    # not sure which of these is best see: https://stackoverflow.com/questions/36361361/python-3-tkinter-treeview-get-name-of-selected-item
    # & https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.selection
    # selected_worlds = event.widget.selection() # gives item IDs of all selected in a tuple, eg ('I001', 'I002')
    # print("widget id:", selected_worlds, type(selected_worlds))
    selected_worlds = treeView.selection() # gives item IDs of all selected in a tuple, eg ('I001', 'I002')
    print("treeview id:", selected_worlds, type(selected_worlds))

    # on row select get the row item and return the name of the world
    selected_world_name = treeView.item(treeView.focus())['text'] # gives "#0' text ie AdventureWorld
    print("focus on:", selected_world_name)
    # selected_id = treeView.selected_id()

def archive_world():
    """gets selected worlds from tree and zips using the archive world method"""
    # should refactor so that method takes a list, then remove this method and call that one directly
    selected_worlds = treeView.selection()  # gives item IDs of all selected in a tuple, eg ('I001', 'I002')
    # on row select get the row item and return the name of the world
    for world in selected_worlds:
        selected_world_name = treeView.item(treeView.focus())['text']  # gives "#0' text ie AdventureWorld

def restore_worlds():
    """gets selected worlds from tree and unzips using the restore world method"""
    # should refactor so that method takes a list, then remove this method and call that one directly
    pass
#methods for treeview end


root = tk.Tk()
canvas = tk.Canvas(root, height=700, width=600, bg="#909696")
canvas.pack()
frame = tk.Frame(root, bg="#CDD5D5")
frame.place(relwidth=0.95, relheight=0.7, relx=0.025, rely=0.2)
print(frame.winfo_height())
frame.update()
canvas_in_frame = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="red")
canvas_in_frame.pack()


# treeview code starts
treeView = ttk.Treeview(canvas_in_frame, columns=["lastplayed", "created"], selectmode='extended')
treeView.heading('#0', text='Name', command=lambda: sort(treeView, '#0', False))
treeView.heading('lastplayed', text='Last Played Date', anchor='e', command=lambda: sort(treeView, 'lastplayed', False))
treeView.heading('created', text='Created Date', anchor='e', command=lambda: sort(treeView, 'created', False))

treeView.column('#0', stretch=True, width=int(frame.winfo_width()*0.5))
treeView.column('lastplayed', width=int(frame.winfo_width()*0.25))
treeView.column('created', width=int(frame.winfo_width()*0.25))
treeView.bind('<<TreeviewSelect>>', on_select)
treeView.pack(expand=True, fill='both')
# treeview code stops

# set up buttons for switching between loaded and archived worlds
show_loadedWorlds_bt = tk.Button(root, text="Loaded", bg="grey", fg="black", width=6, command=showLoadedTree)
show_archivedWorlds_bt = tk.Button(root, text="Archived", bg="grey", fg="black", width=6, command=showArchivedTree)
show_loadedWorlds_bt.pack()
show_loadedWorlds_bt.place(relx=0.1, rely=0.1)
show_archivedWorlds_bt.pack()
show_archivedWorlds_bt.place(relx=0.2, rely=0.1)

# now to set up archiving and unarchiving buttons
archive_worlds_bt = tk.Button(root, text="Archive Selected Worlds", wraplength=45, anchor='w', justify=tk.CENTER,
                              padx=10, bg="grey", fg="black", width=8, height=3, command=archive_world)
restore_worlds_bt = tk.Button(root, text="Restore Selected Worlds", wraplength=45, anchor='w', justify=tk.CENTER,
                              padx=10, bg="grey", fg="black", width=8, height=3, command=restore_worlds)
archive_worlds_bt.pack()
archive_worlds_bt.place(relx=0.65, rely=0.048)
restore_worlds_bt.pack()
restore_worlds_bt.place(relx=0.81, rely=0.048)


# create a search box, set command to filter the treechildren if the #0 contains search text
# need to work out how to change the search functions when switching between loaded and archived worlds
# searchbox methods etc...
def loaded_search():
    search_box.bind("<FocusIn>", lambda event, loaded=True: search_focus_in(loaded))
    search_box.bind("<FocusOut>", lambda event, loaded=True: search_focus_out(loaded))
    search_box.bind("<Return>", filter_tree)
    search_box.pack()
    search_box.place(relx=0.1, rely=0.15)

def archived_search():
    search_box.bind("<FocusIn>", lambda event, loaded=False: search_focus_in(loaded))
    search_box.bind("<FocusOut>", lambda event, loaded=False: search_focus_out(loaded))
    search_box.bind("<Return>", filter_tree)
    search_box.pack()
    search_box.place(relx=0.1, rely=0.15)

def search_focus_in(e):
    # list(treeView.get_children(''))
    search_box.delete('0', 'end')
    search_box.config(foreground="black")

def search_focus_out(e):
    """if the search box is empty it resets and re-populates the treeview.
    if e=True then use the loaded Tree, else use Archived tree"""
    if search_box.get() == "" and e:
        showLoadedTree()
        search_box.insert(0, "search worlds...")
        search_box.config(foreground="grey")
    elif search_box.get() == "" and not e:
        showArchivedTree()
        search_box.insert(0, "search worlds...")
        search_box.config(foreground="grey")


def filter_tree(e):
    search_text = search_box.get().lower()
    if search_text != '':
        item_iid_text_list = []
        initial_iids = []
        for child in treeView.get_children(''):
            item_iid_text_list.append((child, treeView.item(child)['text']))
            initial_iids.append(child)

        # print(item_iid_text_list)
        search_matches = list(filter(lambda child: search_text in child[1].lower(), item_iid_text_list))
        search_itemiidlist = []
        for item in search_matches:
            search_itemiidlist.append(item[0])

        itemiidlist = search_itemiidlist
        treeView.detach(*treeView.get_children())

        for index, iid in enumerate(itemiidlist):
            treeView.move(iid, treeView.parent(iid), index)


# add search box and run methods to show initial loaded world tree
# and set search to use loaded world parameters
search_box = tk.ttk.Entry(root, width=40, background="white", foreground="grey")
search_box.insert(0, "search worlds...")
loaded_search()
showLoadedTree()
# show gui
root.mainloop()

