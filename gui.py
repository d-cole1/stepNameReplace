import PySimpleGUI as sg
import functions_new as fn
import sys
import os

sg.theme("Default1")
sg.set_options(font=("Segoe UI Variable", 10))

input1 = sg.Input()
archive_choose = sg.FolderBrowse("Select Source Directory",
                                 key="source",
                                 pad=(5, 5))

input2 = sg.Input()
BOM_choose = sg.FileBrowse("Select BOM",
                           key="excel",
                           pad=(5, 5))

input3 = sg.Input()
save_dir = sg.FolderBrowse("Select Save Location",
                           key="save",
                           pad=(5, 5))

exec_button = sg.Button("Execute",
                        pad=(5, 5),
                        button_color=('White', 'NavyBlue'))



window = sg.Window(title="Step Name Replace",
                   layout=[[input1, archive_choose],
                           [input2, BOM_choose],
                           [input3, save_dir],
                           [exec_button]])

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Execute":

        # calls func to search directory and store stepfiles in list
        filepaths = fn.stpFinder(values["source"])
        filepaths = [item.replace("\\", "/") for item in filepaths]

        try:
            print(f"Source Directory: {values['source']}")
            print(f"Source Directory: {values['excel']}")
            print(f"Source Directory: {values['save']}")

            # calls func to search directory and store stepfiles in list
            filepaths = fn.stpFinder(values["source"])
            filepaths = [item.replace("\\", "/") for item in filepaths]
            print(f"Found {len(filepaths)} .stp files")

            #gets df from excel
            df = fn.extractMREBOM(values["excel"])

            #runs name replace function
            for filepath in filepaths:
                new_name = os.path.join(values["save"], os.path.basename(filepath).replace(".stp", "_rename.stp"))

                print(f"Processing file: {filepath} -> {new_name}")
                fn.stepNameReplace(filepath, df, new_name)

            sg.popup("Process completed successfully!",
                     font=("Segoe UI Variable", 10))

        except PermissionError:
            sg.popup("Ensure that BOM and folder locations are closed before executing\n\n"
                     "Click OK to terminate",
                     font=("Segoe UI Variable", 10))
            sys.exit()

        except Exception as e:
            sg.popup(f"An error occurred: {e}",
                     font=("Segoe UI Variable", 10))

window.close()
