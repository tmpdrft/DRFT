from Modules.DRFT_Define import *
from termcolor import colored

def run_tool():
    os.system('cls')
    f = Figlet(font='big')
    print(colored(f.renderText('< D R F T >'), 'magenta'))
    print(colored("Data Remnants Forensics Tool\n\n", 'blue'))

def select_keyword():
    while True:
        print(colored("|############### Keyword Search ###############|", 'cyan'))
        print(colored("|   ex) dataremnantstest                       |", 'cyan'))
        print(colored("|   ex) randomfilename                         |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        keywordType = input("Type Keyword: ")
        return keywordType

def select_method():
    while True:
        print(colored("|################### Method ###################|", 'cyan'))
        print(colored("|   1. Identification (Test PC)                |", 'cyan'))
        print(colored("|   2. Examination (Target PC)                 |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        methodType = input("Select OS: ")
        if int(methodType) == 1 or int(methodType) == 2:
            return methodType
        else:
            print()
            print(colored("> Please type a correct number (1 or 2)\n", 'yellow'))

def select_os():
    while True:
        print(colored("|############## Operating System ##############|", 'cyan'))
        print(colored("|   1. Windows                                 |", 'cyan'))
        print(colored("|   2. macOS                                   |", 'cyan'))
        print(colored("|   3. Linux                                   |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        osType = input("Select OS: ")
        if int(osType) == 1 or int(osType) == 2:
            return osType
        elif int(osType) == 3:
            print()
            print(colored("> In development...", 'yellow'))
            print(colored("> Please select another OS type\n", 'yellow'))
        else:
            print()
            print(colored("> Please type a correct number (1~3)\n", 'yellow'))

def select_input():
    while True:
        print(colored("|################## I.N.P.U.T #################|", 'cyan'))
        print(colored("|   1. Live System                             |", 'cyan'))
        print(colored("|   2. Disk Image (e01 only)                   |", 'cyan'))
        print(colored("|   3. Directory                               |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        inputType = input("Select Input: ")
        if int(inputType) == 1 or int(inputType) == 2 or int(inputType) == 3:
            return inputType
        else:
            print()
            print(colored("> Please type a correct number (1~3)\n", 'yellow'))

def type_source_path():
    while True:
        print(colored("|################## P.A.T.H ###################|", 'cyan'))
        print(colored("|  ex) D:\source                               |", 'cyan'))
        #print(colored("|  ex) For testing, type 'allfiledeleted'      |", 'cyan'))
        print(colored("|  Please type folder name, not the filename   |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        inputType = input("Please type the source folder (absolute path): ")
        if os.path.isdir(inputType) == True:
            return inputType
        else:
            print()
            print(colored("> Please type a correct path\n", 'yellow'))

def type_user_name(sourceFolder):
    while True:
        print(colored("|################## U.S.E.R ###################|", 'cyan'))
        print(colored("|    ex) a                                     |", 'cyan'))
        print(colored("|    ex) b                                     |", 'cyan'))
        print(colored("|    ex) x (if you don't know the user name)   |", 'cyan'))
        print(colored("|##############################################|", 'cyan'))
        print()
        UserName = input("Please type the user name: ")
        if os.path.isdir(sourceFolder+'/Users/'+UserName) == True:
            return UserName
        elif UserName == 'x':
            return UserName
        else:
            print()
            print(colored("> Please type a correct user name or type 'x'\n", 'yellow'))