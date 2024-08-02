import pandas as pd
import glob
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

"""def stpFinder(source_dir):
    stp_files = glob.glob(f"{source_dir}\*.stp")
    return stp_files"""


