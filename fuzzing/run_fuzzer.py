
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
import sys, traceback
from constants.enum import OracleType
from os.path import join
from utils.converter import str_to_bool
import tensorflow as tf
from classes.tf_library import TFLibrary
from classes.tf_api import TFAPI
from classes.database import TorchDatabase, TFDatabase
import subprocess, re
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

class InterpreterError(Exception): pass

def my_exec(cmd, globals=None, locals=None, description='source string'):
    existence_flag = False
    try:
        exec(cmd, globals, locals)
    except SyntaxError as err:
        error_class = err.__class__.__name__
        detail = err.args[0]
        if 'SyntaxError' == error_class:
            existence_flag = True
        line_number = err.lineno
    except Exception as err:
        error_class = err.__class__.__name__
        detail = err.args[0]
        if 'AttributeError' == error_class or 'ModuleNotFoundError' == error_class:
            existence_flag = True
        cl, exc, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
    else:
        return existence_flag
    return existence_flag


def pre_run_check(api_):
    code = "import tensorflow as tf\n"
    if re.findall(r'(tensorflow\.python)', api_):
        part_from = ".".join(api_.split('.')[0:-2])
        code += f"from {part_from} import {api_.split('.')[-2]}\n"
        api_ = ".".join(api_.split('.')[-2:])
        flag = my_exec(code)

    else:
        code += api_ 
        flag = my_exec(code)
    return flag
    
def run_fuzzer():
    dbname = 'TF'
    tf_output_dir = '/media/nimashiri/SSD1/testing_results'
    mydb = myclient[dbname]
    check_connection()
    TFDatabase.database_config('localhost', 27017, 'TF')

    for api_ in mydb.list_collection_names():
        # api_ = 'tensorflow.python.ops.gen_count_ops.sparse_count_sparse_output'
        if not pre_run_check(api_):
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
        else:
            print('This module does not exist in tensorflow v2.4.0!')

if __name__ == '__main__':
    run_fuzzer()