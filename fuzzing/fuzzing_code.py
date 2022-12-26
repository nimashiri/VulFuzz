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

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

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
    # buggy_api = '/media/nimashiri/SSD1/testing_results/runcrash.txt'
    # data = read_txt(buggy_api)
    TFDatabase.database_config('localhost', 27017, 'TF')

    dimension_mismatch = True

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
    'NAN_TENSOR',
    'NAN_TENSOR_WHOLE',
    'NON_SCALAR_INPUT',
    'SCALAR_INPUT'
    ]

    tf_output_dir = '/media/nimashiri/SSD1/testing_results'
    MyTF = TFLibrary(tf_output_dir)

    try:
        #for api_name in data:
            # api_name = 'tensorflow.python.ops.gen_count_ops.sparse_count_sparse_output'
            
            api = TFAPI(api_name)
            old_api = copy.deepcopy(api)
            _count_tensor = count_tensor_inputs(api)
            if  len(_count_tensor) > 1:
                print("########################################################################################################################")
                print("The current API under test: ###{0}###. Working on dimension mismatch".format(api_name))
                print("########################################################################################################################")
                api_keywords = api_name.split('.')
                if api_keywords.count('tensorflow') > 1:
                    api_name = make_api_name_unique(api_name)
                api.args.pop('source')
                if '_id' in api.args:
                    api.args.pop('_id')

                api.new_mutate()
                MyTF.test_with_oracle(api, OracleType.CRASH)
                api.api = api_name
                MyTF.test_with_oracle(api, OracleType.CUDA)


            api_keywords = api_name.split('.')
            if api_keywords.count('tensorflow') > 1:
                api_name = make_api_name_unique(api_name)
            old_api.args.pop('source')
            if '_id' in old_api.args:
                old_api.args.pop('_id')
            for i, arg in enumerate(old_api.args):       
                for r in rules:
                    print("########################################################################################################################")
                    print("The current API under test: ###{0}###. Mutating the parameter ###{1}### using the rule ###{2}###".format(api_name, arg, r))
                    print("########################################################################################################################")
                    old_arg = copy.deepcopy(old_api.args[arg])
                    old_api.new_mutate_multiple(old_api.args[arg], r)
                    MyTF.test_with_oracle(old_api, OracleType.CRASH)
                    old_api.api = api_name
                    MyTF.test_with_oracle(old_api, OracleType.CUDA)
                    # api.api = sys.argv[2]
                    # MyTF.test_with_oracle(api, OracleType.PRECISION)
                    old_api.api = api_name
                    old_api.args[arg] = old_arg
    except Exception as e:
        pass

# tensorflow.python.ops.gen_nn_ops.fused_batch_norm_grad_v3
# tensorflow.python.ops.gen_array_ops.quantize_v2
# tensorflow.python.ops.gen_nn_ops.fused_batch_norm_v3
# tensorflow.python.ops.gen_linalg_ops.cholesky
# tensorflow.python.ops.gen_image_ops.extract_glimpse_v2
# tensorflow.python.ops.collective_ops.all_gather
# tensorflow.python.ops.gen_array_ops.pad_v2
# tensorflow.python.ops.linalg.linalg_impl.matrix_exponential
# tensorflow.python.ops.ragged.ragged_string_ops.ngrams
# tensorflow.python.ops.gen_collective_ops.collective_gather
# tensorflow.python.ops.gen_nn_ops.fractional_max_pool_grad
# tensorflow.python.ops.gen_array_ops.upper_bound
# tensorflow.python.ops.gen_bitwise_ops.population_count
# tf.test.create_local_cluster
# tensorflow.python.ops.gen_data_flow_ops.record_input
# tensorflow.python.ops.nn_impl.fused_batch_norm
# tensorflow.python.ops.random_grad.add_leading_unit_dimensions