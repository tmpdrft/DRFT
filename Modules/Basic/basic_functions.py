from Modules.DRFT_Define import *

###################################################### Basic functions
def file_copy(fileA,fileb):
    shutil.copy2(fileA, fileb)

def temp_folder_creation(folderName):
    if os.path.exists(folderName):
        shutil.rmtree(folderName)
    os.makedirs(folderName)

def check_file_in_folder(path_dir):
    filelist = os.listdir(path_dir)
    return filelist

def plistparser(fullpath):
    with open(fullpath, 'rb') as fp:
        return plistlib.load(fp)

def sqliteparser(fullpath):
    conn = sqlite3.connect(fullpath)
    return conn.cursor()

def parse_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def parse_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def parse_binary_text_file(file_path):
    with open(file_path, 'rb') as file:
        lines = file.read()
    return lines