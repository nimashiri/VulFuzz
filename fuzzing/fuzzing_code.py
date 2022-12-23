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
import re
import copy

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


def count_tensor_inputs(api, lib='Tensorflow'):
    tensor_holder = []
    for arg in api.args:
        _arg = api.args[arg]
        
        if lib == 'Tensorflow':
            if re.findall(r'(ArgType\.TF\_TENSOR\:)', repr(_arg.type)):
                tensor_holder.append(1)
        else:
            if re.findall('r(ArgType\.TORCH\_TENSOR\:)', repr(_arg.type)):
                tensor_holder.append(1)
    return tensor_holder

def fuzzing():
    dbname = 'TF'
    mydb = myclient[dbname]
    check_connection()
    TFDatabase.database_config('localhost', 27017, 'TF')
    enable_value = True
    enable_type = True
    enable_db = False

    # 'EMPTY_LIST','EMPTY_TENSOR_TYPE2','EMPTY_TENSOR_TYPE1','NEGATIVE', 'RANK_REDUCTION_EXPANSION', 'LARGE_TENSOR_TYPE1', 'LARGE_TENSOR_TYPE2'
    rules = ['LARGE_TENSOR_TYPE2']

    tf_output_dir = '/media/nimashiri/SSD1/FSE23_2/fuzzing'
    MyTF = TFLibrary(tf_output_dir)

    for api_ in mydb.list_collection_names():
        # api_ = 'tensorflow.python.ops.array_grad._BatchGatherGrad'
        # api_ = 'tf.transpose'
        api_ = 'tensorflow.python.ops.nn_ops.max_pool'
       
        api = TFAPI(api_)
        api.args.pop('source')
        api.args.pop('_id')
        num_tensors = count_tensor_inputs(api)
        if len(num_tensors) > 1:
            api.new_mutate()
        else:
            for i, arg in enumerate(api.args):
                for r in rules:
                    old_arg = copy.deepcopy(api.args[arg])
                    api.new_mutate_multiple(api.args[arg], r)
                    MyTF.test_with_oracle(api, OracleType.CRASH)
                    api.api = api_
                    api.args[arg] = old_arg

    

if __name__ == '__main__':
    fuzzing()