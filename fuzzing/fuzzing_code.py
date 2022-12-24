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

def make_api_name_unique(api):
    api_split = api.split('tensorflow')
    new_api_name = 'tensorflow'+api_split[-1]
    return new_api_name    

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

if __name__ == '__main__':
    library = sys.argv[1]
    api_name = sys.argv[2]
    TFDatabase.database_config('localhost', 27017, library)
    rules = [
        'NEGATE_INT_TENSOR', 
        'RANK_REDUCTION_EXPANSION', 
        'EMPTY_TENSOR_TYPE1', 
        'EMPTY_TENSOR_TYPE2', 
        'EMPTY_LIST', 
        'LARGE_TENSOR_TYPE1', 
        'LARGE_TENSOR_TYPE2',
        'LARGE_LIST_ELEMENT',
        'ZERO_TENSOR_TYPE1',
        'ZERO_TENSOR_TYPE2',
        'NAN_TENSOR'
        ]

    tf_output_dir = '/media/nimashiri/SSD1/testing_results'
    MyTF = TFLibrary(tf_output_dir)

        # api_ = 'tf.transpose'
        # api_ = 'tensorflow.python.ops.nn_ops.max_pool'
        #api_ = 'tensorflow.python.ops.nn_ops.in_top_k'
        # api_ = 'tensorflow.python.ops.linalg.linear_operator_algebra.tensorflow.python.ops.linalg.linear_operator_algebra.RegisterCholesky'

    try:
        api = TFAPI(api_name)
        api_keywords = api_name.split('.')
        if api_keywords.count('tensorflow') > 1:
            api_name = make_api_name_unique(api_name)
        num_tensors = count_tensor_inputs(api)
        api.args.pop('source')
        if '_id' in api.args:
            api.args.pop('_id')

        for i, arg in enumerate(api.args):       
            for r in rules:
                print("The current API under test: ###{0}###. Mutating the parameter ###{1}### using the rule ###{2}###".format(api_name, arg, r))
                old_arg = copy.deepcopy(api.args[arg])
                api.new_mutate_multiple(api.args[arg], r)
                MyTF.test_with_oracle(api, OracleType.CRASH)
                api.api = sys.argv[2]
                MyTF.test_with_oracle(api, OracleType.CUDA)
                # api.api = sys.argv[2]
                # MyTF.test_with_oracle(api, OracleType.PRECISION)
                api.api = sys.argv[2]
                api.args[arg] = old_arg
    except Exception as e:
        pass

