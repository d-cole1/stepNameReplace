from pandas import read_excel
import os

# MAIN FUNCTION
def execute_func(window, values):
    if not validate_inputs(window, values):
        return

    try:
        # Extract the data from the BOM file into a pd DataFrame
        df = extract_mre_bom(str((values["excel"])))

        # Find all step files in the source directory
        files = stp_finder(values["source"])

        # Create an output directory within the source directory
        output_dir = os.path.join(values["source"], "SNR_Output")
        os.makedirs(output_dir, exist_ok=True)

        process_files(window, files, df, output_dir)

        # Indicate that the processing is done
        window.write_event_value("Done", None)

    except Exception as e:
        window.write_event_value("Error", str(e))

# HELPER FUNCTIONS
def validate_inputs(window, values):
    try:
        df = extract_mre_bom(str(values['excel']))
        files = stp_finder(values['source'])

        if not check_bom_format(df):
            window.write_event_value("Error", "invalid_BOM")
            return False

        if not files:
            window.write_event_value("Error", "no_steps_found")
            return False

        return True

    except FileNotFoundError:
        window.write_event_value("Error", "no_bom")

# Searches the selected directory and extracts step files into a list
def stp_finder(source_dir):
    stp_files = []  # Initialize an empty list to store step files
    extensions = (".stp", ".step", ".STP", ".STEP")  # Define the files extensions to look for
    for root, dirs, files in os.walk(source_dir):  # Walk through the directory
        for file in files:  # Iterate over the files in the directory
            if file.endswith(extensions):  # Check if the file has a step extension
                stp_files.append(os.path.join(root, file))  # Add the files to the list
    stp_files = [item.replace("\\", "/") for item in stp_files]  # Normalize the file paths
    return stp_files

# Reads the BOM file and returns a pd DataFrame
def extract_mre_bom(path):
    return read_excel(path, sheet_name="BOM", dtype="str")

# Checks the format of the BOM DataFrame
def check_bom_format(df_arg):
    des_count = df_arg["DESCRIPTION"].count()
    num_count = df_arg["DOC NUMBER"].count()
    type_count = df_arg["DOC TYPE"].count()
    part_count = df_arg["DOC PART"].count()

    # Check if the BOM is formatted correctly
    return des_count == num_count and type_count == part_count  # Correct

def process_files(window, files, df, output_dir):
    for index, file in enumerate(files):
        print(index)
        print(file)
        # Update the progress bar
        window.write_event_value("Update", (index + 1, len(files)))

        # Replace strings in the step file and rename the file
        step_name_replace(file, df, output_dir)

def get_replacements(df_arg):
    # Create a dictionary for matching replacement keys with BOM description values
    replacements = {}

    # Loop through each row in the DataFrame
    for i in range(len(df_arg["DESCRIPTION"])):
        doc_part = df_arg['DOC PART'][i]
        zero_count = len(doc_part)

        # Check for number of zeros in ['DOC PART']
        if zero_count == 1:
            doc_part = '000'
        elif zero_count == 3:
            pass

        # Create a key for each case
        key_upper = f"{df_arg['DOC NUMBER'][i]}_{df_arg['DOC TYPE'][i].upper()}_{doc_part}"
        key_lower = f"{df_arg['DOC NUMBER'][i]}_{df_arg['DOC TYPE'][i].lower()}_{doc_part}"

        # Add the keys to the dictionary with their corresponding description as the value
        replacements[key_upper] = df_arg['DESCRIPTION'][i]
        replacements[key_lower] = df_arg['DESCRIPTION'][i]

    return replacements

def use_replacements(filepath_arg, replacements, output_dir):
    key_found = False
    value = None
    # Open original file for reading
    with open(filepath_arg, 'rb') as file:
        lines = file.readlines()

    # Perform replacements and check for key presence
    for row in lines:
        tmp_str = row.decode("utf-8").replace("\r\n", "\r")  # Decode the line and replace line ending

        # Perform all replacements for the current line
        for key, val in replacements.items():
            if key in tmp_str:
                key_found = True
                value = val
            tmp_str = tmp_str.replace(key, val)

    if key_found:
        # Create a new name for the output file
        new_filename = f"{value}.stp"
        new_file_path = os.path.join(output_dir, new_filename)

        # Write the modified content to the new file
        with open(new_file_path, 'w+') as output:
            for row in lines:
                tmp_str = row.decode("utf-8").replace("\r\n", "\r")  # Decode the line and replace line ending

                # Perform all replacements for the current line
                for key, val in replacements.items():
                    tmp_str = tmp_str.replace(key, val)

                # After all replacements, write the modified line to the output file and restore original line ending
                output.write(tmp_str.replace("\r", "\n"))

def step_name_replace(filepath_arg, df_arg, output_dir):
    replacements = get_replacements(df_arg)
    use_replacements(filepath_arg, replacements, output_dir)
