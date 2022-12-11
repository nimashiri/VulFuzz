import subprocess, os, logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

logging.basicConfig(level = logging.INFO)

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

import os

def runProcess(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
        retcode = p.poll()
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break

def run_tf_tests(data):
    _path_clean_tests = '/media/nimashiri/SSD1/FSE23_2/data/tf/tf_test_files/history.txt'
    _path_corrupted_tests = '/media/nimashiri/SSD1/FSE23_2/data/tf/tf_test_files/corrupted.txt'

    mode = 'a' if os.path.exists(_path_clean_tests) else 'w'
    f1 = open(_path_clean_tests, mode=mode)

    mode = 'a' if os.path.exists(_path_corrupted_tests) else 'w'
    f2 = open(_path_corrupted_tests, mode=mode)

    hist = read_txt(_path_clean_tests)
    corr = read_txt(_path_corrupted_tests)

    for i, t in enumerate(data):
        if t not in hist and t not in corr:

            client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=10, connectTimeoutMS=300)

            try:
                info = client.server_info()
                
            except ServerSelectionTimeoutError:
                logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                logging.info('#### MongoDB Server is Down! I am trying initiating the server now. ####')
                logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

                subprocess.call('rm -rf /media/nimashiri/DATA/mongodata/mongod.lock', shell=True)
                subprocess.run(['mongod', '--dbpath', '/media/nimashiri/DATA/mongodata/', '--logpath', '/media/nimashiri/DATA/mongolog/mongo.log', '--fork'])

            try:
                logging.info('##################################################################################')
                logging.info(f'The connection is OK! Going to run: {t}: {i}/{len(data)}')
                logging.info('##################################################################################')

                subprocess.run(['python3', t], timeout=150)
                write_list_to_txt4(t, _path_clean_tests)

            except subprocess.TimeoutExpired:
                write_list_to_txt4(t, _path_corrupted_tests)


        subprocess.call('find . -name "*.pb" -type f -delete', shell=True)
        subprocess.call('find . -name "*.ckpt" -type f -delete', shell=True)
        subprocess.call('find . -name "*.meta" -type f -delete', shell=True)
        subprocess.call('find . -name "*.saver" -type f -delete', shell=True)

if __name__ == '__main__':

    tf_tests = '/media/nimashiri/SSD1/FSE23_2/data/tf/tf_test_files/tf_tests_v2.4.0.txt'
    data = read_txt(tf_tests)
    run_tf_tests(data)

