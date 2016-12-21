import sys
import os


def get_fies_in_path(path, files_dict):

    for entry in os.scandir(path):
        if entry.is_file(follow_symlinks=False):
            file_stat_key = (entry.name, entry.stat().st_size)

            if file_stat_key not in files_dict:
                files_dict[file_stat_key] = []

            files_dict[file_stat_key].append(entry.path)

        elif entry.is_dir(follow_symlinks=False):
            get_fies_in_path(entry.path, files_dict)


def get_duplicates(path):
    files_dict = {}
    try:
        get_fies_in_path(path, files_dict)
    except:
        return None

    for file_stat_key in list(files_dict):
        if len(files_dict[file_stat_key]) < 2:
            del files_dict[file_stat_key]

    return files_dict


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Укажите путь к папке в качастве параметра скрипта")
        exit(1)

    duplicates_dict = get_duplicates(sys.argv[1])

    for file_stat, duplicates_list in duplicates_dict.items():
        print("Имя:", file_stat[0], "Размер:", file_stat[1], "байт")
        for duplicate_path in duplicates_list:
            print(duplicate_path)
        print()
