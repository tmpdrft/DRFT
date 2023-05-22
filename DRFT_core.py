import Modules.Basic.basic_functions as bf
import Modules.ExtractionConnector as ec
import Modules.AnalyzerConnector as ac
import Modules.DRFT_Display as tdi
from Modules.DRFT_Define import *

logger = logging.getLogger(__name__)

class EWFImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EWFImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()

def get_ewf_files_in_directory(directory):
    ewf_files = []
    for file in sorted(os.listdir(directory)):
        if re.match(r'^.*\.E[a-z,A-Z,0-9]{2}$', file):
            ewf_files.append(os.path.join(directory, file))
    return ewf_files

def keyword_search_in_file(file_entry, keyword):
    if file_entry.info.meta.size != 0 and file_entry.info.meta.size < 1000000000: # Less than 1GB
        file_entry_data = file_entry.read_random(0, file_entry.info.meta.size)
        if keyword.encode('utf-8') in file_entry_data:
            return True
        elif keyword.encode('utf-16le') in file_entry_data:
            return True
        else:
            return False

# (file extraction) DRF files
def extract_and_save_file(file_entry, extracted_folder, path):
    file_name = str(file_entry.info.name.name, 'utf-8')
    file_data = file_entry.read_random(0, file_entry.info.meta.size)

    os.makedirs(extracted_folder + '/' + "/".join(path), exist_ok=True)

    output_file = open(os.path.join(extracted_folder + '/' + "/".join(path), file_name), 'wb')
    output_file.write(file_data)
    output_file.close()

def extract_unique_strings(output_file):
    old_list = {
        r'^[0-9a-f-]+_adal_._.*\.json$', r'^w-mru\d+-[a-z,A-Z]{2}-[a-z,A-Z]{2}-sr(\[\d+\])?\.json$',
        r'^w-rec-[a-z,A-Z]{2}-[a-z,A-Z]{2}-sr(\[\d+\])?\.json$', r'^documents\_[a-z]{2}-[a-z,A-Z]{2}$',
        r'^places[a-z]{2}-[A-Z]{2}$', r'^[0-9]{19}.c4$', r'^safeDelete.db$',
        r'^launcher_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}.[0-9]{2}.log$',
        r'^msteams_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}.[0-9]{2}.log$',
        r'^app_settings.json$', r'^drive_fs_[0-9]{1}.txt$', r'^mpwpptracing-.*\.bin$',
        r'^edb[0-9]{5}\.jtx$', r'^mplog-[0-9]{8}-.*\.log$', r'^ntuser.dat.*', r'.*\.lnk$',
        r'^mirror_metadata_sqlite.db.*', r'^webcachev01.dat$', r'^mirror_sqlite.db.*', r'^root-state.json$',
        r'^.*\.s$', r'^oalerts.evtx$', r'^data_[0-9]{1}$', r'.*\.automaticdestinations-ms$',
        r'.*\.customdestinations-ms$', r'^[0-9]{6}.ldb$', r'^index.dat$', r'.*\.web$', r'^history$',
        r'^[0-9]{1}$', r'^settings.dat.*', r'^\$mft$', r'^appquota.edb$', r'^v01.log$', r'^cache$', r'^\$logfile$',
        r'^edb.jtx$', r'^edb.log$', r'^metadata_sqlite_db.*', r'^wpndatabase.db.*', r'^mpenginedb.db.*',
        r'^activitiescache.db.*', r'^metrics_store_sqlite.db.*', r'^downloadmetadata$', r'^[0-9,a-z,A-Z]{64}\.json$',
        r'^{.*}\.json$', r'^structured_log_.*}', r'.*.asd$', r'^windows.edb$', r'^iclouddrive.db.*', r'^favicons$',
        r'^safedelete.db.*', r'^[0-9]{6}.log$', r'^v01[0-9]{4}.*\.log$', r'^tabs_.*', r'^edb[0-9]{5}\.jtx$',
        r'^systemindex\.[0-9]{1}\.gthr$',
        r'^[0-9,a-z,A-Z]{8}-[0-9,a-z,A-Z]{4}-[0-9,a-z,A-Z]{4}-[0-9,a-z,A-Z]{4}-.*\.dat$',
        r'.*\.ost$', r'[0-9,a-z,A-Z]{8}\.bin', r'^v[0-9]{2}tmp\.log$', r'^logs\.txt$', r'^winsetupmon\.log$'
    }
    unique_file_list = []

    file_list = open(output_file, 'r')
    temp2 = file_list.readlines()

    for b_file_list in temp2:
        is_match = False

        for a_patterns in old_list:
            if re.match(a_patterns, b_file_list.replace("\n", "")):
                is_match = True
                break
        if not is_match:
            unique_file_list.append(b_file_list.replace("\n", ""))

    output_file.close()
    return unique_file_list


# (file extraction) existing file
def file_extraction_w(directory, file_list, extracted_folder):
    for file_entry in directory:
        if file_entry.info.name.name in [b'.', b'..']:
            continue
        try:
            f_type = file_entry.info.meta.type
        except:
            continue
        if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
            sub_directory = file_entry.as_directory()
            file_extraction_w(sub_directory, file_list, extracted_folder)
        elif f_type == pytsk3.TSK_FS_META_TYPE_REG:
            # only MS Office
            if '.docx' in str(file_entry.info.name.name, 'utf-8') or '.pptx' in str(file_entry.info.name.name, 'utf-8') or '.xlsx' in str(file_entry.info.name.name, 'utf-8'):
                file_list.append(str(file_entry.info.name.name, 'utf-8'))
    return file_list

def trace_evidence_parser_w(path_dir):
    temp_list = [] # Initialize
    final_list = []
    temp_list.append(ac.msofficeParser_w(path_dir))
    temp_list.append(ac.msonedriveParser_w(path_dir))
    temp_list.append(ac.msteamsParser_w(path_dir))

    for i in temp_list:
        for j in i:
            final_list.append(j)

    logger.info("Data Remnants Analysis completed")
    return(final_list)

def file_comparison(trace_file_list, all_file_list):
    result_file_list = []
    for trace_file in trace_file_list:
        count = 0
        for exist_file in all_file_list:
            if trace_file.name == exist_file.split('.')[0]:
                count = 1
                break
        if count == 0:
            result_file_list.append(trace_file)

    logger.info("File comparison completed")
    return result_file_list

def print_output(username, data_for_output):
    des = f'Result/{username}'
    bf.temp_folder_creation(des)
    with open(f'{des}/result.csv', 'w', newline='', encoding='utf-8-sig') as f:
        wr = csv.writer(f)
        wr.writerow(
            ['Filename', 'Extension', 'Filepath', 'Content', 'Created Timestamp','Modified Timestamp', 'Accessed Timestamp', 'Filesize', 'Type', 'Source'])
        for i in range(0, len(data_for_output)):
            if data_for_output[i].name != '':
                wr.writerow(
                    [data_for_output[i].name, data_for_output[i].ext, data_for_output[i].path, data_for_output[i].content,
                     data_for_output[i].c_timestamp, data_for_output[i].m_timestamp, data_for_output[i].a_timestamp, data_for_output[i].size,
                     data_for_output[i].type, data_for_output[i].source])

    logger.info("Output printed to CSV file")

def process_directory(directory, keyword, file_list, extracted_folder, path):
    for file_entry in directory:
        if file_entry.info.name.name in [b'.', b'..']:
            continue
        try:
            try:
                f_type = file_entry.info.meta.type
            except:
                continue
            if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
                sub_directory = file_entry.as_directory()
                path.append(file_entry.info.name.name.decode())
                process_directory(sub_directory, keyword, file_list, extracted_folder, path)
                path.pop(-1)
            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and file_entry.info.meta.size != 0:
                if keyword_search_in_file(file_entry, keyword):
                    file_list.append(file_entry)
                    # Extract files from the input source
                    extract_and_save_file(file_entry, extracted_folder, path)
        except IOError as e:
            pass

def main(ewf_files, keyword, identification_folder):

    extracted_folder = identification_folder + '/extracted_folder_from_image'
    os.makedirs(extracted_folder, exist_ok=True)

    ewf_handle = pyewf.handle()
    ewf_handle.open(ewf_files)

    img_info = EWFImgInfo(ewf_handle)
    volume = pytsk3.Volume_Info(img_info)

    for part in volume:
        try:
            print(f"Partition {part.addr}: {part.desc}")
            file_system = pytsk3.FS_Info(img_info, offset=part.start * volume.info.block_size)
            directory = file_system.open_dir(path="/")
            file_list = []

            process_directory(directory, keyword, file_list, extracted_folder, [])

            extracted_file_list = []
            for file_entry in file_list:
                extracted_file_list.append(str(file_entry.info.name.name, 'utf-8'))
            extracted_file_list = set(map(str.lower, extracted_file_list))

            print(f"Found {len(extracted_file_list)} files containing the keyword '{keyword}' in partition {part.addr}")
            for extracted_file in extracted_file_list:
                print(extracted_file)

            output_file = identification_folder + "/extracted_file_list.txt"
            log_file = open(output_file, 'a', encoding='utf-8')
            for extracted_file in extracted_file_list:
                log_file.write(extracted_file + '\n')
            log_file.close()

            # EXTRACT UDRF
            output_file_for_compare = output_file
            unique_strings = extract_unique_strings(output_file_for_compare)

            new_DRF_list_temp = []
            for new_DRF in unique_strings:
                new_DRF_list_temp.append(new_DRF)

            output_file = identification_folder + "/new_DRF_list.txt"
            new_file = open(output_file, 'a', encoding='utf-8')
            for new_DRF in new_DRF_list_temp:
                new_file.write(new_DRF + '\n')

        except Exception as e:
            print(f"Partition {part.addr} not supported, skipping. Reason: {str(e)}")

class DRTF_Core():
    def __init__(self):
        self.trace_file_list = []
        self.data_for_output = []
        self.username = ''

    def run(self):
        logger.info("Starting DRF_TCore")
        tdi.run_tool()
        method_type = tdi.select_method()

        # method
        # Identification
        if method_type == '1':
            print("\n>Identification \n")

            source_folder = tdi.type_source_path()
            ewf_files = get_ewf_files_in_directory(source_folder)
            keyword = tdi.select_keyword()

            identification_folder = 'identification_result'
            os.makedirs(identification_folder, exist_ok=True)

            main(ewf_files, keyword, identification_folder)

        # Examination
        elif method_type == '2':
            print("\n>Examination \n")

            source_folder = tdi.type_source_path()
            ewf_files = get_ewf_files_in_directory(source_folder)

            # DRF ANALYSIS
            ex_file_list = trace_evidence_parser_w('identification_result/extracted_folder_from_image')

            # Extract all files (except Library folder)
            ewf_handle = pyewf.handle()
            ewf_handle.open(ewf_files)

            img_info = EWFImgInfo(ewf_handle)
            volume = pytsk3.Volume_Info(img_info)

            file_list = []
            for part in volume:
                try:
                    file_system = pytsk3.FS_Info(img_info, offset=part.start * volume.info.block_size)
                    directory = file_system.open_dir(path="/")
                    all_file_list = file_extraction_w(directory, file_list, 'identification_result/extracted_folder_from_image')
                except Exception as e:
                    print()

            # Compare the files
            self.data_for_output = file_comparison(set(ex_file_list), set(all_file_list))

            # Print Output
            print_output(self.username, self.data_for_output)

        logger.info("DRFT_Core completed")

if __name__ == '__main__':
    begin = DRTF_Core()
    begin.run()
    print(colored("\n\n--- Completed", 'blue'))


