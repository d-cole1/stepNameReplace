from pandas import read_excel
import os


# Searches the selected directory and extracts step files into a list
def stp_finder(source_dir):
    stp_files = []  # Initialize an empty list to store step files
    extensions = (".stp", ".step", ".STP", ".STEP")  # Define the files extensions to look for
    for root, dirs, files in os.walk(source_dir):  # Walk through the directory
        for file in files:  # Iterate over the files in the directory
            if file.endswith(extensions):  # Check if the file has a step extension
                stp_files.append(os.path.join(root, file))  # Add the files to the list
    return stp_files


# Reads the BOM file and returns a pd DataFrame
def extract_mre_bom(path):
    df = read_excel(path, sheet_name="BOM", dtype="str")
    return df


# Checks the format of the BOM DataFrame
def check_bom_format(df_arg):
    des_count = df_arg["DESCRIPTION"].count()
    num_count = df_arg["DOC NUMBER"].count()
    type_count = df_arg["DOC TYPE"].count()
    part_count = df_arg["DOC PART"].count()

    # Check if the BOM is formatted correctly
    if des_count == num_count and type_count == part_count:  # Correct
        return True
    else:  # Incorrect
        return None


# Uses DataFrame to replace string names with BOM descriptions, then rename the file
def step_name_replace(filepath_arg, df_arg, new_name):

    output = open(new_name, 'w+')  # Open new file for writing
    file = open(filepath_arg, 'rb')  # Open original file for reading

    for row in file:  # Iterate over each row in the file
        tmp_str = row.decode("utf-8").replace("\r\n", "\r")  # Decode the line and replace line ending

        # Perform all replacements for the current line
        for i in range(len(df_arg["DESCRIPTION"])):
            tmp_str = tmp_str.replace(
                f"{df_arg['DOC NUMBER'][i]}_{df_arg['DOC TYPE'][i].upper()}_{df_arg['DOC PART'][i]}",
                df_arg['DESCRIPTION'][i])  # Replace if upper case

            tmp_str = tmp_str.replace(
                f"{df_arg['DOC NUMBER'][i]}_{df_arg['DOC TYPE'][i].lower()}_{df_arg['DOC PART'][i]}",
                df_arg['DESCRIPTION'][i])  # Replace if lower case

        # After all replacements, write the modified line to the output file
        output.write(tmp_str)
    file.close()  # Close the original file
    output.close()  # Close the output file
    return
