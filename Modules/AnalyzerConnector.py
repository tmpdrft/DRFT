from Modules.DRFT_Define import *

class Trace:
    def __init__(self):
        self.name = ''
        self.ext = ''
        self.path = []
        self.c_timestamp = ''
        self.m_timestamp = ''
        self.a_timestamp = ''
        self.size = ''
        self.content = ''
        self.type = ''
        self.source = ''

def msofficeParser_w(path_dir):
    datalist = []
    filecount = 0
    filelist = []
    for root, directories, files in os.walk(path_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            filelist.append(file_path)
    for fullpath in filelist:
        # TabCache
        if re.match(r"^[0-9a-f-]+_ADAL_._.*\.json$", fullpath.split('\\')[-1]):
            try:
                parsed_data = bf.parse_json_file(fullpath)
                for data in parsed_data['Items']:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = data['Title']
                    datalist[filecount].ext = data['FileType']
                    datalist[filecount].c_timestamp = data['CreatedTime']
                    datalist[filecount].m_timestamp = data['LastModifiedTime']
                    datalist[filecount].a_timestamp = data['LastViewedByMeTime']
                    datalist[filecount].size = data['Size']
                    datalist[filecount].content = data['Summary']
                    datalist[filecount].path = data['Path']
                    datalist[filecount].type = 'MSOFFICE - TabCache'
                    datalist[filecount].source = fullpath.split('\\')[-1]
                    filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing" + fullpath)

        # Aggmru
        elif re.match(r'^w-mru\d+-[a-zA-Z]{2}-[a-zA-Z]{2}-sr(\[\d+\])?\.json$', fullpath.split('\\')[-1]):
            try:
                parsed_data = bf.parse_json_file(fullpath)
                for data in parsed_data['documents']['items']:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = data['title']
                    datalist[filecount].ext = data['extension']
                    datalist[filecount].c_timestamp = data['creation_info']['timestamp']
                    datalist[filecount].m_timestamp = data['modification_info']['timestamp']
                    datalist[filecount].size = data['file_size']
                    datalist[filecount].path = data['url']
                    datalist[filecount].type = 'MSOFFICE - Aggmru - MRU'
                    datalist[filecount].source = fullpath.split('\\')[-1]
                    filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing" + fullpath)

        elif re.match(r'^w-rec-[a-zA-Z]{2}-[a-zA-Z]{2}-sr(\[\d+\])?\.json$', fullpath.split('\\')[-1]):
            try:
                parsed_data = bf.parse_json_file(fullpath)
                for data in parsed_data['documents_group']['documents']:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = data['title']
                    datalist[filecount].ext = data['extension']
                    datalist[filecount].c_timestamp = data['creation_info']['timestamp']
                    datalist[filecount].m_timestamp = data['modification_info']['timestamp']
                    datalist[filecount].size = data['file_size']
                    datalist[filecount].path = str(data['display_path'])
                    datalist[filecount].type = 'MSOFFICE - Aggmru - REC'
                    datalist[filecount].source = fullpath.split('\\')[-1]
                    filecount += 1
            except Exception as e:
                logging.error(f"Error occurred while parsing" + fullpath)

        # MruServiceCache
        elif re.match(r"^Documents_[a-z]{2}-[A-Z]{2}$", fullpath.split('\\')[-1]):
            parsed_data = bf.parse_json_file(fullpath)
            for data in parsed_data:
                data_info = Trace()
                datalist.append(data_info)
                datalist[filecount].name = data['FileName']
                datalist[filecount].ext = data['FileName'].split('.')[-1]
                datalist[filecount].a_timestamp = data['Timestamp']
                datalist[filecount].path = data['DocumentUrl']
                datalist[filecount].type = 'MSOFFICE - MruServiceCache - Documents'
                datalist[filecount].source = fullpath.split('\\')[-1]
                filecount += 1

        elif re.match(r"^Places[a-z]{2}-[A-Z]{2}$", fullpath.split('\\')[-1]):
            parsed_data = bf.parse_json_file(fullpath)
            for data in parsed_data:
                data_info = Trace()
                datalist.append(data_info)
                datalist[filecount].name = data['FileName']
                datalist[filecount].ext = data['FileName'].split('.')[-1]
                datalist[filecount].a_timestamp = data['Timestamp']
                datalist[filecount].path = data['DocumentUrl']
                datalist[filecount].type = 'MSOFFICE - MruServiceCache - Places'
                datalist[filecount].source = fullpath.split('\\')[-1]
                filecount += 1

        # MSOFFICE - C4
        elif re.match(r'^[0-9]{19}.C4$', fullpath.split('\\')[-1]):
            data = bf.parse_binary_text_file(fullpath)
            pattern_start = bytes.fromhex("43 3A 5C 55 73 65 72 73 5C")
            pattern_end = bytes.fromhex("D3 83 91 E7 0E 02")

            start_index = 0
            while True:
                start_index = data.find(pattern_start, start_index)
                if start_index == -1:
                    break
                end_index = data.find(pattern_end, start_index + len(pattern_start))
                if end_index == -1:
                    break

                pattern_data = str(data[start_index-9 + len(pattern_start):end_index])[1:]
                start_index = end_index + len(pattern_end)

                data_info = Trace()
                datalist.append(data_info)
                datalist[filecount].name = pattern_data.replace('/', '').split('\\')[-1]
                datalist[filecount].ext = pattern_data.replace('/', '').split('\\')[-1].split('.')[-1]
                datalist[filecount].path = pattern_data.replace('/', '')
                datalist[filecount].type = 'MSOFFICE - C4'
                datalist[filecount].source = fullpath.split('\\')[-1]
                filecount += 1

    return datalist

def msonedriveParser_w(path_dir):
    datalist = []
    filecount = 0
    filelist = []
    for root, directories, files in os.walk(path_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            filelist.append(file_path)

    for fullpath in filelist:
        # Safe Delete
        if re.match(r'^SafeDelete.db$', fullpath.split('\\')[-1]):
            cur = bf.sqliteparser(fullpath)

            # items_moved_to_recycle_bin
            cur.execute("SELECT itemName, notificationTime FROM items_moved_to_recycle_bin")
            rows = cur.fetchall()
            for row in rows:
                if '.' in row[0]:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = row[0].split('.')[:-1]
                    datalist[filecount].ext = row[0].split('.')[-1]
                    datalist[filecount].a_timestamp = row[1]
                    datalist[filecount].type = 'MS OneDrive - SafeDelete - db (items moved to recycle bin)'
                    datalist[filecount].source = fullpath.split('\\')[-1]
                    filecount += 1

            # filter_delete_info
            cur.execute("SELECT path, notificationTime FROM filter_delete_info")
            rows = cur.fetchall()
            for row in rows:
                if '.' in row[0]:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = row[0].split('\\')[-1]
                    datalist[filecount].ext = row[0].split('\\')[-1].split('.')[-1]
                    datalist[filecount].a_timestamp = row[1]
                    datalist[filecount].path = row[0]
                    datalist[filecount].type = 'MS OneDrive - SafeDelete - db (filter_delete_info)'
                    datalist[filecount].source = fullpath.split('\\')[-1]
                    filecount += 1

    return datalist

def msteamsParser_w(path_dir):
    datalist = []
    filecount = 0
    filelist = []
    for root, directories, files in os.walk(path_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            filelist.append(file_path)
    for fullpath in filelist:

        # Launcher - Log
        if re.match(r'^Launcher_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}.[0-9]{2}.log$', fullpath.split('\\')[-1]):
            parsed_data = bf.parse_text_file(fullpath)
            for data in parsed_data:
                if 'shared_files' in fullpath.split('\\')[-1] and 'shared_files":[]' not in fullpath.split('\\')[-1]:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = \
                    data.split('"shared_files":["')[1].split('"]')[0].replace('\\\\', '\\').split('\\')[-1]
                    datalist[filecount].ext = data.split('"shared_files":["')[1].split('"]')[0].split('.')[-1]
                    datalist[filecount].a_timestamp = data[0:26]
                    datalist[filecount].path = data.split('"shared_files":["')[1].split('"]')[0].replace('\\\\', '\\')
                    datalist[filecount].type = 'MS Teams -Launcher - Log'
                    datalist[filecount].source = fullpath.split('\\')[-1]
                    filecount += 1

        # MSTeams - Log
        elif re.match(r'^MSTeams_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}.[0-9]{2}.log$', fullpath.split('\\')[-1]):
            parsed_data = bf.parse_text_file(fullpath)
            for data in parsed_data:
                if 'shared_files' in fullpath.split('\\')[-1] and 'shared_files":[]' not in fullpath.split('\\')[-1]:
                    data_info = Trace()
                    datalist.append(data_info)
                    datalist[filecount].name = \
                    data.split('"shared_files":["')[1].split('"]')[0].replace('\\\\', '\\').split('\\')[-1]
                    datalist[filecount].ext = data.split('"shared_files":["')[1].split('"]')[0].split('.')[-1]
                    datalist[filecount].a_timestamp = data[0:26]
                    datalist[filecount].path = data.split('"shared_files":["')[1].split('"]')[0].replace('\\\\', '\\')
                    datalist[filecount].type = 'MS Teams - MSTeams - Log'
                    datalist[filecount].source = fullpath.split('\\')[-1]
                    filecount += 1

        # MSTeams - Appsettings
        elif re.match(r'^app_settings.json$', fullpath.split('\\')[-1]):
            parsed_data = bf.parse_json_file(fullpath)
            data_info = Trace()
            datalist.append(data_info)
            datalist[filecount].name = parsed_data['share_session']['files'][0].replace('\\\\','\\').split('\\')[-1]
            datalist[filecount].ext = parsed_data['share_session']['files'][0].split('.')[-1]
            datalist[filecount].path = parsed_data['share_session']['files'][0].replace('\\\\','\\')
            datalist[filecount].type = 'MSTeams - Appsettings'
            datalist[filecount].source = fullpath.split('\\')[-1]
            filecount += 1

    return datalist