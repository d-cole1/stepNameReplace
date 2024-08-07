import PySimpleGUI as sg
import functions_new as fn
import sys
import os
import threading

sg.theme("DefaultNoMoreNagging")
sg.set_options(font=("Segoe UI Variable", 10),
               progress_meter_color=("#bde0eb", "#f0f0f0"), progress_meter_border_depth=(1))

def execute_func(window, values):

        # Extracts data from BOM as a panda array
        df = fn.extractMREBOM((values["excel"]))

        # Checks format of BOM before continuing code-> if format is wrong, err msg
        BOM_format = fn.checkBOMFormat(df)

        # If it is correct, the rest of execute_func will run
        if BOM_format == True:
            try:
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

            except Exception as e:
                window.write_event_value("Error", str(e))
                """
                If an error occurs throughout this process, the error type will be returned when values['event']
                is called in the main loop
                """
        else:
            window.write_event_value("Error", "invalid_BOM")

# Sets layout for GUI
layout = [
    [sg.Input(), sg.FolderBrowse("Select Source Directory", key="source", pad=(5, 5))],
    [sg.Input(), sg.FileBrowse("Select BOM", key="excel", pad=(5, 5))],
    [sg.Button("Execute"),
     sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar'),
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
        # print(values[event])
        if values[event] == f"[Errno 13] Permission denied: '{values['excel']}'":
            sg.popup("Ensure that the BOM is closed before running.\n\n"
                     "Click OK to terminate.")
            sys.exit()

        if values[event] == "invalid_BOM":
            sg.popup("Ensure BOM is formatted correctly.\n(Inconsistent column lengths)\n\n"
                     "Click OK to terminate.")
            sys.exit()

        else:
            sg.popup(f"An unforeseen error occurred: {values[event]}")
            sys.exit()


    if event == "Update":
        current_file, total_files = values[event]
        window["progressbar"].update(current_file * 100 / total_files)
        window["info"].update(f"Working file {current_file} of {total_files}.")

    if event == "Done":
        sg.popup("Process completed successfully!",
                 font=("Segoe UI Variable", 10))
        sys.exit()

window.close()
