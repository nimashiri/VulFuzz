
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
import sys
from constants.enum import OracleType
from os.path import join
from utils.converter import str_to_bool
import tensorflow as tf
from classes.tf_library import TFLibrary
from classes.tf_api import TFAPI
from classes.database import TorchDatabase, TFDatabase
import subprocess
from utils.printer import dump_data
logging.basicConfig(level = logging.INFO)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

def check_connection():
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=10, connectTimeoutMS=300)

    try:
        info = client.server_info()
                
    except ServerSelectionTimeoutError:
        logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        logging.info('#### MongoDB Server is Down! I am trying initiating the server now. ####')
        logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

def find_skip_list(api_):
    flag_ = True
    skip_list = ['python.autograph', 'python.debug', 'python.distribute', 'python.eager', 'python.framework', 'python.grappler']
    if 'tf.' in  api_:
        return True
    else:
        split_api = api_.split('.')
        target = ".".join([split_api[1], split_api[2]])
        if target in skip_list:
            flag_ = False
    return flag_


def run_fuzzer():
    dbname = 'TF'
    tf_output_dir = '/media/nimashiri/SSD1/testing_results'
    mydb = myclient[dbname]
    check_connection()
    TFDatabase.database_config('localhost', 27017, 'TF')


    for api_ in mydb.list_collection_names():
        skip_flag = find_skip_list(api_)
        if skip_flag:
            try:
                res = subprocess.run(["python3", "/media/nimashiri/SSD1/FSE23_2/fuzzing/fuzzing_code.py", "TF", api_], shell=False, timeout=100)
            except subprocess.TimeoutExpired:
                dump_data(f"{api_}\n", join(tf_output_dir, "timeout.txt"), "a")
            except Exception as e:
                dump_data(f"{api_}\n  {e}\n", join(tf_output_dir, "runerror.txt"), "a")
            else:
                if res.returncode != 0:
                    dump_data(f"{api_}\n", join(tf_output_dir, "runcrash.txt"), "a")
        else:
            print('API Skipped!')

if __name__ == '__main__':
    run_fuzzer()