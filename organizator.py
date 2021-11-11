import tkinter as tk
from tkinter import ttk, simpledialog
import json
import os
from tkinter.constants import E, END
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from typing import Dict, Callable
import uuid
from datetime import datetime
import re

# WINDOW AND FRAMES SETUP
# window setup
ws = tk.Tk()
ws.title("Contact Organizator")
ws.geometry("1542x750")
ws.resizable(False, False)

# FORM FRAME - config
form_frame = tk.Frame(ws, background="#FFF", width=390, height=500)
form_frame.grid(row=0, column=0, sticky="nsew", padx=45, pady=50)
form_frame.grid_propagate(0)

# BUTTONS FRAME - config
btns_frame = tk.Frame(ws, background="#FFF0C1", width=390,
                      height=250, pady=30, padx=50)
btns_frame.grid(row=1, column=0, sticky="nsew")
btns_frame.grid_propagate(0)

# CONTACT FRAME - config
contact_frame = tk.Frame(ws, background="#D2E2FB", width=1110, height=750)
contact_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
contact_frame.grid_propagate(0)

# id "shower"
identifier = tk.Label(form_frame, text="", anchor="w",
                      width=37, font=("Arial", 14), bg="lightgray")
identifier.grid(row=0, column=0)

# name input - mandatory
name = tk.Label(form_frame, text="Name:* ", anchor="w",
                width=30, font=("Arial", 18), pady=15)
name.grid(row=1, column=0)
Name = tk.Entry(form_frame, width=60)
Name.grid(row=2, column=0)

# birthday label and input
birthday = tk.Label(form_frame, text="Birthday: (DD.MM.YYYY)",
                    anchor="w", width=30, font=("Arial", 18), pady=15)
birthday.grid(row=3, column=0)
Birthday = tk.Entry(form_frame, width=60)
Birthday.grid(row=4, column=0)

# email label and input
email = tk.Label(form_frame, text="Email: ", anchor="w",
                 width=30, font=("Arial", 18), pady=15)
email.grid(row=5, column=0)
Email = tk.Entry(form_frame, width=60)
Email.grid(row=6, column=0)

# phone label and input
phone = tk.Label(form_frame, text="Phone number: ", anchor="w",
                 width=30, font=("Arial", 18), pady=15)
phone.grid(row=7, column=0)
Phone = tk.Entry(form_frame, width=60)
Phone.grid(row=8, column=0)

# note label and input
note = tk.Label(form_frame, text="Note: ", anchor="w",
                width=30, font=("Arial", 18), pady=15)
note.grid(row=9, column=0)
Note = tk.Text(form_frame, width=51, height=5, font=("TimesNewRoman", 9))
Note.grid(row=10, column=0)

# TREEVIEW
# tree setup and function
tree = ttk.Treeview(contact_frame, columns=(
    '1', '2', '3', '4', '5', '6'), show='headings', height=30)
tree.grid(row=0, column=0, columnspan=5)


# sort column alphabetically
def alph_sort() -> None:
    # check if column was pressed
    global vertically

    # gather item names
    item_names = [tree.item(i)["values"] for i in tree.get_children()]

    # CHECK BUTTON STATES
    # sort alphabetically
    if vertically == 0:
        tree.delete(*tree.get_children())
        item_names = sorted(item_names, key=lambda x: x[0])
        for item in item_names:
            tree.insert('', tk.END, values=item)

        # set what will happen next
        vertically += 1

    # sort alphabetically (reversed)
    elif vertically == 1:
        tree.delete(*tree.get_children())
        item_names = sorted(item_names, key=lambda x: x[0], reverse=True)
        for item in item_names:
            tree.insert('', tk.END, values=item)

        # set what will happen next
        vertically += 1

    # return to original state
    elif vertically == 2:
        tree.delete(*tree.get_children())
        load()

        # set what will happen next
        vertically = 0

    # if state is broken return popup
    else:
        return popup("You somehow broke the app ( •_•)>⌐■-■")


# initial value
vertically = 0

# define headings of the tree
tree.heading('1', text='Name', command=alph_sort)
tree.heading('2', text='Email')
tree.heading('3', text='Phone Number')
tree.heading('4', text='Birthday')
tree.heading('5', text='Note')
tree.heading('6', text='Id')

# dont display id column
tree["displaycolumns"] = ('1', '2', '3', '4', '5')

# adding a scrollbar to our treeview
scrollbar = ttk.Scrollbar(
    contact_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=6, columnspan=5, sticky='ns')


# SETUP FUNCTIONS AND HELPING FUNCTIONS
# check if JSON FILE exists, if not, create one
def setup_json() -> None:
    if os.path.exists("contacts.json") is False:
        with open("contacts.json", "w", encoding="utf-8") as f:
            f.write('[]')


# load contacts from JSON
def load() -> None:
    with open("contacts.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for friend in data:
            # insert data to treeview
            tree.insert("", tk.END, values=(
                f'{friend["name"]}', f'{friend["email"]}',
                f'{friend["phone"]}', f'{friend["birthday"]}',
                f'{friend["note"]}', f'{friend["id"]}'
            ))

            # check if anyone has birthday
            if check_for_birthday(friend):
                popup(friend["name"] + " is celebrating bithday today!")


# show popup message
def popup(message: str) -> Callable:
    return showinfo("!", message)


# clear form inputs
def clear_inputs() -> None:
    Name.delete(0, END)
    Birthday.delete(0, END)
    Phone.delete(0, END)
    Email.delete(0, END)
    Note.delete('1.0', END)
    identifier["text"] = ""


# MAIN FUNCTIONS
# CHECK FUNCTIONS
def check_for_birthday(birthman: Dict) -> bool:
    if birthman["birthday"] == "":
        return False

    # 'birthman' birthday and today's date
    b_date = datetime.strptime(
                birthman["birthday"],
                '%d.%m.%Y').strftime('%d.%m')
    today = datetime.today().strftime('%d.%m')

    # check if today's date matches contact's birthdate
    if b_date == today:
        return True

    return False


# MAIN CHECK FUNCTION and its SUBFUNCTIONS
def check(to_update: Dict) -> bool:
    # check name mandatority
    if to_update["name"] == "":
        popup("Name is mandatory, see that star? Try again ;)")
        return False

    # check phone validity
    if phone_validity(to_update["phone"]) is False:
        return False

    # check email validity
    if email_validity(to_update["email"]) is False:
        return False

    # check birthday validity
    if bday_validity(to_update["birthday"]) is False:
        return False

    # if check didnt give us False, return True
    return True


def phone_validity(phone_num: str) -> bool:
    # check if number was even filled
    if phone_num == "":
        return True

    # regular expression for phone number
    phone_regex = r'^[+]?[\d \s]+$'

    # check if email is valid
    if re.fullmatch(phone_regex, phone_num):
        return True

    else:
        popup("Your phone number format is invalid!")
        return False


def bday_validity(bday: str) -> bool:
    # check if date is even filled, if not, just return true
    if bday == "":
        return True

    # check if date format is correct
    try:
        datetime.strptime(bday, '%d.%m.%Y').strftime('%dd.%m.%Y')

    except ValueError:
        popup("Incorrect data or date format, should be DD.MM.YYYY")
        return False

    return True


def email_validity(email: str) -> bool:
    # check if email is even filled, if not, just return true
    if email == "":
        return True

    # make regular expression for checking email
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # check if email is valid
    if re.fullmatch(email_regex, email):
        return True

    # if not, throw a popup
    else:
        popup("Your email data or format is invalid!")
        return False


# BINDING FUNCTIONS
# reset on doubleclick
def reset_form(event) -> None:
    Name.delete(0, END)
    Birthday.delete(0, END)
    Phone.delete(0, END)
    Email.delete(0, END)
    Note.delete('1.0', END)
    identifier["text"] = ""


identifier.bind('<Double-Button-1>', reset_form)


# get selected item
def item_selected(event) -> None:
    for selected in tree.selection():
        item = tree.item(selected)
        txt_message = ""
        j = 0

        for i in tree["displaycolumns"]:
            txt_message += tree.heading(i)['text'] + \
                ": " + item["values"][j] + "\n"
            j += 1

        showinfo(title='Information',
                 message=txt_message)


tree.bind('<Double-1>', item_selected)


# BUTTONS AND ITS CORRESPONDING FUNCTIONS
# update button
# decide whether to update or add new item to tree
def decide() -> Callable:
    if identifier["text"] == "":
        return add_new()
    else:
        return edit_handle()


# add item
def add_new() -> None:
    with open('contacts.json', 'r+', encoding="utf-8") as f:
        file_data = json.load(f)

        # item to add
        new_one = {
            "id": str(uuid.uuid1()),
            "name": Name.get(),
            "phone": Phone.get(),
            "email": Email.get(),
            "note": Note.get("1.0", "end-1c")
        }

        # check if birthday is valid
        try:
            new_one.update({"birthday": datetime.strptime(
                str(Birthday.get()), '%d.%m.%Y').strftime('%d.%m.%Y')})
        except ValueError:
            new_one.update({"birthday": ""})

        # add item to json and a tree
        if check(new_one):
            file_data.append(new_one)
            f.seek(0)
            json.dump(file_data, f, indent=4)
            tree.insert("", tk.END, text=new_one["phone"], values=(
                f'{new_one["name"]}', f'{new_one["email"]}',
                f'{new_one["phone"]}', f'{new_one["birthday"]}',
                f'{new_one["note"]}', f'{new_one["id"]}'
            ))

            # get form ready for next input
            clear_inputs()


# edit the actual item
def edit_handle() -> None:
    # item to update
    updated_one = {
        "id": identifier["text"],
        "name": Name.get(),
        "birthday": "",
        "phone": Phone.get(),
        "email": Email.get(),
        "note": Note.get("1.0", "end-1c")
    }

    # check birthday
    if str(Birthday.get()) != "":
        updated_one.update({
            "birthday": datetime.strptime(
                str(Birthday.get()), '%d.%m.%Y'
            ).strftime('%d.%m.%Y')
            })

    if check(updated_one):
        # update item in a tree
        tree.item(selected_item, text=Phone.get(), values=(
            f'{Name.get()}', f'{Email.get()}',
            f'{Phone.get()}', f'{Birthday.get()}',
            f'{Note.get("1.0", "end-1c")}', f'{identifier["text"]}'
        ))

        # update item in json
        with open("contacts.json", 'r+', encoding="utf-8") as f:
            file_data = json.load(f)
            i = 0
            for item in file_data:
                if updated_one["id"] == item["id"]:
                    file_data[i] = updated_one
                    f.seek(0)
                    json.dump(file_data, f, indent=4)
                    f.truncate()
                i += 1

        # clear form then
        clear_inputs()


submit = tk.Button(btns_frame, text='Add/Update contact!',
                   command=decide, padx=85, font=("Arial", 16))
submit.grid(row=0, columnspan=2)


# import contacts
def import_con() -> None:
    # setup external file
    with open(fd.askopenfilename(
        title="Import VCARD file",
        filetypes=[("VCF files", "*.vcf")],
    ), encoding="utf-8") as ext_file:

        if ext_file is None:
            return

        # initial values
        lines = ext_file.readlines()
        cur_line = 0
        begin = False

        imported_one = {
            "id": str(uuid.uuid4()),
            "name": "",
            "email": "",
            "phone": "",
            "birthday": "",
            "note": "",
        }

        # parsing
        while cur_line < len(lines):
            try:
                with open("contacts.json", "r+", encoding="utf-8") as f:
                    file_data = json.load(f)

                    # check beggining
                    if lines[cur_line] == "BEGIN:VCARD\n":
                        if lines[cur_line+1] == "VERSION:3.0\n":
                            begin = True
                            cur_line += 2

                        else:
                            popup("Your file is missing version attribute!")
                            return

                    elif begin:
                        if "FN:" in lines[cur_line]:
                            imported_one.update({
                                "name": str(("").join(lines[cur_line][3:-1:]))
                            })
                            cur_line += 1

                        elif "EMAIL" in lines[cur_line]:
                            imported_one.update({
                                "email": ("").join(
                                        lines[cur_line].split(":")[-1]
                                    ).replace("\n", "")
                            })
                            cur_line += 1

                        elif "NOTE:" in lines[cur_line]:
                            imported_one.update({
                                "note": str(("").join(lines[cur_line][5:-1:]))
                            })
                            cur_line += 1

                        elif "TEL" in lines[cur_line]:
                            imported_one.update({
                                "phone": ("").join(
                                        lines[cur_line].split(":")[-1]
                                    ).replace("\n", "")
                            })
                            cur_line += 1

                        elif "BDAY:" in lines[cur_line]:
                            date_str = datetime.strptime(
                                    ("").join(lines[cur_line][5:-1:]),
                                    '%Y-%m-%d'
                                )
                            imported_one.update({
                                "birthday": datetime.strftime(
                                    date_str,
                                    '%d.%m.%Y'
                                )
                            })
                            cur_line += 1

                        elif lines[cur_line] == "END:VCARD\n":
                            # update file
                            file_data.append(imported_one)
                            f.seek(0)
                            json.dump(file_data, f, indent=4)

                            begin = False
                            imported_one.update({
                                "id": str(uuid.uuid4()),
                                "name": "",
                                "email": "",
                                "phone": "",
                                "birthday": "",
                                "note": "",
                            })

                            cur_line += 1

                        else:
                            cur_line += 1

                    elif not begin:
                        popup("Your file doesn't seem to be valid!")
                        return

            except Exception:
                popup("Import failed!")
                return

        # load items to our tree
        load()

    return


# import button
import_btn = tk.Button(btns_frame, text='Import Contacts',
                       command=import_con, padx=11, font=("Arial", 16))
import_btn.grid(row=1, column=0)


# export contacts
def export_con() -> None:
    # load json files
    f = open("contacts.json", "r", encoding="utf-8")
    f_json = json.load(f)

    # save file as
    save_name = fd.asksaveasfilename(
        title="Save Contacts as .vcf",
        defaultextension=[("VCF files", "*.vcf")],
        filetypes=[("VCF files", "*.vcf")]
    )
    to_save = open(save_name, mode='w', encoding="utf-8")

    # make text
    save_content = ""
    for contact in f_json:
        # header
        save_content += str(
            "BEGIN:VCARD" + "\n"
            "VERSION:3.0" + "\n"
        )

        # name
        save_content += str(
            "N:" + (";").join(reversed(contact["name"].split(" "))) + "\n"
            "FN:" + contact["name"] + "\n"
        )

        # birthday
        if contact["birthday"] != "":
            save_content += str(
                "BDAY:" + datetime.strptime(
                    contact["birthday"], '%d.%m.%Y'
                ).strftime('%Y-%m-%d') + "\n"
            )

        # email
        if contact["email"] != "":
            save_content += str(
                "EMAIL;TYPE=internet:" + contact["email"] + "\n"
            )

        # phone
        if contact["phone"] != "":
            save_content += str(
                "TEL;TYPE=voice,pref:" + contact["phone"] + "\n"
            )

        # note
        if contact["note"] != "":
            save_content += str(
                "NOTE:" + contact["note"] + "\n"
            )

        # footer
        save_content += str(
            "END:VCARD" + "\n"
        )

    # asksaveasfile return `None` if dialog closed with "cancel".
    if to_save is None:
        return

    # add the vcard to the file
    to_save.write(save_content)

    # close the file
    f.close()
    to_save.close()


# export button
export_btn = tk.Button(btns_frame, text='Export Contacts',
                       command=export_con, padx=11, font=("Arial", 16))
export_btn.grid(row=1, column=1)


# edit button
# edit selected item
def edit() -> None:
    try:
        # check if more items are selected
        if len(tree.selection()) > 1:
            popup("You can only edit one item at the time")

        # clear inputs at first
        clear_inputs()

        # i made selected item global variable, as it cause problems when
        # editing if person checks other item while editing original one
        global selected_item
        selected_item = tree.selection()[0]

        to_edit = {
            "id": tree.item(selected_item)["values"][-1],
            "name": tree.item(selected_item)["values"][0],
            "birthday": tree.item(selected_item)["values"][3],
            "phone": tree.item(selected_item)["values"][2],
            "email": tree.item(selected_item)["values"][1],
            "note": tree.item(selected_item)["values"][4]
        }
        to_edit.update({
            "id": tree.item(selected_item)["values"][-1],
            "name": tree.item(selected_item)["values"][0],
            "birthday": tree.item(selected_item)["values"][3],
            "phone": tree.item(selected_item)["values"][2],
            "email": tree.item(selected_item)["values"][1],
            "note": tree.item(selected_item)["values"][4]
        }
        )

        # load values into form
        identifier.config(text=to_edit["id"])
        Name.insert(0, to_edit["name"])
        Birthday.insert(0, to_edit["birthday"])
        Phone.insert(0, to_edit["phone"])
        Email.insert(0, to_edit["email"])
        Note.insert("end-1c", to_edit["note"])

    # check if item is even selected
    except IndexError:
        popup("No item selected!")


edit_btn = tk.Button(contact_frame, text="Edit",
                     command=edit, padx=507.5, pady=4)
edit_btn.grid(row=1, column=0, columnspan=5)


# delete button
# delete selected item
def delete() -> None:
    # delete input at first, if there was item in form
    clear_inputs()

    # check if items are selected
    if tree.selection() == ():
        popup("No item selected!")

    # delete from json
    con_data = open("contacts.json", mode="r+", encoding="utf-8")
    file_data = json.load(con_data)
    to_delete = {
        "id": ""
    }
    for selected_one in tree.selection():
        to_delete.update({"id": tree.item(selected_one)["values"][-1]})
        del_id = to_delete["id"]
        i = 0
        while i in range(len(file_data)):
            if del_id == file_data[i]["id"]:
                file_data.pop(i)
                con_data.seek(0)
                json.dump(file_data, con_data, indent=4)
                con_data.truncate()

                # delete from tree
                tree.delete(selected_one)
                break
            i += 1
    con_data.close()


del_btn = tk.Button(contact_frame, text="Delete",
                    command=delete, padx=501, pady=3)
del_btn.grid(row=2, column=0, columnspan=5)


# search button
# seach in contacts
def search() -> None:
    # popup window
    popup_input = simpledialog.askstring(
        title="Search sequence", prompt="Search:")

    # detached items
    global det_items
    det_items = []

    # check if filtering makes sense
    if popup_input == "":
        return

    tree_items = tree.get_children()

    # searching string in values
    for item in tree_items:
        item_val = tree.item(item)["values"]
        not_in = False
        for value in item_val:
            if popup_input in value:
                not_in = True
                break
        if not not_in:
            tree.detach(item)
            det_items.append(item)

    # check if there are any results
    if tree.get_children() == ():
        popup("No items found!")
        cancel_search()
        return


search_btn = tk.Button(contact_frame, text='Search',
                       command=search, padx=288, pady=3)
search_btn.grid(row=3, column=0, columnspan=3)


# cancel search button
# cancel search result
def cancel_search() -> None:
    # check if we already searched
    try:
        if det_items == []:
            popup("There is no need to cancel your search!")
            return

    except NameError:
        popup("You cant cancel search if you hadnt even searched yet :)")
        return

    # return back items that were detached
    for item in det_items:
        tree.reattach(item, "", 0)


cancel_btn = tk.Button(contact_frame, text='Cancel Search',
                       command=cancel_search, padx=170, pady=3)
cancel_btn.grid(row=3, column=3, columnspan=2)


# COLUMN HIDING BUTTONS AND FUNCTIONS
# hide name
def name_col() -> None:
    global nameClicked

    # show column back if it was hidden
    if nameClicked:
        tree["displaycolumns"] = tuple(sorted(tree["displaycolumns"] + ('1',)))

    # check if atleast one item is shown
    else:
        if len(tree["displaycolumns"]) == 1:
            popup("You need to show at least one column")
            return

        # column hiding
        disp_list = list(tree["displaycolumns"])
        disp_list.remove('1')
        tree["displaycolumns"] = tuple(disp_list)

    nameClicked = not nameClicked


# initial value
nameClicked = False

hide_name = tk.Button(contact_frame, text='(Un)Hide Name',
                      command=name_col, padx=55, pady=3)
hide_name.grid(row=4, column=0)


# hide email column
def email_col() -> None:
    global emailClicked

    # show column back if it was hidden
    if emailClicked:
        tree["displaycolumns"] = tuple(sorted(tree["displaycolumns"] + ('2',)))

    # check if atleast one item is shown
    else:
        if len(tree["displaycolumns"]) == 1:
            popup("You need to show at least one column")
            return

        # column hiding
        disp_list = list(tree["displaycolumns"])
        disp_list.remove('2')
        tree["displaycolumns"] = tuple(disp_list)

    emailClicked = not emailClicked


# initial value
emailClicked = False

hide_email = tk.Button(contact_frame, text='(Un)Hide Email',
                       command=email_col, padx=55, pady=3)
hide_email.grid(row=4, column=1)


# hide phone
def phone_col() -> None:
    global phoneClicked

    # show column back if it was hidden
    if phoneClicked:
        tree["displaycolumns"] = tuple(sorted(tree["displaycolumns"] + ('3',)))

    # check if atleast one item is shown
    else:
        if len(tree["displaycolumns"]) == 1:
            popup("You need to show at least one column")
            return

        # column hiding
        disp_list = list(tree["displaycolumns"])
        disp_list.remove('3')
        tree["displaycolumns"] = tuple(disp_list)

    phoneClicked = not phoneClicked


# initial value
phoneClicked = False

hide_phone = tk.Button(contact_frame, text='(Un)Hide Phone',
                       command=phone_col, padx=55, pady=3)
hide_phone.grid(row=4, column=2)


# hide birthday
def bday_col() -> None:
    global bdayClicked

    # show column back if it was hidden
    if bdayClicked:
        tree["displaycolumns"] = tuple(sorted(tree["displaycolumns"] + ('4',)))

    # check if atleast one item is shown
    else:
        if len(tree["displaycolumns"]) == 1:
            popup("You need to show at least one column")
            return

        # column hiding
        disp_list = list(tree["displaycolumns"])
        disp_list.remove('4')
        tree["displaycolumns"] = tuple(disp_list)

    bdayClicked = not bdayClicked


# initial value
bdayClicked = False

hide_bday = tk.Button(contact_frame, text='(Un)Hide Birthday',
                      command=bday_col, padx=55, pady=3)
hide_bday.grid(row=4, column=3)


# hide note
def note_col() -> None:
    global noteClicked

    # show column back if it was hidden
    if noteClicked:
        tree["displaycolumns"] = tuple(sorted(tree["displaycolumns"] + ('5',)))

    # check if atleast one item is shown
    else:
        if len(tree["displaycolumns"]) == 1:
            popup("You need to show at least one column")
            return

        # column hiding
        disp_list = list(tree["displaycolumns"])
        disp_list.remove('5')
        tree["displaycolumns"] = tuple(disp_list)

    noteClicked = not noteClicked


# initial value
noteClicked = False

hide_note = tk.Button(contact_frame, text='(Un)Hide Note',
                      command=note_col, padx=55, pady=3)
hide_note.grid(row=4, column=4)

# RUN SETUP
setup_json()
load()

# RUN THE APP MAINLOOP
ws.mainloop()
