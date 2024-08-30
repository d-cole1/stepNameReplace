import PySimpleGUI as sg
from functions import execute_func
from threading import Thread

# Define a custom theme for the GUI
my_new_theme = {'BACKGROUND': "#31363b",
                'TEXT': "#f9f1ee",
                'INPUT': "#232629",
                'TEXT_INPUT': "#f9f1ee",
                'SCROLL': "#333a41",
                'BUTTON': ('#31363b', '#0dd1fc'),
                'PROGRESS': ('#f9f1ee', '#31363b'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# Add and set the custom theme
sg.theme_add_new("MyNewTheme", my_new_theme)
sg.theme("MyNewTheme")
sg.set_options(font=("Helvetica", 13))

logo = r"C:\Users\dominick.cole\Python\stepNameReplace\logos\applogo.ico"
e_logo = r"C:\Users\dominick.cole\Python\stepNameReplace\logos\error.ico"
s_logo = r"C:\Users\dominick.cole\Python\stepNameReplace\logos\success.ico"

# Define the layout for the GUI
layout = [
    [sg.Text("Select folder:", size=(11, 1)), sg.Input(), sg.FolderBrowse("Browse", key="source", pad=(5, 5))],
    [sg.Text("Select BOM:", size=(11, 1)), sg.Input(),
     sg.FileBrowse("Browse", key="excel", pad=(5, 5), file_types=(('Excel', '.xlsx'),))],

    [sg.Button("Execute"),
     sg.ProgressBar(1000, orientation='h', pad=(7, 5), size=(30, 18), key='progressbar'),
     sg.Text("", key="info")]
]

# Create the main window with the specified layout
window = sg.Window(title="Step Name Replace (SNR)", layout=layout, icon=logo)

# Main event loop
while True:
    event, values = window.read()  # Read events and values from the window

    match event:

        case sg.WIN_CLOSED:  # If the window is closed, exit the loop
            break

        case "Execute":  # If the Execute button is clicked

            # Start the execution function in a new thread
            Thread(target=execute_func, args=(window, values), daemon=True).start()
            window["Execute"].update(disabled=True)
            window["source"].update(disabled=True)
            window["excel"].update(disabled=True)

        case "Done":  # If processing is done
            sg.popup("A new folder named ‘SNR_Output’ will appear in the folder you"
                     " originally selected.",
                     custom_text="Exit", icon=s_logo, title="SUCCESS!")
            break

        case "Update":  # Update the progress bar
            current_file, total_files = values[event]
            window["progressbar"].update(current_file * 1000 / total_files)
            window["info"].update(f"Processing file {current_file} of {total_files}.")

        case "Error":  # If an error occurs
            error_message = values[event]

            # print(values[event])
            if "[Errno 13]" in error_message:
                sg.popup("Ensure that the BOM is closed before running.\n",
                         icon=e_logo, custom_text="Exit", title="ERROR!")

            elif error_message == "no_bom":
                sg.popup("Ensure a BOM is selected.\n",
                         icon=e_logo, custom_text="Exit", title="ERROR!")

            elif error_message == "no_steps_found":
                sg.popup("No step files found, please select another folder.\n",
                         icon=e_logo, custom_text="Exit", title="ERROR!")

            elif error_message == "invalid_BOM":
                sg.popup("Ensure BOM is formatted correctly.\n(Inconsistent column lengths)\n",
                         icon=e_logo, custom_text="Exit", title="ERROR!")

            else:
                print(values[event])
                sg.popup(f"An unforeseen error occurred.\n"
                         f"{error_message}", icon=e_logo, custom_text="Exit")
            break

window.close()  # Close the window
