import PySimpleGUI as sg
import functions_new as fn
import pandas as pd

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

exec_button = sg.Button("Execute",
                        pad=(5, 5),
                        button_color=('White', 'NavyBlue'))

window = sg.Window(title="Step Name Replace",
                   layout=[[input1, archive_choose],
                           [input2, BOM_choose],
                           [exec_button]])

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    # Gets correct amount of .stp files from folder when gui executed
    stp_files = fn.stpFinder(values['source'])
    stp_files = [item.replace("\\", "/") for item in stp_files]
    print(stp_files)

    try:
        df = fn.excelExtract(values['excel'])



    except PermissionError:
        sg.popup("Ensure BOM is closed before executing")



window.close()
