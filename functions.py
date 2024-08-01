import os
import sys
import pandas


# Current Reading function, might be able to be improved/changed
def readDir(path):
    filename = []
    for root, d_names, f_names, in os.walk(path):
        for f in f_names:
            filename.append(os.path.join(root, f))
    return filename

# Current Main function
def stepNameReplace(file, dic, outName):
    output = open(outName, 'w+')
    stpFile = open(file, 'rb')
    for row in stpFile:
        tmpstr = row.decode("utf-8").replace(r"\r\n", r"\r")
        for k, v in dic.items():
            tmpstr = tmpstr.replace(k, v)
        output.write(tmpstr)
    output.close()
    return
