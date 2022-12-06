
import os
import sys, re
import argparse

def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    allFiles = filter_python_tests(allFiles)
    return allFiles

def filter_python_tests(target_files):
    filtered = []
    for f in target_files:
        if re.findall(r'\/test\/', f) or re.findall(r'\/tests\/', f):
            if f.endswith('.py'):
                filtered.append(f)
    return filtered

def main():
    target_path = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_test_files/tf_tests_v2.4.0.txt'
    tf_root_path = '/media/nimashiri/DATA/tensorflow/tensorflow'
    if not os.path.isfile(tf_root_path):
        # get list of all files
        _files = getListOfFiles(tf_root_path)
        # output the list to disk
        for f in _files:
            if re.findall(r'(\/lite\/)', f):
                continue
            else:
                write_list_to_txt4(f, target_path)
        

if __name__ == '__main__':
    main()