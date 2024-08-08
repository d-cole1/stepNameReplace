import PySimpleGUI as sg
import functions_new as fn
import os
import threading

# Define a custom theme for the GUI
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

# Add and set the custom theme
sg.theme_add_new("MyNewTheme", my_new_theme)
sg.theme("MyNewTheme")

# Set the default options for the GUI
sg.set_options(font=("Segoe UI Variable", 10))


# Function to execute the main processing
def execute_func(window, values):
    try:
        # Extract the data from the BOM file into a pd DataFrame
        df = fn.extract_mre_bom((values["excel"]))

        # Check the format of the BOM file
        bom_format = fn.check_bom_format(df)

        # Proceed if the BOM format is correct
        if bom_format:  # == True omitted

            # Find all step files in the source directory
            files = fn.stp_finder(values["source"])
            files = [item.replace("\\", "/") for item in files]  # Normalize the file paths
            print(f"Found {len(files)} .stp files")
            if len(files) <= 0:
                window.write_event_value("Error", "no_steps_found")

            total_files = len(files)

            # Create an output directory within the source directory
            output_dir = os.path.join(values["source"], "SNR_Output")
            os.makedirs(output_dir, exist_ok=True)

            # Process each step file
            for index, file in enumerate(files):

                # Create a new name for the output file
                new_name = os.path.join(output_dir, os.path.basename(file))

                # Update the progress bar
                window.write_event_value("Update", (index + 1, total_files))

                # Replace strings in the step file
                print(f"Processing file: {file}")
                fn.step_name_replace(file, df, new_name)

            # Indicate that the processing is done
            window.write_event_value("Done", None)

        else:
            window.write_event_value("Error", "invalid_BOM")

    except Exception as e:
        window.write_event_value("Error", str(e))


# Define the layout for the GUI
layout = [
    [sg.Input(), sg.FolderBrowse("Select Source Directory", key="source", pad=(5, 5))],
    [sg.Input(), sg.FileBrowse("Select BOM", key="excel", pad=(5, 5))],
    [sg.Button("Execute"),
     sg.ProgressBar(1000, orientation='h', pad=(9, 5), size=(19, 15), key='progressbar'),
     sg.Text("", key="info")]
]

# Create the main window with the specified layout
window_main = sg.Window(title="Step Name Replace (SNR)", layout=layout)

# Main event loop
while True:
    event, values = window_main.read()  # Read events and values from the window

    if event == sg.WIN_CLOSED:  # If the window is closed, exit the loop
        break

    elif event == "Execute":  # If the Execute button is clicked
        print(f"Source Directory: {values['source']}")
        print(f"Source Directory: {values['excel']}")

        # Start the execution function in a new thread
        threading.Thread(target=execute_func, args=(window_main, values), daemon=True).start()

    elif event == "Error":  # If an error occurs
        error_message = values[event]
        # print(values[event])
        if "[Errno 13]" in error_message:
            sg.popup("Ensure that the BOM is closed before running.\n\n"
                     "Click OK to terminate.")

        elif "[Errno 2]" in error_message:
            sg.popup("Ensure the correct BOM is selected.\n\n"
                     "Click OK to terminate.")

        elif error_message == "no_steps_found":
            sg.popup("No step files found, please select another folder.\n\n"
                     "Click OK to terminate.")

        elif error_message == "invalid_BOM":
            sg.popup("Ensure BOM is formatted correctly.\n(Inconsistent column lengths)\n\n"
                     "Click OK to terminate.")

        else:
            sg.popup(f"An unforeseen error occurred: {values[event]}\n\n"
                     f"Click OK to terminate.")
        break

    elif event == "Update":  # Update the progress bar
        current_file, total_files = values[event]
        window_main["progressbar"].update(current_file * 1000 / total_files)
        window_main["info"].update(f"Processing file {current_file} of {total_files}.")

    elif event == "Done":  # If processing is done
        sg.popup("Process completed successfully!\n",
                 font=("Segoe UI Variable", 10), custom_text="Close")
        break

window_main.close()  # Close the window
