import tkinter as tk
from tkinter import filedialog, Text, ttk
import os
from os.path import join
from worlds import getWorlds, getArchived
import archive_world as aw

#todo, turn this into a def/class or something, put all the gui setup into the __main__ and group the related functions,
# check if a mangaer_params.ini exists and if not prompt user for worldsave path and write to new file,
# use this full path for all bits that need a path.
# if exists, read path an use etc.

# set up some useful variables to be used elsewhere:
# don't think having this tag list here is a great idea, but we'll see if it works Todo
tag_filter_list = []
# list of loaded worlds
loaded_world_list = getWorlds()
#list of archived worlds
archived_worlds_list = getArchived()

#methods for treeview
def showLoadedTree():
    #deactivate the restore worlds button
    restore_worlds_bt.config(relief='sunken', state='disabled')
    archive_worlds_bt.config(relief='raised', state='normal')
    show_loadedWorlds_bt.config(relief='sunken')
    show_archivedWorlds_bt.config(relief='raised')
    #set up the search bar for loaded worlds
    loaded_search()
    #set up the world tags list prior to fetching the tags from world dir ini files
    world_tags = []
    treeView.delete(*treeView.get_children())
    loaded_worlds = getWorlds()
    for world in loaded_worlds:
        world_tags.extend(world.tags)

    world_tags = sorted(list(dict.fromkeys(world_tags)))
    # print(world_tags)
    #set starting x coordinate for tag buttons
    button_x_coord = 0.02

    for tag in world_tags:
        print(tag)
        button = tk.Button(root, text=tag, bg="grey", fg="black", width=10)
        button['command'] = lambda button=button: add_tag_to_filter_list(button)
        # button.config(command=lambda: add_tag_to_filter_list(tag))
        button.pack()
        button.place(relx=button_x_coord, rely=0.12)
        button_x_coord+=0.08


    for world in loaded_worlds:
        #todo get the world image and add to the row, didn't seem to work last time. need to convert file to gif?
        # icon = tk.PhotoImage(file=join(*['minecraft_worlds', world.dir, 'world_icon.gif']))
        # print(icon)
        treeView.insert('', 'end', text=world.name,
                        value=(world.last_used,
                                world.created))


def showArchivedTree():
    # deactivate archive worlds button and activate restore button
    archive_worlds_bt.config(relief='sunken', state='disabled')
    restore_worlds_bt.config(relief='raised', state='normal')
    show_loadedWorlds_bt.config(relief='raised')
    show_archivedWorlds_bt.config(relief='sunken')
    #todo change created date header to archived date
    archived_search()
    treeView.delete(*treeView.get_children())
    # archived_worlds = archived_worlds_list
    archived_worlds = getArchived()
    for world in archived_worlds:
        treeView.insert('', 'end', text=world[0],
                        values=("na",
                                world[1]))

def add_tag_to_filter_list(button):
    """intended to add the tag for the pressed button to the list, then call filter def?"""
    tag_filter_list.append(button['text'])
    button.config(relief='sunken')
    button['command'] = lambda button=button: remove_tag_from_filter_list(button)
    filter_on_tag()

def remove_tag_from_filter_list(button):
    """intended to remove tag from list when button is deactivated"""
    tag_filter_list.remove(button['text'])
    button.config(relief='raised')
    button['command'] = lambda button=button: add_tag_to_filter_list(button)
    filter_on_tag()

# taken from the filter function, sub in using the list
def filter_on_tag():
    # todo, add tag value passed by button to a list, filter the treeview based on list similar to search,
    #  but will have to say for each world tag if tag in tag list then show else destroy?detach?
    """if the search box is not empty it and
            if e=True then refer to loaded worlds list, else use Archived worlds list in filter"""
    e = True #todo, add this parameter to the buttons, true for loaded False for archived,
            #prob create CONSTANTS for LOADED & ARCHIVED that can be used, these are becomming more common
    # if search_text != '':
    print(tag_filter_list)
    if len(tag_filter_list) > 0:
        if e:
            loaded_worlds = loaded_world_list   # maybe have this conditional on "e" loaded list for true
                                                # else archived and delete the else part of the if block

            #if intersection of world.tags list and tag_filter_list > 0 then keep world
            filtered_worlds = list(filter(lambda world: len(set(tag_filter_list).intersection(world.tags)) > 0, loaded_worlds))

            treeView.detach(*treeView.get_children())

            for world in filtered_worlds:
                treeView.insert('', 'end', text=world.name,
                                value=(world.last_used,
                                       world.created))

        #todo change this so that the filter works for archived worlds, need to change the worlds.py to create
        # world objects from archived worlds and use the same as loaded worlds

        # else:
        #     if not e:
        #         print("searching archived")
        #         archived_worlds = archived_worlds_list
        #         search_matches = list(filter(lambda world: search_text in world[0].lower(), archived_worlds))
        #         print(search_matches)
        #
        #         treeView.detach(*treeView.get_children())
        #
        #         for world in search_matches:
        #             treeView.insert('', 'end', text=world[0],
        #                             values=("na",
        #                                     world[1]))
    else:
        treeView.detach(*treeView.get_children())
        for world in loaded_world_list:
            treeView.insert('', 'end', text=world.name,
                            value=(world.last_used,
                                   world.created))


def add_tag_to_world(tag):
    # rethinking how the buttons should work. depressing a button should filter the tree to those worlds with the tag,
    # adding a tag will wait for now. tags will be generated by the level.dat values.
    # adding a tag might have it's own menu/buttons
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
    """sorts the treeview items by the contents of selected column header"""
    print(col)
    itemlist = list(treeView.get_children(''))
    # itemlist.sort(reverse=reverse)
    # itemlist.sort(reverse=reverse)
    # get row values and sort on those not iids
    row_values = []
    for iid in itemlist:
        if col == '#0':
            row_values.append((iid, treeView.item(iid)['text']))
        elif col == 'lastplayed':
            row_values.append((iid, treeView.item(iid)['values'][0]))
        elif col == 'created':
            row_values.append((iid, treeView.item(iid)['values'][1]))

        # rowdata = 'text' if col == '#0' else 'values'
        # index = 0 if col == 'lastplayed' else 0 if col == '#0' else 1
        # print('rowdata: ',rowdata,'index: ', index)
        # print(treeView.item(iid)[rowdata][index])
        # row_values.append((iid, treeView.item(iid)[rowdata][index]))

    # performing sort on row valuse
    sortedlist = sorted(row_values, key=lambda row: row[1], reverse=reverse)
    for index, iid in enumerate(sortedlist):
        treeView.move(iid[0], treeView.parent(iid[0]), index)

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
        selected_world_name = treeView.item(world)['text']  # gives "#0' text ie AdventureWorld
        aw.archive_world(selected_world_name)
    os.chdir('../')
    showLoadedTree()


def restore_worlds():
    """gets selected worlds from tree and unzips using the restore world method"""
    # should refactor so that method takes a list, then remove this method and call that one directly
    selected_archived_world_ids = treeView.selection()  # gives item IDs of all selected in a tuple, eg ('I001', 'I002')

    # on row select get the row item and return the name of the world
    for world_iid in selected_archived_world_ids:
        print("worldid:", world_iid)
        selected_world_name = treeView.item(world_iid)['text']  # gives "#0' text ie AdventureWorld
        print("restoring world:", selected_world_name)
        aw.restore_world(selected_world_name)

    os.chdir('../')
    showArchivedTree()

#methods for treeview end


root = tk.Tk()
canvas = tk.Canvas(root, height=500, width=1000, bg="#909696")
canvas.pack()
frame = tk.Frame(root, bg="#CDD5D5")
frame.place(relwidth=0.95, relheight=0.7, relx=0.025, rely=0.25)
print(frame.winfo_height())
frame.update()
canvas_in_frame = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="red")
canvas_in_frame.pack()


# treeview code starts
treeView = ttk.Treeview(canvas_in_frame, height=30, columns=["lastplayed", "created"], selectmode='extended')
vsb = ttk.Scrollbar(canvas_in_frame, orient="vertical", command=treeView.yview)
vsb.pack(side='right', fill='y')
treeView.configure(yscrollcommand=vsb.set)

treeView.heading('#0', text='Name', anchor='w'
                 , command=lambda: sort(treeView, '#0', False))
treeView.heading('lastplayed', text='Last Played Date', anchor='w', command=lambda: sort(treeView, 'lastplayed', False))
treeView.heading('created', text='Created Date', anchor='w', command=lambda: sort(treeView, 'created', False))

treeView.column('#0', stretch=True, width=int(frame.winfo_width()*0.4))
treeView.column('lastplayed', width=int(frame.winfo_width()*0.3))
treeView.column('created', width=int(frame.winfo_width()*0.3))
treeView.bind('<<TreeviewSelect>>', on_select)
treeView.pack(expand=True, fill='both')
# treeview code stops

# set up buttons for switching between loaded and archived worlds
# todo cleanup button generation, have a loop or something
show_loadedWorlds_bt = tk.Button(root, text="Loaded", bg="grey", fg="black", width=8, height=2, command=showLoadedTree)
show_archivedWorlds_bt = tk.Button(root, text="Archived", bg="grey", fg="black", width=8,height=2, command=showArchivedTree)
show_loadedWorlds_bt.pack()
show_loadedWorlds_bt.place(relx=0.02, rely=0.01)
show_archivedWorlds_bt.pack()
show_archivedWorlds_bt.place(relx=0.10, rely=0.01)

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
    search_box.bind("<FocusIn>", search_focus_in)
    search_box.bind("<FocusOut>", lambda event, loaded=True: search_focus_out(loaded))
    search_box.bind("<Key>", lambda event, loaded=True: filter_tree(loaded))
    search_box.pack()
    search_box.place(relx=0.02, rely=0.2)

def archived_search():
    search_box.bind("<FocusIn>", search_focus_in)
    search_box.bind("<FocusOut>", lambda event, loaded=False: search_focus_out(loaded))
    search_box.bind("<Key>", lambda event, loaded=False: filter_tree(loaded))
    search_box.pack()
    search_box.place(relx=0.02, rely=0.2)

def search_focus_in(e):
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

# do the search
def filter_tree(e):
    """if the search box is not empty it and
        if e=True then refer to loaded worlds list, else use Archived worlds list in filter"""
    search_text = search_box.get().lower()
    if search_text != '':
        if e:
            loaded_worlds = loaded_world_list
            search_matches = list(filter(lambda world: search_text in world.name.lower(), loaded_worlds))

            treeView.detach(*treeView.get_children())

            for world in search_matches:
                treeView.insert('', 'end', text=world.name,
                                value=(world.last_used,
                                       world.created))
        else:
            if not e:
                print("searching archived")
                archived_worlds = archived_worlds_list
                search_matches = list(filter(lambda world: search_text in world[0].lower(), archived_worlds))
                print(search_matches)

                treeView.detach(*treeView.get_children())

                for world in search_matches:
                    treeView.insert('', 'end', text=world[0],
                                    values=("na",
                                            world[1]))


        # this bit uses the existing items in the tree view, what I should do is filter the world lists and
        # then re-insert those that match
        # item_iid_text_list = []
        # for child in treeView.get_children(''):
        #     item_iid_text_list.append((child, treeView.item(child)['text']))
        #
        # # print(item_iid_text_list)
        # search_matches = list(filter(lambda child: search_text in child[1].lower(), item_iid_text_list))
        # search_itemiidlist = []
        # for item in search_matches:
        #     search_itemiidlist.append(item[0])
        #
        # itemiidlist = search_itemiidlist
        # treeView.detach(*treeView.get_children())
        #
        # for index, iid in enumerate(itemiidlist):
        #     treeView.move(iid, treeView.parent(iid), index)


# add search box and run methods to show initial loaded world tree
# and set search to use loaded world parameters
search_box = tk.ttk.Entry(root, width=40, background="white", foreground="grey")
search_box.insert(0, "search worlds...")
loaded_search()
showLoadedTree()
# show gui
root.mainloop()

