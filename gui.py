import PySimpleGUI as sg
import functions_new as fn
import sys
import os
import threading

my_new_theme = {'BACKGROUND': '#212325',
                'TEXT': '#F0F0F0',
                'INPUT': "#343638",
                'TEXT_INPUT': "#F0F0F0",
                'SCROLL': "#343638",
                'BUTTON': ('#F0F0F0', '#1e6aa4'),
                'PROGRESS': ('#F0F0F0', '#212325'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

sg.theme_add_new("MyNewTheme", my_new_theme)
sg.theme("MyNewTheme")

sg.set_options(font=("Segoe UI Variable", 10))

def execute_func(window, values):
    try:
        # Extracts data from BOM as a panda array
        df = fn.extractMREBOM((values["excel"]))

        # Checks format of BOM before continuing code-> if format is wrong, err msg
        BOM_format = fn.checkBOMFormat(df)

        # If it is correct, the rest of execute_func will run
        if BOM_format == True:

            # Calls func to search directory and store stepfiles in list
            files = fn.stpFinder(values["source"])
            files = [item.replace("\\", "/") for item in files]
            print(f"Found {len(files)} .stp files")

            total_files = len(files)

            # Create new directory within source directory
            output_dir = os.path.join(values["source"], "SNR_Output")
            os.makedirs(output_dir, exist_ok=True)

            # Iterates over step files and assigns a number to each file
            for index, file in enumerate(files):

                # Creates name for output step file
                new_name = os.path.join(output_dir, os.path.basename(file))

                # "Update" assigned to be called by elif to update status bar through each iteration
                window.write_event_value("Update", (index + 1, total_files))

                # Runs stepNameReplace
                print(f"Processing file: {file}")
                fn.stepNameReplace(file, df, new_name)

            # Once loop completes, "Done" value assigned to be called by elif
            window.write_event_value("Done", None)

        else:
            window.write_event_value("Error", "invalid_BOM")

    except Exception as e:
        window.write_event_value("Error", str(e))

# Sets layout for GUI
layout = [
    [sg.Input(), sg.FolderBrowse("Select Source Directory", key="source", pad=(5, 5))],
    [sg.Input(), sg.FileBrowse("Select BOM", key="excel", pad=(5, 5))],
    [sg.Button("Execute"),
     sg.ProgressBar(1000, orientation='h', pad=(9, 5) , size=(19, 15), key='progressbar'),
     sg.Text("", key="info")]
]

# Creates window variable, assigns name and layout
window = sg.Window(title="Step Name Replace (SNR)", layout=layout)

# Main loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "Execute":
        print(f"Source Directory: {values['source']}")
        print(f"Source Directory: {values['excel']}")

        threading.Thread(target=execute_func, args=(window, values), daemon=True).start()

    if event == "Error":
        error_message = values[event]
        # print(values[event])
        if "[Errno 13]" in error_message:
            sg.popup("Ensure that the BOM is closed before running.\n\n"
                     "Click OK to terminate.")

        elif error_message == "invalid_BOM":
            sg.popup("Ensure BOM is formatted correctly.\n(Inconsistent column lengths)\n\n"
                     "Click OK to terminate.")

        else:
            sg.popup(f"An unforeseen error occurred: {values[event]}")
        break

    if event == "Update":
        current_file, total_files = values[event]
        window["progressbar"].update(current_file * 1000 / total_files)
        window["info"].update(f"Working file {current_file} of {total_files}.")

    if event == "Done":
        sg.popup("Process completed successfully!",
                 font=("Segoe UI Variable", 10))
        sys.exit()

window.close()