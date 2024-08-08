from pandas import read_excel
import os


# searches selected directory and extracts stepfiles into list
def stpFinder(source_dir):
    stp_files = []
    extensions = (".stp", ".step", ".STP", ".STEP")
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(extensions):
                stp_files.append(os.path.join(root, file))
    return stp_files


# Reads BOM excel and returns dataframe
def extractMREBOM(path):
    df = read_excel(path, sheet_name="BOM", dtype="str")
    return df

def checkBOMFormat(df_arg):
    des_count = df_arg["DESCRIPTION"].count()
    num_count = df_arg["DOC NUMBER"].count()
    type_count = df_arg["DOC TYPE"].count()
    part_count = df_arg["DOC PART"].count()

    # Checks if BOM is formatted correctly before returning
    if des_count == num_count and type_count == part_count:
        return True
    else:
        return None


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
    file.close()
    output.close()
    return
