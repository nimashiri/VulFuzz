import subprocess, os
from multiprocessing import Pool
import multiprocessing, threading
from threading import Thread
import logging, re

logging.basicConfig(level = logging.INFO)

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def process_prerun(input_addr):
    print("executed {}. thread".format(input_addr))

def process_prerun(input_addr):
    print("executed {}. thread".format(input_addr))
def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')


def run_mxnet_tests(data):
    import os

    _path_clean_tests = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/mxnet/mxnet_test_files/history.txt'


    if not os.path.exists(_path_clean_tests):
        f1 = open(_path_clean_tests, 'a') 

    hist = read_txt(_path_clean_tests)

    for i, t in enumerate(data):
        if t not in hist:
            write_list_to_txt4(t, _path_clean_tests)
            logging.info('###############################################')
            logging.info(f'Current test is: {t}: {i}/{len(data)} test files has been executed!')
            logging.info('###############################################')

            status = subprocess.run(['nc', '-zvv', 'localhost', '27017'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if re.findall(r'(succeeded!)', status.stderr):
                try:
                    subprocess.run(['python3 -m pytest', t])
                except Exception as e:
                    print(e)
            else:
                subprocess.call('rm -rf /media/nimashiri/DATA/mongodata/mongod.lock', shell=True)
                subprocess.run(['mongod', '--dbpath', '/media/nimashiri/DATA/mongodata/', '--logpath', '/media/nimashiri/DATA/mongolog/mongo.log', '--fork'])

if __name__ == '__main__':
    subprocess.call('cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/mxnet/mxnet_test_files/write_tools.py /media/nimashiri/SSD1/mxnet/python/mxnet/', shell=True)

    torch_tests = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/mxnet/mxnet_test_files/mxnet.txt'
    data = read_txt(torch_tests)
    run_mxnet_tests(data)