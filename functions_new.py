from pandas import read_excel
import os
import sys
import PySimpleGUI as sg

# searches selected directory and extracts stepfiles into list
def stpFinder(source_dir):
    stp_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".stp"):
                stp_files.append(os.path.join(root, file))
            elif file.endswith(".step"):
                stp_files.append(os.path.join(root, file))
    return stp_files


# Reads BOM excel and returns dataframe
def extractMREBOM(path):
    df = read_excel(path, sheet_name="BOM", dtype="str")

    des_count = df["DESCRIPTION"].count()
    num_count = df["DOC NUMBER"].count()
    type_count = df["DOC TYPE"].count()
    part_count = df["DOC PART"].count()

    # Checks if BOM is formatted correctly before returning df
    if des_count == num_count and type_count == part_count:
        return df

    else:
        sg.popup("BOM formatted incorrectly (Inconsistent number of rows)\n \n"
                 "Click OK to Terminate",
                 font=("Segoe UI Variable", 10))
        sys.exit()


# Uses returned dataframe to replace string names with BOM Description, then rename
def stepNameReplace(filepath_arg, df_arg, newName):

    output = open(newName, 'w+')
    file = open(filepath_arg, 'rb')

    for row in file:
        tmp_str = row.decode("utf-8").replace("\r\n", "\r")

        # Perform all replacements for the current line
        for i in range(len(df_arg["DESCRIPTION"])):
            tmp_str = tmp_str.replace(
                f"{df_arg['DOC NUMBER'][i]}_{df_arg['DOC TYPE'][i].upper()}_{df_arg['DOC PART'][i]}",
                df_arg['DESCRIPTION'][i])  # case Upper

            tmp_str = tmp_str.replace(
                f"{df_arg['DOC NUMBER'][i]}_{df_arg['DOC TYPE'][i].lower()}_{df_arg['DOC PART'][i]}",
                df_arg['DESCRIPTION'][i])  # case Lower

        # After all replacements, write the modified line to the output file
        output.write(tmp_str)
    output.close()
    return

