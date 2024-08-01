import os
import sys
import pandas

def readDir(path):
    filename = []
    for root, d_names, f_names, in os.walk(path):
        for f in f_names:
            filename.append(os.path.join(root, f))
    return filename



