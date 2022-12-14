from tensorflow.python.client import timeline
from dill import dumps, loads
import os
import pickle
import gc, inspect, sys


from tensorflow.python.client import timeline
from tensorflow.python.client import pywrap_tf_session
from tensorflow.python.client import session
from tensorflow.python.client import device_lib
from tensorflow.python.platform import remote_utils
from tensorflow.python.platform import benchmark
from tensorflow.python.platform import app
from tensorflow.python.platform import tf_logging
from tensorflow.python.platform import flags
from tensorflow.python.platform import analytics
from tensorflow.python.platform import status_bar
from tensorflow.python.platform import test
from tensorflow.python.platform import googletest
from tensorflow.python.platform import sysconfig
from tensorflow.python.platform import gfile
from tensorflow.python.platform import device_context
from tensorflow.python.platform import resource_loader
from tensorflow.python.platform import self_check
from tensorflow.python.distribute import distribute_coordinator_context
from tensorflow.python.distribute import cross_device_utils
from tensorflow.python.distribute import multi_process_lib
from tensorflow.python.distribute import values
from tensorflow.python.distribute import reduce_util
from tensorflow.python.distribute import distribute_config
from tensorflow.python.distribute import cross_device_ops
from tensorflow.python.distribute import mirrored_strategy
from tensorflow.python.distribute import parameter_server_strategy
from tensorflow.python.distribute import strategy_test_lib
from tensorflow.python.distribute import tpu_strategy
from tensorflow.python.distribute import step_fn
from tensorflow.python.distribute import central_storage_strategy
from tensorflow.python.distribute import collective_all_reduce_strategy
from tensorflow.python.distribute import distribute_coordinator
from tensorflow.python.distribute import distribute_lib
from tensorflow.python.distribute import distributed_file_utils
from tensorflow.python.distribute import shared_variable_creator
from tensorflow.python.distribute import values_util
from tensorflow.python.distribute import summary_op_util
from tensorflow.python.distribute import estimator_training
from tensorflow.python.distribute import numpy_dataset
from tensorflow.python.distribute import distribution_strategy_context
from tensorflow.python.distribute import test_util
from tensorflow.python.distribute import parameter_server_strategy_v2
from tensorflow.python.distribute import input_lib
from tensorflow.python.distribute import device_util
from tensorflow.python.distribute import ps_values
from tensorflow.python.distribute import multi_worker_test_base
from tensorflow.python.distribute import input_ops
from tensorflow.python.distribute import one_device_strategy
from tensorflow.python.distribute import tpu_values
from tensorflow.python.distribute import collective_util
from tensorflow.python.distribute import all_reduce
from tensorflow.python.distribute import multi_worker_util
from tensorflow.python.distribute import multi_process_runner
from tensorflow.python.distribute import sharded_variable
from tensorflow.python.distribute import combinations
from tensorflow.python.distribute import mirrored_run
from tensorflow.python.distribute import single_loss_example
from tensorflow.python.distribute import packed_distributed_variable
from tensorflow.python.distribute import strategy_combinations
from tensorflow.python.distribute import distribute_utils
from tensorflow.python.saved_model import revived_types
from tensorflow.python.saved_model import main_op_impl
from tensorflow.python.saved_model import load_options
from tensorflow.python.saved_model import load
from tensorflow.python.saved_model import signature_def_utils_impl
from tensorflow.python.saved_model import save_options
from tensorflow.python.saved_model import save_context
from tensorflow.python.saved_model import function_deserialization
from tensorflow.python.saved_model import load_context
from tensorflow.python.saved_model import loader_impl
from tensorflow.python.saved_model import utils_impl
from tensorflow.python.saved_model import method_name_updater
from tensorflow.python.saved_model import nested_structure_coder
from tensorflow.python.saved_model import save
from tensorflow.python.saved_model import load_v1_in_v2
from tensorflow.python.saved_model import simple_save
from tensorflow.python.saved_model import builder_impl
from tensorflow.python.saved_model import signature_serialization
from tensorflow.python.saved_model import function_serialization
from tensorflow.python.util import tf_stack
from tensorflow.python.util import keras_deps
from tensorflow.python.util import decorator_utils
from tensorflow.python.util import all_util
from tensorflow.python.util import memory
from tensorflow.python.util import lock_util
from tensorflow.python.util import module_wrapper
from tensorflow.python.util import tf_decorator
from tensorflow.python.util import tf_inspect
from tensorflow.python.util import keyword_args
from tensorflow.python.util import compat_internal
from tensorflow.python.util import serialization
from tensorflow.python.util import tf_contextlib
from tensorflow.python.util import function_utils
from tensorflow.python.util import tf_export
from tensorflow.python.util import compat
from tensorflow.python.util import deprecation
from tensorflow.python.util import tf_should_use
from tensorflow.python.util import object_identity
from tensorflow.python.util import example_parser_configuration
from tensorflow.python.util import dispatch
from tensorflow.python.util import nest
from tensorflow.python.util import lazy_loader
from tensorflow.python.user_ops import user_ops
from tensorflow.python.framework import ops
from tensorflow.python.framework import auto_control_deps_utils
from tensorflow.python.framework import test_ops
from tensorflow.python.framework import auto_control_deps
from tensorflow.python.framework import op_callbacks
from tensorflow.python.framework import graph_io
from tensorflow.python.framework import tfrt_utils
from tensorflow.python.framework import op_def_library
from tensorflow.python.framework import random_seed
from tensorflow.python.framework import function_def_to_graph
from tensorflow.python.framework import graph_to_function_def
from tensorflow.python.framework import importer
from tensorflow.python.framework import tensor_spec
from tensorflow.python.framework import composite_tensor_utils
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import errors_impl
from tensorflow.python.framework import indexed_slices
from tensorflow.python.framework import composite_tensor
from tensorflow.python.framework import device
from tensorflow.python.framework import common_shapes
from tensorflow.python.framework import load_library
from tensorflow.python.framework import registry
from tensorflow.python.framework import config
from tensorflow.python.framework import tensor_shape
from tensorflow.python.framework import error_interpolation
from tensorflow.python.framework import subscribe
from tensorflow.python.framework import test_util
from tensorflow.python.framework import python_memory_checker
from tensorflow.python.framework import sparse_tensor
from tensorflow.python.framework import c_api_util
from tensorflow.python.framework import gpu_util
from tensorflow.python.framework import op_def_registry
from tensorflow.python.framework import test_combinations
from tensorflow.python.framework import smart_cond
from tensorflow.python.framework import tensor_util
from tensorflow.python.framework import func_graph
from tensorflow.python.framework import type_spec
from tensorflow.python.framework import function
from tensorflow.python.framework import constant_op
from tensorflow.python.framework import graph_util_impl
from tensorflow.python.framework import convert_to_constants
from tensorflow.python.framework import combinations
from tensorflow.python.framework import tensor_conversion_registry
from tensorflow.python.framework import device_spec
from tensorflow.python.framework import traceable_stack
from tensorflow.python.framework import memory_checker
from tensorflow.python.framework import meta_graph
from tensorflow.python.framework import kernels
from tensorflow.python.feature_column import serialization
from tensorflow.python.feature_column import utils
from tensorflow.python.feature_column import feature_column
from tensorflow.python.feature_column import sequence_feature_column
from tensorflow.python.feature_column import feature_column_v2
from tensorflow.python.keras import testing_utils
from tensorflow.python.keras import optimizers
from tensorflow.python.keras import optimizer_v1
from tensorflow.python.keras import callbacks_v1
from tensorflow.python.keras import models
from tensorflow.python.keras import keras_parameterized



with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/import_objects/timeline', 'wb') as outp:  # Overwrites any existing file.
    dumps(timeline)

if os.path.getsize('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/import_objects/timeline') > 0:          
    with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/import_objects/timeline', 'r') as file:
        data = pickle.load(StrToBytes(file))
    print(data)