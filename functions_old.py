# Function: To parse step files and attempt find/replace names
#
#

import os
import sys


####### Helper Functions

def readDirFull(path):
    fname = []
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            fname.append(os.path.join(root, f))
    return fname


def readDirFiles(path):
    fname = []
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            fname.append(f)
    return fname


####### Main Function
def stepNameReplace(file, dic, outName):
    output = open(outName, 'w+')
    stpFile = open(file, 'rb')
    for row in stpFile:
        tmpstr = row.decode("utf-8").replace("\r\n", "\r")
        for k, v in dic.items():
            tmpstr = tmpstr.replace(k, v)
        output.write(tmpstr)
    output.close()
    return


## Runs Main Function if this is top function
if __name__ == "__main__":
    dir = sys.argv[1]
    try:
        os.chdir(dir)
    except:
        print("Could not find the path you were looking for")
        sys.exit()

    ## Find Thicknesses
    files = [i for i in tuple(readDirFull(os.getcwd())) if ('.stp' in i) or ('.STP' in i)]

    ## Create Dictionary of Replace
    dic = { \
        '20178534_MUP_000': '11007100 ^ MRE004', \
        '20009384_MUP_000': '11588685', \
        '20009382_MUP_000': '11588316', \
        '20009386_MUP_000': '11611072', \
        '20009628_MUP_000': '11588324 ^ 009', \
        '20008514_MUP_000': '11588322 ^ 010', \
        '20178828_MUP_000': '11007137 ^ MRE001', \
        '20177626_MUP_000': 'BKC22177 ^ 001.0001', \
        '20177623_MUP_000': 'BKC22044 ^ 001.0001', \
        '20177619_MUP_000': 'BKC22037 ^ 001.0001', \
        '20178614_MUP_000': '11007120 ^ MRE003', \
        '20178615_MUP_000': '11007121 ^ MRE001', \
        '20178630_MUP_000': '11007119 ^ MRE001', \
        '20178618_MUP_000': '11007122 ^ MRE001', \
        '20178836_MUP_000': '11007141 ^ MRE001', \
        '20178839_MUP_000': '11007142 ^ MRE002', \
        '20178834_MUP_000': '11007139 ^ MRE002', \
        '20178835_MUP_000': '11007140 ^ MRE002', \
        '20178533_MUP_000': '11007101 ^ MRE003', \
        '20178613_MUP_000': '11007103 ^ MRE003', \
        '20178616_MUP_000': '11007102 ^ MRE003', \
        '20178617_MUP_000': '11007104 ^ MRE002', \
        '20178668_MUP_000': '11007126 ^ MRE003', \
        '20178671_MUP_000': '11007127 ^ MRE003', \
        '20178641_MUP_000': '11007109 ^ MRE003', \
        '20178644_MUP_000': '11007110 ^ MRE003', \
        '20178619_MUP_000': '11007111 ^ MRE001', \
        '20178620_MUP_000': '11007112 ^ MRE001', \
        '20178537_MUP_000': '11007107 ^ MRE002', \
        '20178539_MUP_000': '11007108 ^ MRE003', \
        '20178549_MUP_000': '11007105 ^ MRE002', \
        '20178589_MUP_000': '11007106 ^ MRE002', \
        '20178625_MUP_000': '11007114 ^ MRE002', \
        '20178622_MUP_000': '11007113 ^ MRE002', \
        '20178626_MUP_000': '11007116 ^ MRE002', \
        '20178623_MUP_000': '11007115 ^ MRE002', \
        '20178638_MUP_000': '11007124 ^ MRE002', \
        '20178680_MUP_000': '11007129 ^ MRE003', \
        '20178682_MUP_000': '11007131 ^ MRE003', \
        '20178681_MUP_000': '11007130 ^ MRE003', \
        '20178683_MUP_000': '11007132 ^ MRE003', \
        '20178816_MUP_000': '11007133 ^ MRE002', \
        '20178823_MUP_000': '11007134 ^ MRE002', \
        '20178824_MUP_000': '11007135 ^ MRE002', \
        '20178825_MUP_000': '11007136 ^ MRE002', \
        '20178831_MUP_000': '11007138 ^ MRE002', \
        '20178979_MUP_000': '11007143 ^ MRE002', \
        '20178981_MUP_000': '11007145 ^ MRE001', \
        '20178980_MUP_000': '11007144 ^ MRE001', \
        '20178982_MUP_000': '11007146 ^ MRE001', \
        '20177654_MUP_000': 'BKC41217 ^ 001.0002', \
        '20177864_MUP_000': 'AGU10830 ^ MRE001', \
        '20178679_MUP_000': '11007128 ^ MRE002', \
        '20178627_MUP_000': '11007117 ^ MRE004', \
        '20178628_MUP_000': '11007118 ^ MRE004', \
        '20178534_mup_000': '11007100 ^ MRE004', \
        '20009384_mup_000': '11588685', \
        '20009382_mup_000': '11588316', \
        '20009386_mup_000': '11611072', \
        '20009628_mup_000': '11588324 ^ 009', \
        '20008514_mup_000': '11588322 ^ 010', \
        '20178828_mup_000': '11007137 ^ MRE001', \
        '20177626_mup_000': 'BKC22177 ^ 001.0001', \
        '20177623_mup_000': 'BKC22044 ^ 001.0001', \
        '20177619_mup_000': 'BKC22037 ^ 001.0001', \
        '20178614_mup_000': '11007120 ^ MRE003', \
        '20178615_mup_000': '11007121 ^ MRE001', \
        '20178630_mup_000': '11007119 ^ MRE001', \
        '20178618_mup_000': '11007122 ^ MRE001', \
        '20178836_mup_000': '11007141 ^ MRE001', \
        '20178839_mup_000': '11007142 ^ MRE002', \
        '20178834_mup_000': '11007139 ^ MRE002', \
        '20178835_mup_000': '11007140 ^ MRE002', \
        '20178533_mup_000': '11007101 ^ MRE003', \
        '20178613_mup_000': '11007103 ^ MRE003', \
        '20178616_mup_000': '11007102 ^ MRE003', \
        '20178617_mup_000': '11007104 ^ MRE002', \
        '20178668_mup_000': '11007126 ^ MRE003', \
        '20178671_mup_000': '11007127 ^ MRE003', \
        '20178641_mup_000': '11007109 ^ MRE003', \
        '20178644_mup_000': '11007110 ^ MRE003', \
        '20178619_mup_000': '11007111 ^ MRE001', \
        '20178620_mup_000': '11007112 ^ MRE001', \
        '20178537_mup_000': '11007107 ^ MRE002', \
        '20178539_mup_000': '11007108 ^ MRE003', \
        '20178549_mup_000': '11007105 ^ MRE002', \
        '20178589_mup_000': '11007106 ^ MRE002', \
        '20178625_mup_000': '11007114 ^ MRE002', \
        '20178622_mup_000': '11007113 ^ MRE002', \
        '20178626_mup_000': '11007116 ^ MRE002', \
        '20178623_mup_000': '11007115 ^ MRE002', \
        '20178638_mup_000': '11007124 ^ MRE002', \
        '20178680_mup_000': '11007129 ^ MRE003', \
        '20178682_mup_000': '11007131 ^ MRE003', \
        '20178681_mup_000': '11007130 ^ MRE003', \
        '20178683_mup_000': '11007132 ^ MRE003', \
        '20178816_mup_000': '11007133 ^ MRE002', \
        '20178823_mup_000': '11007134 ^ MRE002', \
        '20178824_mup_000': '11007135 ^ MRE002', \
        '20178825_mup_000': '11007136 ^ MRE002', \
        '20178831_mup_000': '11007138 ^ MRE002', \
        '20178979_mup_000': '11007143 ^ MRE002', \
        '20178981_mup_000': '11007145 ^ MRE001', \
        '20178980_mup_000': '11007144 ^ MRE001', \
        '20178982_mup_000': '11007146 ^ MRE001', \
        '20177654_mup_000': 'BKC41217 ^ 001.0002', \
        '20177864_mup_000': 'AGU10830 ^ MRE001', \
        '20178679_mup_000': '11007128 ^ MRE002', \
        '20178627_mup_000': '11007117 ^ MRE004', \
        '20178628_mup_000': '11007118 ^ MRE004'}

    print("Welcome Weary Traveler, Please Hold While I analyze the Folder for Step Files \n")
    print("I have Found These:")
    print(files)
    print("\n")
    mypath = input('press ENTER to CONTINUE')
    for f in files:
        stepNameReplace(f, dic, os.path.basename(f).replace(".stp", "_rename.stp"))

    ## Run Script
    stepNameReplace(dir, dic, 'out.step')
    print("script run successfully")

    mypath = input('press ENTER to CLOSE this window')