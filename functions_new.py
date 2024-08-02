import pandas as pd
import os


def stpFinder(source_dir):
    stp_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".stp"):
                stp_files.append(os.path.join(root, file))
            elif file.endswith(".step"):
                stp_files.append(os.path.join(root, file))
    return stp_files


def excelExtract(path):
    dic = {}
    df = pd.read_excel(path, sheet_name="BOM", dtype="str")
    for index, row in df.iterrows():
        print(f"Index {index}")
        print(f"{row['DOC NUMBER']}_{row['DOC TYPE']}_{row['DOC PART']}")
        print(f"{row['Part Number']} ^ {row['Customer Revision']}\n")
    return df