import PySimpleGUI as sg

sg.theme("Default1")

input1 = sg.Input()
archive_choose = sg.FolderBrowse("Select Source Directory",
                                 key="source",
                                 pad=(5, 5))

input2 = sg.Input()
BOM_choose = sg.FileBrowse("Select BOM",
                           key="excel",
                           pad=(5, 5))

exec_button = sg.Button("Execute",
                        key="execute",
                        pad=(5, 5),
                        button_color=('White', 'NavyBlue'))

window = sg.Window(title="Step Name Replace",
                   layout=[[input1, archive_choose],
                           [input2, BOM_choose],
                           [exec_button]],
                   font=("Segoe UI Variable", 10))

while True:
    event, values = window.read()

    print(event, values)

    if event == sg.WIN_CLOSED:
        break

window.close()
