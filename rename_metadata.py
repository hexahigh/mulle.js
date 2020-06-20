import json
import os
import shutil

cst_path_no = os.path.realpath('cst_out_new_NO')
cst_path_sw = os.path.realpath('cst_out_new_SE')


def get_files(folder, number):
    extensions = ['png', 'wav', 'json', 'txt']
    files = []
    for extension in extensions:
        file = os.path.join(folder, '%s.%s' % (number, extension))
        if os.path.exists(file):
            files.append(os.path.abspath(file))
    return files


def get_names(cst_folder):
    files_out = {}
    module_data = {}
    for module in os.scandir(cst_folder):
        module_key = module.name.upper()
        metadata_file = os.path.join(module, 'metadata.json')
        if not os.path.exists(metadata_file):
            continue
        files_out[module_key] = {}
        with open(metadata_file, 'r') as fp:
            metadata = json.load(fp)
            module_data[module_key] = {'library': metadata['libraries'][0]['name'], 'metadata_file': metadata_file}
            for library in metadata['libraries']:
                subfolder = library['name']
                for number, member in library['members'].items():
                    folder = os.path.join(module, subfolder)
                    files = get_files(folder, number)
                    member['name'] = member['name'].lower()
                    if not files:
                        continue
                    if not member['name'] in files_out[module_key]:
                        files_out[module_key][member['name']] = {}

                    files_out[module_key][member['name']][number] = {'files': files, 'module': module_key, 'library': library['name'], 'number': number}
    return files_out, module_data


files_no, module_data_no = get_names(cst_path_no)
files_sw, module_data_sw = get_names(cst_path_sw)
# pprint(files_no)

for module, names in files_no.items():
    if module not in files_sw:
        # print('Module %s not found' % module)
        continue
    shutil.copyfile(module_data_sw[module]['metadata_file'], module_data_no[module]['metadata_file'])

    original_folder = os.path.join(cst_path_no, module, module_data_no[module]['library'])
    rename_folder = original_folder + ' rename'
    orphan_folder = original_folder + ' orphans'

    if not os.path.exists(rename_folder):
        os.mkdir(rename_folder)

    for name, numbers in names.items():
        if name not in files_sw[module]:
            print('%s not found' % name)
            continue

        numbers_sw = files_sw[module][name]

        key = 0
        for data in numbers.values():
            data_sw = list(files_sw[module][name].values())[key]

            for file in data['files']:
                # print(file)
                root, ext = os.path.splitext(file)
                new_file = os.path.join(rename_folder, data_sw['number'] + ext)
                os.rename(file, new_file)
            key += 1

    if os.path.exists(rename_folder):
        if os.path.exists(original_folder):
            try:
                os.rmdir(original_folder)
            except OSError:
                os.rename(original_folder, orphan_folder)

        os.rename(rename_folder, original_folder)
