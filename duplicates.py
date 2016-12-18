#!/usr/local/bin/python3
import sys
import os

def get_fies_in_path(path):
	files_list = list()
	for entry in os.scandir(path):
		if entry.is_file(follow_symlinks=False):
			file = (entry.path, entry.name, entry.stat().st_size)
			files_list.append(file)
		elif entry.is_dir(follow_symlinks=False):
			files_list.extend(get_fies_in_path(entry.path))
	return files_list


def are_files_duplicates(file_stat1, file_stat2):
    return file_stat1[1] == file_stat2[1] and file_stat1[2] == file_stat2[2]

def get_duplicates_paths(files_list):
	duplicates = list()

	for file_stat1_num, file_stat1 in enumerate(files_list):
		current_file_duplicates = list()
		
		for file_stat2 in files_list[file_stat1_num:]:
			if are_files_duplicates(file_stat1, file_stat2):
				current_file_duplicates.append(file_stat2)

		if len(current_file_duplicates) > 1:
			duplicates.append(current_file_duplicates)

	return duplicates

def get_duplicates(path):
	try:
		files_list = get_fies_in_path(path)
	except:
		return None

	return get_duplicates_paths(files_list)


if __name__ == '__main__':
    if len(sys.argv) < 2:
    	print("Укажите путь к папке в качастве параметра скрипта")
    	exit()

    duplicates = get_duplicates(sys.argv[1])

    if not duplicates is None:
    	for block_of_duplicates in duplicates:
    		print("Имя файла:", block_of_duplicates[0][1], "Размер:", block_of_duplicates[0][2], "байт")
    		print("Дубликаты:")
    		for duplicate in block_of_duplicates:
    			print(duplicate[0])
    		print()
    else:
    	print("Ошибка")

