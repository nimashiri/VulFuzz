# import os
# from csv import writer
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import tensorflow as tf
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# import inspect
# from tensorflow.instrumentation.decorators import dump_signature_of_class, dump_signature_of_function

# def hijack(output_dir="/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf"):
#     hijack_all(output_dir)


# def hijack_api(obj, func_name_str, output_dir):
#     """
#     Function to hijack an API.
#     Args:
#         obj: the base module. This function is currently specific to TensorFlow.
#             So obj should be tensorflow.
#         func_name_str: A string. The full name of the api (except 'tf.'). For example, the name of
#             `tf.keras.losses.MeanSquaredError` should be 'keras.losses.MeanSquaredError'.
#     Returns:
#         A boolean, indicating if hijacking is successful.
#     The targeted API can be either a function or a class (the type will be detected by this function).
#     This function would replace the original api with the new decorated api we created. This is achieved
#     in a fairly simple and straight-forward way. For the example above, we just set the attribute by calling
#     `setattr(tf.keras.losses, 'MeanSquaredError', wrapped_func)`.
#     """
#     func_name_list = func_name_str.split('.')
    
#     func_name = func_name_list[-1]
    
    
    
#     # Get the module object and the api object.
#     module_obj = obj
#     if len(func_name_list) > 1:
#         for module_name in func_name_list[:-1]:
#             module_obj = getattr(module_obj, module_name)
#     orig_func = getattr(module_obj, func_name)

#     # Utilities.
#     def is_class(x):
#         return inspect.isclass(x)
#     def is_callable(x):
#         return callable(x)
#     def is_built_in_or_extension_type(x):
#         if is_class(x) and hasattr(x, '__dict__') and not '__module__' in x.__dict__:
#             return True
#         else:
#             return False
#     # Handle special cases of types.
#     if is_built_in_or_extension_type(orig_func):
#       return False
#     if is_class(orig_func):
#         if hasattr(orig_func, '__slots__'):
#             # with open('/media/nimashiri/DATA/vsprojects/FSE23_2/slot_apis.csv', 'a', newline='\n') as fd:
#             #     writer_object = writer(fd)
#             #     writer_object.writerow([orig_func])
#             return False
#         # with open('/media/nimashiri/DATA/vsprojects/FSE23_2/allowed_apis.csv', 'a', newline='\n') as fd:
#         #     writer_object = writer(fd)
#         #     writer_object.writerow([orig_func])
#         wrapped_func = dump_signature_of_class(orig_func, func_name_str, output_dir=output_dir)
#         setattr(module_obj, func_name, wrapped_func)
#         return True 
#     else:
#       if is_callable(orig_func):
#         wrapped_func = dump_signature_of_function(orig_func, func_name_str, output_dir=output_dir)
#         setattr(module_obj, func_name, wrapped_func)
#         return True
#       else:
#         return False

# def should_skip(api):

#     skip_list = [
#         'tf.keras.layers.Layer',
#         'tf.compat.v1.keras.layers.Layer',
#         'tf.Module',
#         'tf.compat.v1.Module',
#         'tf.compat.v1.flags.FLAGS',
#         'tf.compat.v1.app.flags.EnumClassListSerializer',
#         'tf.compat.v1.app.flags.EnumClassSerializer',
#         'tf.compat.v1.flags.EnumClassListSerializer',
#         'tf.compat.v1.flags.EnumClassSerializer',
#         'tf.init_scope',
#         'tf.TensorShape',
#         'tf.compat.v1.Variable',
#         'tf.ResourceVariable',
#         'tf.Tensor',
#         'tf.compat.v1.Tensor',
#         'tf.compat.v1.flags.tf_decorator.make_decorator',
#         'tf.compat.v1.flags.tf_decorator.tf_stack.extract_stack',
#         'tf.compat.v1.flags.tf_decorator.unwrap',
#         'tf.compat.v1.flags.tf_decorator.rewrap',
#         'tf.compat.v1.app.flags.tf_decorator.make_decorator',
#         'tf.compat.v1.app.flags.tf_decorator.rewrap',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack.CurrentModuleFilter',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack.FrameSummary',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackSummary',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackTraceFilter',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackTraceMapper',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackTraceTransform',
#         'tf.compat.v1.app.flags.tf_decorator.tf_stack.extract_stack',
#         'tf.compat.v1.app.flags.tf_decorator.unwrap',

#     ]
#     skip_key_word = [
#         'tf.debugging',
#         'tf.distribute',
#         'tf.errors',
#         'tf.profiler',
#         'tf.test',
#         'tf.tpu',
#         'tf.summary',
#         'tpu',
#         'TPU',
#         # 'tf.quantization', 
#         # 'tf.experimental.numpy',

#     ]
    
#     if api.find('tf.') != 0:
#         return True
#     # Skip the current api if it's in the skip list.
#     if api in skip_list:
#         return True
#     # Skip the current api if it has some keywords.
#     for kw in skip_key_word:
#         if kw in api:
#             return True
            
# def hijack_all(output_dir, verbose=False):
#     import os
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     success_list = []
#     failed_list = []
#     skip_list = []
#     import os
#     api_file = __file__.replace("hijack.py", "tf_valid_APIs_new.txt")
#     with open(api_file, 'r') as fr:
#         apis = fr.readlines()
#     # print('Number of total apis: ', len(apis)) 
#     skip_apis = False
#     cnt = 0
#     for i, api in enumerate(apis):
#         api = api.strip()
#         if skip_apis:
#             if should_skip(api):
#                 skip_list.append(api + "\n")
#                 continue
#         try:
#             hijack_api(tf, api[3:], output_dir)
#         except:
#             continue


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import array_grad

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
from tensorflow.python.keras import activations
from tensorflow.python.keras import losses
from tensorflow.python.keras import regularizers
from tensorflow.python.keras import combinations
from tensorflow.python.keras import constraints
from tensorflow.python.keras import metrics
from tensorflow.python.keras import backend_config
from tensorflow.python.keras import backend
from tensorflow.python.keras import callbacks
from tensorflow.python.ops import manip_grad
from tensorflow.python.ops import variables
from tensorflow.python.ops import functional_ops
from tensorflow.python.ops import gen_set_ops
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import gen_script_ops
from tensorflow.python.ops import gen_batch_ops
from tensorflow.python.ops import custom_gradient
from tensorflow.python.ops import linalg_grad
from tensorflow.python.ops import clip_ops
from tensorflow.python.ops import gen_ctc_ops
from tensorflow.python.ops import gen_image_ops
from tensorflow.python.ops import cond_v2
from tensorflow.python.ops import histogram_ops
from tensorflow.python.ops import gen_spectral_ops
from tensorflow.python.ops import gen_sdca_ops
from tensorflow.python.ops import gen_tensor_forest_ops
from tensorflow.python.ops import gen_ragged_math_ops
from tensorflow.python.ops import gen_candidate_sampling_ops
from tensorflow.python.ops import gen_boosted_trees_ops
from tensorflow.python.ops import manip_ops
from tensorflow.python.ops import unconnected_gradients
from tensorflow.python.ops import nn_impl
from tensorflow.python.ops import parsing_ops
from tensorflow.python.ops import gen_checkpoint_ops
from tensorflow.python.ops import variable_scope
from tensorflow.python.ops import io_ops
from tensorflow.python.ops import embedding_ops
from tensorflow.python.ops import weights_broadcast_ops
from tensorflow.python.ops import while_v2_indexed_slices_rewriter
from tensorflow.python.ops import map_fn
from tensorflow.python.ops import gen_sparse_ops
from tensorflow.python.ops import numerics
from tensorflow.python.ops import gen_ragged_conversion_ops
from tensorflow.python.ops import tensor_array_ops
from tensorflow.python.ops import gen_encode_proto_ops
from tensorflow.python.ops import array_grad
from tensorflow.python.ops import gradients_util
from tensorflow.python.ops import math_grad
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import session_ops
from tensorflow.python.ops import gen_stateless_random_ops_v2
from tensorflow.python.ops import gen_io_ops
from tensorflow.python.ops import list_ops
from tensorflow.python.ops import batch_ops
from tensorflow.python.ops import optional_grad
from tensorflow.python.ops import linalg_ops_impl
from tensorflow.python.ops import gen_array_ops
from tensorflow.python.ops import gen_linalg_ops
from tensorflow.python.ops import lookup_ops
from tensorflow.python.ops import map_ops
from tensorflow.python.ops import gen_debug_ops
from tensorflow.python.ops import gen_nccl_ops
from tensorflow.python.ops import gen_training_ops
from tensorflow.python.ops import data_flow_grad
from tensorflow.python.ops import random_ops
from tensorflow.python.ops import gen_random_ops
from tensorflow.python.ops import sparse_ops
from tensorflow.python.ops import gen_special_math_ops
from tensorflow.python.ops import string_ops
from tensorflow.python.ops import gen_string_ops
from tensorflow.python.ops import summary_op_util
from tensorflow.python.ops import op_selector
from tensorflow.python.ops import gen_user_ops
from tensorflow.python.ops import gen_dataset_ops
from tensorflow.python.ops import control_flow_util
from tensorflow.python.ops import init_ops_v2
from tensorflow.python.ops import boosted_trees_ops
from tensorflow.python.ops import image_ops
from tensorflow.python.ops import nn_ops
from tensorflow.python.ops import gen_manip_ops
from tensorflow.python.ops import bincount_ops
from tensorflow.python.ops import collective_ops
from tensorflow.python.ops import gen_parsing_ops
from tensorflow.python.ops import rnn
from tensorflow.python.ops import sparse_grad
from tensorflow.python.ops import gradients_impl
from tensorflow.python.ops import gen_data_flow_ops
from tensorflow.python.ops import resources
from tensorflow.python.ops import nn_grad
from tensorflow.python.ops import gen_collective_ops
from tensorflow.python.ops import control_flow_v2_func_graphs
from tensorflow.python.ops import gen_nn_ops
from tensorflow.python.ops import metrics_impl
from tensorflow.python.ops import sets_impl
from tensorflow.python.ops import cudnn_rnn_grad
from tensorflow.python.ops import gen_state_ops
from tensorflow.python.ops import tensor_array_grad
from tensorflow.python.ops import image_ops_impl
from tensorflow.python.ops import partitioned_variables
from tensorflow.python.ops import gradient_checker_v2
from tensorflow.python.ops import nccl_ops
from tensorflow.python.ops import check_ops
from tensorflow.python.ops import gen_math_ops
from tensorflow.python.ops import critical_section_ops
from tensorflow.python.ops import gen_summary_ops
from tensorflow.python.ops import control_flow_util_v2
from tensorflow.python.ops import stateful_random_ops
from tensorflow.python.ops import sort_ops
from tensorflow.python.ops import parsing_config
from tensorflow.python.ops import gen_decode_proto_ops
from tensorflow.python.ops import control_flow_v2_toggles
from tensorflow.python.ops import data_flow_ops
from tensorflow.python.ops import gen_rnn_ops
from tensorflow.python.ops import gen_sendrecv_ops
from tensorflow.python.ops import gen_cudnn_rnn_ops
from tensorflow.python.ops import gen_stateless_random_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import inplace_ops
from tensorflow.python.ops import linalg_ops
from tensorflow.python.ops import gradient_checker
from tensorflow.python.ops import gen_bitwise_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import special_math_ops
from tensorflow.python.ops import logging_ops
from tensorflow.python.ops import image_grad
from tensorflow.python.ops import ctc_ops
from tensorflow.python.ops import image_grad_test_base
from tensorflow.python.ops import gen_stateful_random_ops
from tensorflow.python.ops import random_grad
from tensorflow.python.ops import gen_tpu_ops
from tensorflow.python.ops import gen_resource_variable_ops
from tensorflow.python.ops import confusion_matrix
from tensorflow.python.ops import gen_functional_ops
from tensorflow.python.ops import handle_data_util
from tensorflow.python.ops import tensor_forest_ops
from tensorflow.python.ops import gen_experimental_dataset_ops
from tensorflow.python.ops import script_ops
from tensorflow.python.ops import rnn_grad
from tensorflow.python.ops import while_v2
from tensorflow.python.ops import gen_logging_ops
from tensorflow.python.ops import summary_ops_v2
from tensorflow.python.ops import gen_ragged_array_ops
from tensorflow.python.ops import gen_map_ops
from tensorflow.python.ops import control_flow_grad
from tensorflow.python.ops import gen_audio_ops
from tensorflow.python.ops import stateless_random_ops
from tensorflow.python.ops import gen_lookup_ops
from tensorflow.python.ops import gen_clustering_ops
from tensorflow.python.ops import gen_count_ops
from tensorflow.python.ops import gen_control_flow_ops
from tensorflow.python.ops import candidate_sampling_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.ops import template
from tensorflow.python.ops import default_gradient
from tensorflow.python.ops import clustering_ops
from tensorflow.python.ops import resource_variable_ops
from tensorflow.python.ops import control_flow_state
from tensorflow.python.ops import gen_list_ops
from tensorflow.python.training import gradient_descent
from tensorflow.python.training import proximal_gradient_descent
from tensorflow.python.training import sync_replicas_optimizer
from tensorflow.python.training import adagrad
from tensorflow.python.training import coordinator
from tensorflow.python.training import checkpoint_ops
from tensorflow.python.training import session_manager
from tensorflow.python.training import ftrl
from tensorflow.python.training import session_run_hook
from tensorflow.python.training import saver
from tensorflow.python.training import device_setter
from tensorflow.python.training import server_lib
from tensorflow.python.training import training_util
from tensorflow.python.training import checkpoint_utils
from tensorflow.python.training import adagrad_da
from tensorflow.python.training import momentum
from tensorflow.python.training import monitored_session
from tensorflow.python.training import adadelta
from tensorflow.python.training import optimizer
from tensorflow.python.training import saver_test_utils
from tensorflow.python.training import moving_averages
from tensorflow.python.training import basic_session_run_hooks
from tensorflow.python.training import rmsprop
from tensorflow.python.training import py_checkpoint_reader
from tensorflow.python.training import slot_creator
from tensorflow.python.training import checkpoint_management
from tensorflow.python.training import quantize_training
from tensorflow.python.training import adam
from tensorflow.python.training import tensorboard_logging
from tensorflow.python.training import warm_starting_util
from tensorflow.python.training import summary_io
from tensorflow.python.training import supervisor
from tensorflow.python.training import basic_loops
from tensorflow.python.training import queue_runner_impl
from tensorflow.python.training import evaluation
from tensorflow.python.training import input
from tensorflow.python.training import proximal_adagrad
from tensorflow.python.eager import executor
from tensorflow.python.eager import wrap_function
from tensorflow.python.eager import backprop_util
from tensorflow.python.eager import graph_only_ops
from tensorflow.python.eager import imperative_grad
from tensorflow.python.eager import profiler_client
from tensorflow.python.eager import forwardprop_util
from tensorflow.python.eager import profiler
from tensorflow.python.eager import def_function
from tensorflow.python.eager import core
from tensorflow.python.eager import test
from tensorflow.python.eager import forwardprop
from tensorflow.python.eager import monitoring
from tensorflow.python.eager import cancellation
from tensorflow.python.eager import remote
from tensorflow.python.eager import execute
from tensorflow.python.eager import function
from tensorflow.python.eager import tape
from tensorflow.python.eager import lift_to_graph
from tensorflow.python.eager import backprop
from tensorflow.python.eager import benchmarks_test_base
from tensorflow.python.eager import context
from tensorflow.python.module import module
from tensorflow.python.summary import summary
from tensorflow.python.summary import plugin_asset
from tensorflow.python.summary import summary_iterator
from tensorflow.python.layers import utils
from tensorflow.python.grappler import item
from tensorflow.python.grappler import cluster
from tensorflow.python.grappler import tf_optimizer
from tensorflow.python.types import internal
from tensorflow.python.types import distribute
from tensorflow.python.types import core
from tensorflow.python.types import doc_typealias
from tensorflow.python.profiler.internal import flops_registry
from tensorflow.python.compiler.mlir import mlir
from tensorflow.python.compiler.xla import jit
from tensorflow.python.compiler.xla import xla
from tensorflow.python.compiler.tensorrt import trt_convert
from tensorflow.python.compiler.tensorrt.test import tf_trt_integration_test_base
from tensorflow.python.tpu.client import client
from tensorflow.python.tpu.ops import tpu_ops
from tensorflow.python.distribute.coordinator import metric_utils
from tensorflow.python.distribute.coordinator import utils
from tensorflow.python.distribute.coordinator import cluster_coordinator
from tensorflow.python.distribute.cluster_resolver import slurm_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import sagemaker_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import kubernetes_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import gce_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import tfconfig_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import cluster_resolver
from tensorflow.python.distribute.parallel_device import parallel_device
from tensorflow.python.distribute.parallel_device import saving
from tensorflow.python.saved_model.model_utils import export_output
from tensorflow.python.saved_model.model_utils import mode_keys
from tensorflow.python.saved_model.model_utils import export_utils
from tensorflow.python.util.protobuf import compare
from tensorflow.python.data.util import structure
from tensorflow.python.data.util import random_seed
from tensorflow.python.data.util import traverse
from tensorflow.python.data.util import sparse
from tensorflow.python.data.util import options
from tensorflow.python.data.util import nest
from tensorflow.python.data.util import convert
from tensorflow.python.data.ops import iterator_ops
from tensorflow.python.data.ops import optional_ops
from tensorflow.python.data.ops import multi_device_iterator_ops
from tensorflow.python.data.ops import readers
from tensorflow.python.data.ops import dataset_ops
from tensorflow.python.data.benchmarks import benchmark_base
from tensorflow.python.data.experimental.service import server_lib
from tensorflow.python.data.experimental.ops import iterator_ops
from tensorflow.python.data.experimental.ops import optimization
from tensorflow.python.data.experimental.ops import testing
from tensorflow.python.data.experimental.ops import stats_ops
from tensorflow.python.data.experimental.ops import scan_ops
from tensorflow.python.data.experimental.ops import compression_ops
from tensorflow.python.data.experimental.ops import optimization_options
from tensorflow.python.data.experimental.ops import unique
from tensorflow.python.data.experimental.ops import parsing_ops
from tensorflow.python.data.experimental.ops import distribute
from tensorflow.python.data.experimental.ops import get_single_element
from tensorflow.python.data.experimental.ops import stats_aggregator
from tensorflow.python.data.experimental.ops import take_while_ops
from tensorflow.python.data.experimental.ops import counter
from tensorflow.python.data.experimental.ops import threadpool
from tensorflow.python.data.experimental.ops import snapshot
from tensorflow.python.data.experimental.ops import cardinality
from tensorflow.python.data.experimental.ops import random_ops
from tensorflow.python.data.experimental.ops import error_ops
from tensorflow.python.data.experimental.ops import prefetching_ops
from tensorflow.python.data.experimental.ops import enumerate_ops
from tensorflow.python.data.experimental.ops import map_defun
from tensorflow.python.data.experimental.ops import shuffle_ops
from tensorflow.python.data.experimental.ops import stats_options
from tensorflow.python.data.experimental.ops import threading_options
from tensorflow.python.data.experimental.ops import grouping
from tensorflow.python.data.experimental.ops import interleave_ops
from tensorflow.python.data.experimental.ops import matching_files
from tensorflow.python.data.experimental.ops import distribute_options
from tensorflow.python.data.experimental.ops import io
from tensorflow.python.data.experimental.ops import resampling
from tensorflow.python.data.experimental.ops import writers
from tensorflow.python.data.experimental.ops import batching
from tensorflow.python.data.experimental.ops import data_service_ops
from tensorflow.python.data.experimental.ops import readers
from tensorflow.python.data.experimental.kernel_tests.serialization import dataset_serialization_test_base
from tensorflow.python.debug.examples import debug_mnist
from tensorflow.python.debug.cli import profile_analyzer_cli
from tensorflow.python.debug.cli import base_ui
from tensorflow.python.debug.cli import debugger_cli_common
from tensorflow.python.debug.cli import cli_test_utils
from tensorflow.python.debug.cli import analyzer_cli
from tensorflow.python.debug.cli import command_parser
from tensorflow.python.debug.cli import cli_config
from tensorflow.python.debug.cli import curses_widgets
from tensorflow.python.debug.cli import cli_shared
from tensorflow.python.debug.cli import evaluator
from tensorflow.python.debug.cli import tensor_format
from tensorflow.python.debug.cli import ui_factory
from tensorflow.python.debug.cli import curses_ui
from tensorflow.python.debug.cli import readline_ui
from tensorflow.python.debug.cli import offline_analyzer
from tensorflow.python.debug.wrappers import framework
from tensorflow.python.debug.wrappers import grpc_wrapper
from tensorflow.python.debug.wrappers import local_cli_wrapper
from tensorflow.python.debug.wrappers import hooks
from tensorflow.python.debug.wrappers import dumping_wrapper
from tensorflow.python.debug.examples.v1 import debug_keras
from tensorflow.python.debug.examples.v1 import debug_mnist_v1
from tensorflow.python.debug.examples.v1 import debug_fibonacci
from tensorflow.python.debug.examples.v1 import debug_errors
from tensorflow.python.debug.examples.v2 import debug_mnist_v2
from tensorflow.python.debug.examples.v2 import debug_fibonacci_v2
from tensorflow.python.keras.engine import compile_utils
from tensorflow.python.keras.engine import input_layer
from tensorflow.python.keras.engine import training_utils_v1
from tensorflow.python.keras.engine import training_eager_v1
from tensorflow.python.keras.engine import partial_batch_padding_handler
from tensorflow.python.keras.engine import base_layer_v1
from tensorflow.python.keras.engine import base_preprocessing_layer
from tensorflow.python.keras.engine import base_layer_utils
from tensorflow.python.keras.engine import functional
from tensorflow.python.keras.engine import training_v1
from tensorflow.python.keras.engine import training_utils
from tensorflow.python.keras.engine import sequential
from tensorflow.python.keras.engine import base_layer
from tensorflow.python.keras.engine import training_generator_v1
from tensorflow.python.keras.engine import training_arrays_v1
from tensorflow.python.keras.engine import training
from tensorflow.python.keras.engine import keras_tensor
from tensorflow.python.keras.engine import input_spec
from tensorflow.python.keras.engine import data_adapter
from tensorflow.python.keras.engine import base_preprocessing_layer_v1
from tensorflow.python.keras.engine import training_distributed_v1
from tensorflow.python.keras.engine import node
from tensorflow.python.keras.preprocessing import text_dataset
from tensorflow.python.keras.preprocessing import dataset_utils
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.preprocessing import sequence
from tensorflow.python.keras.preprocessing import timeseries
from tensorflow.python.keras.preprocessing import text
from tensorflow.python.keras.preprocessing import image_dataset
from tensorflow.python.keras.distribute import keras_image_model_correctness_test
from tensorflow.python.keras.distribute import keras_utils_test
from tensorflow.python.keras.distribute import keras_stateful_lstm_model_correctness_test
from tensorflow.python.keras.distribute import keras_embedding_model_correctness_test
from tensorflow.python.keras.distribute import distributed_training_utils_v1
from tensorflow.python.keras.distribute import keras_correctness_test_base
from tensorflow.python.keras.distribute import keras_rnn_model_correctness_test
from tensorflow.python.keras.distribute import distribute_strategy_test
from tensorflow.python.keras.distribute import distributed_training_utils
from tensorflow.python.keras.distribute import saved_model_test_base
from tensorflow.python.keras.distribute import worker_training_state
from tensorflow.python.keras.distribute import simple_models
from tensorflow.python.keras.distribute import optimizer_combinations
from tensorflow.python.keras.distribute import keras_dnn_correctness_test
from tensorflow.python.keras.distribute import multi_worker_testing_utils
from tensorflow.python.keras.distribute import model_collection_base
from tensorflow.python.keras.tests import model_subclassing_test_util
from tensorflow.python.keras.tests import model_architectures
from tensorflow.python.keras.initializers import initializers_v1
from tensorflow.python.keras.initializers import initializers_v2
from tensorflow.python.keras.legacy_tf_layers import base
from tensorflow.python.keras.legacy_tf_layers import convolutional
from tensorflow.python.keras.legacy_tf_layers import core
from tensorflow.python.keras.legacy_tf_layers import pooling
from tensorflow.python.keras.legacy_tf_layers import normalization
from tensorflow.python.keras.datasets import fashion_mnist
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras.datasets import cifar
from tensorflow.python.keras.datasets import imdb
from tensorflow.python.keras.datasets import cifar10
from tensorflow.python.keras.datasets import boston_housing
from tensorflow.python.keras.datasets import cifar100
from tensorflow.python.keras.datasets import reuters
from tensorflow.python.keras.utils import tf_utils
from tensorflow.python.keras.utils import conv_utils
from tensorflow.python.keras.utils import tf_inspect
from tensorflow.python.keras.utils import metrics_utils
from tensorflow.python.keras.utils import tf_contextlib
from tensorflow.python.keras.utils import data_utils
from tensorflow.python.keras.utils import control_flow_util
from tensorflow.python.keras.utils import vis_utils
from tensorflow.python.keras.utils import version_utils
from tensorflow.python.keras.utils import losses_utils
from tensorflow.python.keras.utils import generic_utils
from tensorflow.python.keras.utils import multi_gpu_utils
from tensorflow.python.keras.utils import kernelized_utils
from tensorflow.python.keras.utils import layer_utils
from tensorflow.python.keras.utils import io_utils
from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras.feature_column import base_feature_layer
from tensorflow.python.keras.feature_column import dense_features_v2
from tensorflow.python.keras.feature_column import sequence_feature_column
from tensorflow.python.keras.feature_column import dense_features
from tensorflow.python.keras.wrappers import scikit_learn
from tensorflow.python.keras.premade import wide_deep
from tensorflow.python.keras.premade import linear
from tensorflow.python.keras.benchmarks import distribution_util
from tensorflow.python.keras.benchmarks import benchmark_util
from tensorflow.python.keras.saving import saving_utils
from tensorflow.python.keras.saving import saved_model_experimental
from tensorflow.python.keras.saving import model_config
from tensorflow.python.keras.saving import hdf5_format
from tensorflow.python.keras.saving import save
from tensorflow.python.keras.applications import densenet
from tensorflow.python.keras.applications import mobilenet
from tensorflow.python.keras.applications import xception
from tensorflow.python.keras.applications import vgg16
from tensorflow.python.keras.applications import mobilenet_v3
from tensorflow.python.keras.applications import vgg19
from tensorflow.python.keras.applications import resnet
from tensorflow.python.keras.applications import imagenet_utils
from tensorflow.python.keras.applications import efficientnet
from tensorflow.python.keras.applications import nasnet
from tensorflow.python.keras.applications import mobilenet_v2
from tensorflow.python.keras.applications import inception_v3
from tensorflow.python.keras.applications import inception_resnet_v2
from tensorflow.python.keras.applications import resnet_v2
from tensorflow.python.keras.layers import einsum_dense
from tensorflow.python.keras.layers import kernelized
from tensorflow.python.keras.layers import multi_head_attention
from tensorflow.python.keras.layers import wrappers
from tensorflow.python.keras.layers import rnn_cell_wrapper_v2
from tensorflow.python.keras.layers import recurrent_v2
from tensorflow.python.keras.layers import convolutional
from tensorflow.python.keras.layers import serialization
from tensorflow.python.keras.layers import normalization_v2
from tensorflow.python.keras.layers import merge
from tensorflow.python.keras.layers import local
from tensorflow.python.keras.layers import core
from tensorflow.python.keras.layers import dense_attention
from tensorflow.python.keras.layers import noise
from tensorflow.python.keras.layers import recurrent
from tensorflow.python.keras.layers import advanced_activations
from tensorflow.python.keras.layers import pooling
from tensorflow.python.keras.layers import embeddings
from tensorflow.python.keras.layers import cudnn_recurrent
from tensorflow.python.keras.layers import normalization
from tensorflow.python.keras.layers import convolutional_recurrent
from tensorflow.python.keras.mixed_precision import autocast_variable
from tensorflow.python.keras.mixed_precision import loss_scale
from tensorflow.python.keras.mixed_precision import get_layer_policy
from tensorflow.python.keras.mixed_precision import loss_scale_optimizer
from tensorflow.python.keras.mixed_precision import test_util
from tensorflow.python.keras.mixed_precision import device_compatibility_check
from tensorflow.python.keras.mixed_precision import policy
from tensorflow.python.keras.optimizer_v2 import gradient_descent
from tensorflow.python.keras.optimizer_v2 import adagrad
from tensorflow.python.keras.optimizer_v2 import adamax
from tensorflow.python.keras.optimizer_v2 import ftrl
from tensorflow.python.keras.optimizer_v2 import nadam
from tensorflow.python.keras.optimizer_v2 import legacy_learning_rate_decay
from tensorflow.python.keras.optimizer_v2 import adadelta
from tensorflow.python.keras.optimizer_v2 import utils
from tensorflow.python.keras.optimizer_v2 import rmsprop
from tensorflow.python.keras.optimizer_v2 import learning_rate_schedule
from tensorflow.python.keras.optimizer_v2 import adam
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from tensorflow.python.keras.benchmarks.saved_model_benchmarks import saved_model_benchmark_util
from tensorflow.python.keras.saving.saved_model import network_serialization
from tensorflow.python.keras.saving.saved_model import load
from tensorflow.python.keras.saving.saved_model import json_utils
from tensorflow.python.keras.saving.saved_model import utils
from tensorflow.python.keras.saving.saved_model import metric_serialization
from tensorflow.python.keras.saving.saved_model import save
from tensorflow.python.keras.saving.saved_model import base_serialization
from tensorflow.python.keras.saving.saved_model import save_impl
from tensorflow.python.keras.saving.saved_model import serialized_attributes
from tensorflow.python.keras.saving.saved_model import model_serialization
from tensorflow.python.keras.saving.saved_model import layer_serialization
from tensorflow.python.keras.layers.preprocessing import string_lookup
from tensorflow.python.keras.layers.preprocessing import reduction
from tensorflow.python.keras.layers.preprocessing import hashing
from tensorflow.python.keras.layers.preprocessing import discretization
from tensorflow.python.keras.layers.preprocessing import integer_lookup_v1
from tensorflow.python.keras.layers.preprocessing import preprocessing_stage
from tensorflow.python.keras.layers.preprocessing import string_lookup_v1
from tensorflow.python.keras.layers.preprocessing import category_crossing
from tensorflow.python.keras.layers.preprocessing import table_utils
from tensorflow.python.keras.layers.preprocessing import category_encoding
from tensorflow.python.keras.layers.preprocessing import image_preprocessing
from tensorflow.python.keras.layers.preprocessing import index_lookup_v1
from tensorflow.python.keras.layers.preprocessing import text_vectorization
from tensorflow.python.keras.layers.preprocessing import category_encoding_v1
from tensorflow.python.keras.layers.preprocessing import index_lookup
from tensorflow.python.keras.layers.preprocessing import normalization_v1
from tensorflow.python.keras.layers.preprocessing import preprocessing_test_utils
from tensorflow.python.keras.layers.preprocessing import normalization
from tensorflow.python.keras.layers.preprocessing import text_vectorization_v1
from tensorflow.python.keras.layers.preprocessing import integer_lookup
from tensorflow.python.keras.layers.ops import core
from tensorflow.python.keras.layers.legacy_rnn import rnn_cell_impl
from tensorflow.python.keras.layers.legacy_rnn import rnn_cell_wrapper_impl
from tensorflow.python.ops.parallel_for import gradients
from tensorflow.python.ops.parallel_for import pfor
from tensorflow.python.ops.parallel_for import test_util
from tensorflow.python.ops.parallel_for import control_flow_ops
from tensorflow.python.ops.losses import losses_impl
from tensorflow.python.ops.losses import loss_reduction
from tensorflow.python.ops.losses import util
from tensorflow.python.ops.distributions import special_math
from tensorflow.python.ops.distributions import transformed_distribution
from tensorflow.python.ops.distributions import bijector_impl
from tensorflow.python.ops.distributions import dirichlet_multinomial
from tensorflow.python.ops.distributions import categorical
from tensorflow.python.ops.distributions import laplace
from tensorflow.python.ops.distributions import bernoulli
from tensorflow.python.ops.distributions import normal
from tensorflow.python.ops.distributions import student_t
from tensorflow.python.ops.distributions import uniform
from tensorflow.python.ops.distributions import distribution
from tensorflow.python.ops.distributions import util
from tensorflow.python.ops.distributions import exponential
from tensorflow.python.ops.distributions import beta
from tensorflow.python.ops.distributions import bijector_test_util
from tensorflow.python.ops.distributions import kullback_leibler
from tensorflow.python.ops.distributions import gamma
from tensorflow.python.ops.distributions import identity_bijector
from tensorflow.python.ops.distributions import multinomial
from tensorflow.python.ops.distributions import dirichlet
from tensorflow.python.ops.signal import reconstruction_ops
from tensorflow.python.ops.signal import util_ops
from tensorflow.python.ops.signal import window_ops
from tensorflow.python.ops.signal import mfcc_ops
from tensorflow.python.ops.signal import mel_ops
from tensorflow.python.ops.signal import fft_ops
from tensorflow.python.ops.signal import shape_ops
from tensorflow.python.ops.signal import spectral_ops
from tensorflow.python.ops.signal import dct_ops
from tensorflow.python.ops.linalg import linear_operator_kronecker
from tensorflow.python.ops.linalg import linear_operator_block_diag
from tensorflow.python.ops.linalg import registrations_util
from tensorflow.python.ops.linalg import matmul_registrations
from tensorflow.python.ops.linalg import linear_operator_adjoint
from tensorflow.python.ops.linalg import linear_operator_test_util
from tensorflow.python.ops.linalg import linear_operator_block_lower_triangular
from tensorflow.python.ops.linalg import linear_operator_inversion
from tensorflow.python.ops.linalg import linear_operator_full_matrix
from tensorflow.python.ops.linalg import linear_operator_tridiag
from tensorflow.python.ops.linalg import linalg_impl
from tensorflow.python.ops.linalg import adjoint_registrations
from tensorflow.python.ops.linalg import linear_operator_circulant
from tensorflow.python.ops.linalg import linear_operator_addition
from tensorflow.python.ops.linalg import cholesky_registrations
from tensorflow.python.ops.linalg import inverse_registrations
from tensorflow.python.ops.linalg import linear_operator_diag
from tensorflow.python.ops.linalg import linear_operator_zeros
from tensorflow.python.ops.linalg import linear_operator
from tensorflow.python.ops.linalg import linear_operator_lower_triangular
from tensorflow.python.ops.linalg import linear_operator_util
from tensorflow.python.ops.linalg import linear_operator_householder
from tensorflow.python.ops.linalg import linear_operator_algebra
from tensorflow.python.ops.linalg import linear_operator_toeplitz
from tensorflow.python.ops.linalg import linear_operator_identity
from tensorflow.python.ops.linalg import linear_operator_permutation
from tensorflow.python.ops.linalg import solve_registrations
from tensorflow.python.ops.linalg import linear_operator_composition
from tensorflow.python.ops.linalg import linear_operator_low_rank_update
from tensorflow.python.ops.structured import structured_tensor
from tensorflow.python.ops.numpy_ops import np_dtypes
from tensorflow.python.ops.numpy_ops import np_export
from tensorflow.python.ops.numpy_ops import np_arrays
from tensorflow.python.ops.numpy_ops import np_math_ops
from tensorflow.python.ops.numpy_ops import np_array_ops
from tensorflow.python.ops.numpy_ops import np_random
from tensorflow.python.ops.numpy_ops import np_utils
from tensorflow.python.ops.ragged import ragged_functional_ops
from tensorflow.python.ops.ragged import ragged_tensor
from tensorflow.python.ops.ragged import ragged_concat_ops
from tensorflow.python.ops.ragged import ragged_operators
from tensorflow.python.ops.ragged import row_partition
from tensorflow.python.ops.ragged import ragged_string_ops
from tensorflow.python.ops.ragged import ragged_getitem
from tensorflow.python.ops.ragged import ragged_array_ops
from tensorflow.python.ops.ragged import ragged_factory_ops
from tensorflow.python.ops.ragged import ragged_map_ops
from tensorflow.python.ops.ragged import segment_id_ops
from tensorflow.python.ops.ragged import ragged_tensor_value
from tensorflow.python.ops.ragged import ragged_squeeze_op
from tensorflow.python.ops.ragged import ragged_batch_gather_ops
from tensorflow.python.ops.ragged import ragged_config
from tensorflow.python.ops.ragged import ragged_dispatch
from tensorflow.python.ops.ragged import ragged_gather_ops
from tensorflow.python.ops.ragged import ragged_tensor_shape
from tensorflow.python.ops.ragged import ragged_math_ops
from tensorflow.python.ops.ragged import ragged_where_op
from tensorflow.python.ops.ragged import ragged_conversion_ops
from tensorflow.python.ops.ragged import ragged_util
from tensorflow.python.ops.ragged import ragged_batch_gather_with_default_op
from tensorflow.python.ops.linalg.sparse import gen_sparse_csr_matrix_ops
from tensorflow.python.ops.linalg.sparse import sparse_csr_matrix_ops
from tensorflow.python.ops.linalg.sparse import sparse_csr_matrix_grad
from tensorflow.python.ops.linalg.sparse import conjugate_gradient
from tensorflow.python.training.experimental import loss_scale
from tensorflow.python.training.experimental import loss_scale_optimizer
from tensorflow.python.training.experimental import loss_scaling_gradient_tape
from tensorflow.python.training.experimental import mixed_precision
from tensorflow.python.training.saving import checkpoint_options
from tensorflow.python.training.saving import functional_saver
from tensorflow.python.training.saving import saveable_object
from tensorflow.python.training.saving import saveable_object_util
from tensorflow.python.training.saving import saveable_hook
from tensorflow.python.training.tracking import graph_view
from tensorflow.python.training.tracking import base
from tensorflow.python.training.tracking import data_structures
from tensorflow.python.training.tracking import util
from tensorflow.python.training.tracking import tracking
from tensorflow.python.training.tracking import python_state
from tensorflow.python.training.tracking import layer_utils
from tensorflow.python.eager.memory_tests import memory_test_util
from tensorflow.python.tools.api.generator import create_python_api
from tensorflow.python.tools.api.generator import doc_srcs
from tensorflow.python.summary.writer import event_file_writer_v2
from tensorflow.python.summary.writer import writer
from tensorflow.python.summary.writer import writer_cache
from tensorflow.python.summary.writer import event_file_writer
from tensorflow.python.kernel_tests.signal import test_util
from tensorflow.python.kernel_tests.random import util
from tensorflow.python.autograph.impl import conversion
from tensorflow.python.autograph.impl import api
from tensorflow.python.autograph.core import config_lib
from tensorflow.python.autograph.core import ag_ctx
from tensorflow.python.autograph.core import converter_testing
from tensorflow.python.autograph.core import converter
from tensorflow.python.autograph.core import unsupported_features_checker
from tensorflow.python.autograph.core import function_wrappers
from tensorflow.python.autograph.utils import testing
from tensorflow.python.autograph.utils import misc
from tensorflow.python.autograph.utils import context_managers
from tensorflow.python.autograph.utils import tensor_list
from tensorflow.python.autograph.utils import py_func
from tensorflow.python.autograph.utils import compat_util
from tensorflow.python.autograph.utils import tensors
from tensorflow.python.autograph.utils import ag_logging
from tensorflow.python.autograph.operators import variables
from tensorflow.python.autograph.operators import conditional_expressions
from tensorflow.python.autograph.operators import py_builtins
from tensorflow.python.autograph.operators import control_flow
from tensorflow.python.autograph.operators import data_structures
from tensorflow.python.autograph.operators import control_flow_deprecated_py2
from tensorflow.python.autograph.operators import logical
from tensorflow.python.autograph.operators import slices
from tensorflow.python.autograph.operators import exceptions
from tensorflow.python.autograph.converters import variables
from tensorflow.python.autograph.converters import conditional_expressions
from tensorflow.python.autograph.converters import logical_expressions
from tensorflow.python.autograph.converters import control_flow
from tensorflow.python.autograph.converters import asserts
from tensorflow.python.autograph.converters import directives
from tensorflow.python.autograph.converters import control_flow_deprecated_py2
from tensorflow.python.autograph.converters import slices
from tensorflow.python.autograph.converters import lists
from tensorflow.python.autograph.converters import call_trees
from tensorflow.python.autograph.converters import functions
from tensorflow.python.autograph.converters import list_comprehensions
from tensorflow.python.autograph.converters import continue_statements
from tensorflow.python.autograph.converters import break_statements
from tensorflow.python.autograph.converters import return_statements
from tensorflow.python.autograph.pyct import anno
from tensorflow.python.autograph.pyct import transformer
from tensorflow.python.autograph.pyct import inspect_utils
from tensorflow.python.autograph.pyct import naming
from tensorflow.python.autograph.pyct import parser
from tensorflow.python.autograph.pyct import error_utils
from tensorflow.python.autograph.pyct import cfg
from tensorflow.python.autograph.pyct import templates
from tensorflow.python.autograph.pyct import ast_util
from tensorflow.python.autograph.pyct import qual_names
from tensorflow.python.autograph.pyct import transpiler
from tensorflow.python.autograph.pyct import origin_info
from tensorflow.python.autograph.pyct import loader
from tensorflow.python.autograph.pyct import cache
from tensorflow.python.autograph.pyct import pretty_printer
from tensorflow.python.autograph.pyct import errors
from tensorflow.python.autograph.pyct import gast_util
from tensorflow.python.autograph.lang import directives
from tensorflow.python.autograph.lang import special_functions
from tensorflow.python.autograph.pyct.common_transformers import anf
from tensorflow.python.autograph.pyct.testing import decorators
from tensorflow.python.autograph.pyct.testing import basic_definitions
from tensorflow.python.autograph.pyct.static_analysis import activity
from tensorflow.python.autograph.pyct.static_analysis import reaching_definitions
from tensorflow.python.autograph.pyct.static_analysis import reaching_fndefs
from tensorflow.python.autograph.pyct.static_analysis import liveness
from tensorflow.python.autograph.pyct.static_analysis import type_inference
from tensorflow.python.autograph.pyct.static_analysis import annos
from tensorflow.python.lib.io import file_io
from tensorflow.python.lib.io import tf_record
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
from tensorflow.python.keras import activations
from tensorflow.python.keras import losses
from tensorflow.python.keras import regularizers
from tensorflow.python.keras import combinations
from tensorflow.python.keras import constraints
from tensorflow.python.keras import metrics
from tensorflow.python.keras import backend_config
from tensorflow.python.keras import backend
from tensorflow.python.keras import callbacks
from tensorflow.python.ops import manip_grad
from tensorflow.python.ops import variables
from tensorflow.python.ops import functional_ops
from tensorflow.python.ops import gen_set_ops
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import gen_script_ops
from tensorflow.python.ops import gen_batch_ops
from tensorflow.python.ops import custom_gradient
from tensorflow.python.ops import linalg_grad
from tensorflow.python.ops import clip_ops
from tensorflow.python.ops import gen_ctc_ops
from tensorflow.python.ops import gen_image_ops
from tensorflow.python.ops import cond_v2
from tensorflow.python.ops import histogram_ops
from tensorflow.python.ops import gen_spectral_ops
from tensorflow.python.ops import gen_sdca_ops
from tensorflow.python.ops import gen_tensor_forest_ops
from tensorflow.python.ops import gen_ragged_math_ops
from tensorflow.python.ops import gen_candidate_sampling_ops
from tensorflow.python.ops import gen_boosted_trees_ops
from tensorflow.python.ops import manip_ops
from tensorflow.python.ops import unconnected_gradients
from tensorflow.python.ops import nn_impl
from tensorflow.python.ops import parsing_ops
from tensorflow.python.ops import gen_checkpoint_ops
from tensorflow.python.ops import variable_scope
from tensorflow.python.ops import io_ops
from tensorflow.python.ops import embedding_ops
from tensorflow.python.ops import weights_broadcast_ops
from tensorflow.python.ops import while_v2_indexed_slices_rewriter
from tensorflow.python.ops import map_fn
from tensorflow.python.ops import gen_sparse_ops
from tensorflow.python.ops import numerics
from tensorflow.python.ops import gen_ragged_conversion_ops
from tensorflow.python.ops import tensor_array_ops
from tensorflow.python.ops import gen_encode_proto_ops
from tensorflow.python.ops import array_grad
from tensorflow.python.ops import gradients_util
from tensorflow.python.ops import math_grad
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import session_ops
from tensorflow.python.ops import gen_stateless_random_ops_v2
from tensorflow.python.ops import gen_io_ops
from tensorflow.python.ops import list_ops
from tensorflow.python.ops import batch_ops
from tensorflow.python.ops import optional_grad
from tensorflow.python.ops import linalg_ops_impl
from tensorflow.python.ops import gen_array_ops
from tensorflow.python.ops import gen_linalg_ops
from tensorflow.python.ops import lookup_ops
from tensorflow.python.ops import map_ops
from tensorflow.python.ops import gen_debug_ops
from tensorflow.python.ops import gen_nccl_ops
from tensorflow.python.ops import gen_training_ops
from tensorflow.python.ops import data_flow_grad
from tensorflow.python.ops import random_ops
from tensorflow.python.ops import gen_random_ops
from tensorflow.python.ops import sparse_ops
from tensorflow.python.ops import gen_special_math_ops
from tensorflow.python.ops import string_ops
from tensorflow.python.ops import gen_string_ops
from tensorflow.python.ops import summary_op_util
from tensorflow.python.ops import op_selector
from tensorflow.python.ops import gen_user_ops
from tensorflow.python.ops import gen_dataset_ops
from tensorflow.python.ops import control_flow_util
from tensorflow.python.ops import init_ops_v2
from tensorflow.python.ops import boosted_trees_ops
from tensorflow.python.ops import image_ops
from tensorflow.python.ops import nn_ops
from tensorflow.python.ops import gen_manip_ops
from tensorflow.python.ops import bincount_ops
from tensorflow.python.ops import collective_ops
from tensorflow.python.ops import gen_parsing_ops
from tensorflow.python.ops import rnn
from tensorflow.python.ops import sparse_grad
from tensorflow.python.ops import gradients_impl
from tensorflow.python.ops import gen_data_flow_ops
from tensorflow.python.ops import resources
from tensorflow.python.ops import nn_grad
from tensorflow.python.ops import gen_collective_ops
from tensorflow.python.ops import control_flow_v2_func_graphs
from tensorflow.python.ops import gen_nn_ops
from tensorflow.python.ops import metrics_impl
from tensorflow.python.ops import sets_impl
from tensorflow.python.ops import cudnn_rnn_grad
from tensorflow.python.ops import gen_state_ops
from tensorflow.python.ops import tensor_array_grad
from tensorflow.python.ops import image_ops_impl
from tensorflow.python.ops import partitioned_variables
from tensorflow.python.ops import gradient_checker_v2
from tensorflow.python.ops import nccl_ops
from tensorflow.python.ops import check_ops
from tensorflow.python.ops import gen_math_ops
from tensorflow.python.ops import critical_section_ops
from tensorflow.python.ops import gen_summary_ops
from tensorflow.python.ops import control_flow_util_v2
from tensorflow.python.ops import stateful_random_ops
from tensorflow.python.ops import sort_ops
from tensorflow.python.ops import parsing_config
from tensorflow.python.ops import gen_decode_proto_ops
from tensorflow.python.ops import control_flow_v2_toggles
from tensorflow.python.ops import data_flow_ops
from tensorflow.python.ops import gen_rnn_ops
from tensorflow.python.ops import gen_sendrecv_ops
from tensorflow.python.ops import gen_cudnn_rnn_ops
from tensorflow.python.ops import gen_stateless_random_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import inplace_ops
from tensorflow.python.ops import linalg_ops
from tensorflow.python.ops import gradient_checker
from tensorflow.python.ops import gen_bitwise_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import special_math_ops
from tensorflow.python.ops import logging_ops
from tensorflow.python.ops import image_grad
from tensorflow.python.ops import ctc_ops
from tensorflow.python.ops import image_grad_test_base
from tensorflow.python.ops import gen_stateful_random_ops
from tensorflow.python.ops import random_grad
from tensorflow.python.ops import gen_tpu_ops
from tensorflow.python.ops import gen_resource_variable_ops
from tensorflow.python.ops import confusion_matrix
from tensorflow.python.ops import gen_functional_ops
from tensorflow.python.ops import handle_data_util
from tensorflow.python.ops import tensor_forest_ops
from tensorflow.python.ops import gen_experimental_dataset_ops
from tensorflow.python.ops import script_ops
from tensorflow.python.ops import rnn_grad
from tensorflow.python.ops import while_v2
from tensorflow.python.ops import gen_logging_ops
from tensorflow.python.ops import summary_ops_v2
from tensorflow.python.ops import gen_ragged_array_ops
from tensorflow.python.ops import gen_map_ops
from tensorflow.python.ops import control_flow_grad
from tensorflow.python.ops import gen_audio_ops
from tensorflow.python.ops import stateless_random_ops
from tensorflow.python.ops import gen_lookup_ops
from tensorflow.python.ops import gen_clustering_ops
from tensorflow.python.ops import gen_count_ops
from tensorflow.python.ops import gen_control_flow_ops
from tensorflow.python.ops import candidate_sampling_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.ops import template
from tensorflow.python.ops import default_gradient
from tensorflow.python.ops import clustering_ops
from tensorflow.python.ops import resource_variable_ops
from tensorflow.python.ops import control_flow_state
from tensorflow.python.ops import gen_list_ops
from tensorflow.python.training import gradient_descent
from tensorflow.python.training import proximal_gradient_descent
from tensorflow.python.training import sync_replicas_optimizer
from tensorflow.python.training import adagrad
from tensorflow.python.training import coordinator
from tensorflow.python.training import checkpoint_ops
from tensorflow.python.training import session_manager
from tensorflow.python.training import ftrl
from tensorflow.python.training import session_run_hook
from tensorflow.python.training import saver
from tensorflow.python.training import device_setter
from tensorflow.python.training import server_lib
from tensorflow.python.training import training_util
from tensorflow.python.training import checkpoint_utils
from tensorflow.python.training import adagrad_da
from tensorflow.python.training import momentum
from tensorflow.python.training import monitored_session
from tensorflow.python.training import adadelta
from tensorflow.python.training import optimizer
from tensorflow.python.training import saver_test_utils
from tensorflow.python.training import moving_averages
from tensorflow.python.training import basic_session_run_hooks
from tensorflow.python.training import rmsprop
from tensorflow.python.training import py_checkpoint_reader
from tensorflow.python.training import slot_creator
from tensorflow.python.training import checkpoint_management
from tensorflow.python.training import quantize_training
from tensorflow.python.training import adam
from tensorflow.python.training import tensorboard_logging
from tensorflow.python.training import warm_starting_util
from tensorflow.python.training import summary_io
from tensorflow.python.training import supervisor
from tensorflow.python.training import basic_loops
from tensorflow.python.training import queue_runner_impl
from tensorflow.python.training import evaluation
from tensorflow.python.training import input
from tensorflow.python.training import proximal_adagrad
from tensorflow.python.eager import executor
from tensorflow.python.eager import wrap_function
from tensorflow.python.eager import backprop_util
from tensorflow.python.eager import graph_only_ops
from tensorflow.python.eager import imperative_grad
from tensorflow.python.eager import profiler_client
from tensorflow.python.eager import forwardprop_util
from tensorflow.python.eager import profiler
from tensorflow.python.eager import def_function
from tensorflow.python.eager import core
from tensorflow.python.eager import test
from tensorflow.python.eager import forwardprop
from tensorflow.python.eager import monitoring
from tensorflow.python.eager import cancellation
from tensorflow.python.eager import remote
from tensorflow.python.eager import execute
from tensorflow.python.eager import function
from tensorflow.python.eager import tape
from tensorflow.python.eager import lift_to_graph
from tensorflow.python.eager import backprop
from tensorflow.python.eager import benchmarks_test_base
from tensorflow.python.eager import context
from tensorflow.python.module import module
from tensorflow.python.summary import summary
from tensorflow.python.summary import plugin_asset
from tensorflow.python.summary import summary_iterator
from tensorflow.python.layers import utils
from tensorflow.python.grappler import item
from tensorflow.python.grappler import cluster
from tensorflow.python.grappler import tf_optimizer
from tensorflow.python.types import internal
from tensorflow.python.types import distribute
from tensorflow.python.types import core
from tensorflow.python.types import doc_typealias
from tensorflow.python.profiler.internal import flops_registry
from tensorflow.python.compiler.mlir import mlir
from tensorflow.python.compiler.xla import jit
from tensorflow.python.compiler.xla import xla
from tensorflow.python.compiler.tensorrt import trt_convert
from tensorflow.python.compiler.tensorrt.test import tf_trt_integration_test_base
from tensorflow.python.tpu.client import client
from tensorflow.python.tpu.ops import tpu_ops
from tensorflow.python.distribute.coordinator import metric_utils
from tensorflow.python.distribute.coordinator import utils
from tensorflow.python.distribute.coordinator import cluster_coordinator
from tensorflow.python.distribute.cluster_resolver import slurm_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import sagemaker_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import kubernetes_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import gce_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import tfconfig_cluster_resolver
from tensorflow.python.distribute.cluster_resolver import cluster_resolver
from tensorflow.python.distribute.parallel_device import parallel_device
from tensorflow.python.distribute.parallel_device import saving
from tensorflow.python.saved_model.model_utils import export_output
from tensorflow.python.saved_model.model_utils import mode_keys
from tensorflow.python.saved_model.model_utils import export_utils
from tensorflow.python.util.protobuf import compare
from tensorflow.python.data.util import structure
from tensorflow.python.data.util import random_seed
from tensorflow.python.data.util import traverse
from tensorflow.python.data.util import sparse
from tensorflow.python.data.util import options
from tensorflow.python.data.util import nest
from tensorflow.python.data.util import convert
from tensorflow.python.data.ops import iterator_ops
from tensorflow.python.data.ops import optional_ops
from tensorflow.python.data.ops import multi_device_iterator_ops
from tensorflow.python.data.ops import readers
from tensorflow.python.data.ops import dataset_ops
from tensorflow.python.data.benchmarks import benchmark_base
from tensorflow.python.data.experimental.service import server_lib
from tensorflow.python.data.experimental.ops import iterator_ops
from tensorflow.python.data.experimental.ops import optimization
from tensorflow.python.data.experimental.ops import testing
from tensorflow.python.data.experimental.ops import stats_ops
from tensorflow.python.data.experimental.ops import scan_ops
from tensorflow.python.data.experimental.ops import compression_ops
from tensorflow.python.data.experimental.ops import optimization_options
from tensorflow.python.data.experimental.ops import unique
from tensorflow.python.data.experimental.ops import parsing_ops
from tensorflow.python.data.experimental.ops import distribute
from tensorflow.python.data.experimental.ops import get_single_element
from tensorflow.python.data.experimental.ops import stats_aggregator
from tensorflow.python.data.experimental.ops import take_while_ops
from tensorflow.python.data.experimental.ops import counter
from tensorflow.python.data.experimental.ops import threadpool
from tensorflow.python.data.experimental.ops import snapshot
from tensorflow.python.data.experimental.ops import cardinality
from tensorflow.python.data.experimental.ops import random_ops
from tensorflow.python.data.experimental.ops import error_ops
from tensorflow.python.data.experimental.ops import prefetching_ops
from tensorflow.python.data.experimental.ops import enumerate_ops
from tensorflow.python.data.experimental.ops import map_defun
from tensorflow.python.data.experimental.ops import shuffle_ops
from tensorflow.python.data.experimental.ops import stats_options
from tensorflow.python.data.experimental.ops import threading_options
from tensorflow.python.data.experimental.ops import grouping
from tensorflow.python.data.experimental.ops import interleave_ops
from tensorflow.python.data.experimental.ops import matching_files
from tensorflow.python.data.experimental.ops import distribute_options
from tensorflow.python.data.experimental.ops import io
from tensorflow.python.data.experimental.ops import resampling
from tensorflow.python.data.experimental.ops import writers
from tensorflow.python.data.experimental.ops import batching
from tensorflow.python.data.experimental.ops import data_service_ops
from tensorflow.python.data.experimental.ops import readers
from tensorflow.python.data.experimental.kernel_tests.serialization import dataset_serialization_test_base
from tensorflow.python.debug.examples import debug_mnist
from tensorflow.python.debug.cli import profile_analyzer_cli
from tensorflow.python.debug.cli import base_ui
from tensorflow.python.debug.cli import debugger_cli_common
from tensorflow.python.debug.cli import cli_test_utils
from tensorflow.python.debug.cli import analyzer_cli
from tensorflow.python.debug.cli import command_parser
from tensorflow.python.debug.cli import cli_config
from tensorflow.python.debug.cli import curses_widgets
from tensorflow.python.debug.cli import cli_shared
from tensorflow.python.debug.cli import evaluator
from tensorflow.python.debug.cli import tensor_format
from tensorflow.python.debug.cli import ui_factory
from tensorflow.python.debug.cli import curses_ui
from tensorflow.python.debug.cli import readline_ui
from tensorflow.python.debug.cli import offline_analyzer
from tensorflow.python.debug.wrappers import framework
from tensorflow.python.debug.wrappers import grpc_wrapper
from tensorflow.python.debug.wrappers import local_cli_wrapper
from tensorflow.python.debug.wrappers import hooks
from tensorflow.python.debug.wrappers import dumping_wrapper
from tensorflow.python.debug.examples.v1 import debug_keras
from tensorflow.python.debug.examples.v1 import debug_mnist_v1
from tensorflow.python.debug.examples.v1 import debug_fibonacci
from tensorflow.python.debug.examples.v1 import debug_errors
from tensorflow.python.debug.examples.v2 import debug_mnist_v2
from tensorflow.python.debug.examples.v2 import debug_fibonacci_v2
from tensorflow.python.keras.engine import compile_utils
from tensorflow.python.keras.engine import input_layer
from tensorflow.python.keras.engine import training_utils_v1
from tensorflow.python.keras.engine import training_eager_v1
from tensorflow.python.keras.engine import partial_batch_padding_handler
from tensorflow.python.keras.engine import base_layer_v1
from tensorflow.python.keras.engine import base_preprocessing_layer
from tensorflow.python.keras.engine import base_layer_utils
from tensorflow.python.keras.engine import functional
from tensorflow.python.keras.engine import training_v1
from tensorflow.python.keras.engine import training_utils
from tensorflow.python.keras.engine import sequential
from tensorflow.python.keras.engine import base_layer
from tensorflow.python.keras.engine import training_generator_v1
from tensorflow.python.keras.engine import training_arrays_v1
from tensorflow.python.keras.engine import training
from tensorflow.python.keras.engine import keras_tensor
from tensorflow.python.keras.engine import input_spec
from tensorflow.python.keras.engine import data_adapter
from tensorflow.python.keras.engine import base_preprocessing_layer_v1
from tensorflow.python.keras.engine import training_distributed_v1
from tensorflow.python.keras.engine import node
from tensorflow.python.keras.preprocessing import text_dataset
from tensorflow.python.keras.preprocessing import dataset_utils
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.preprocessing import sequence
from tensorflow.python.keras.preprocessing import timeseries
from tensorflow.python.keras.preprocessing import text
from tensorflow.python.keras.preprocessing import image_dataset
from tensorflow.python.keras.distribute import keras_image_model_correctness_test
from tensorflow.python.keras.distribute import keras_utils_test
from tensorflow.python.keras.distribute import keras_stateful_lstm_model_correctness_test
from tensorflow.python.keras.distribute import keras_embedding_model_correctness_test
from tensorflow.python.keras.distribute import distributed_training_utils_v1
from tensorflow.python.keras.distribute import keras_correctness_test_base
from tensorflow.python.keras.distribute import keras_rnn_model_correctness_test
from tensorflow.python.keras.distribute import distribute_strategy_test
from tensorflow.python.keras.distribute import distributed_training_utils
from tensorflow.python.keras.distribute import saved_model_test_base
from tensorflow.python.keras.distribute import worker_training_state
from tensorflow.python.keras.distribute import simple_models
from tensorflow.python.keras.distribute import optimizer_combinations
from tensorflow.python.keras.distribute import keras_dnn_correctness_test
from tensorflow.python.keras.distribute import multi_worker_testing_utils
from tensorflow.python.keras.distribute import model_collection_base
from tensorflow.python.keras.tests import model_subclassing_test_util
from tensorflow.python.keras.tests import model_architectures
from tensorflow.python.keras.initializers import initializers_v1
from tensorflow.python.keras.initializers import initializers_v2
from tensorflow.python.keras.legacy_tf_layers import base
from tensorflow.python.keras.legacy_tf_layers import convolutional
from tensorflow.python.keras.legacy_tf_layers import core
from tensorflow.python.keras.legacy_tf_layers import pooling
from tensorflow.python.keras.legacy_tf_layers import normalization
from tensorflow.python.keras.datasets import fashion_mnist
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras.datasets import cifar
from tensorflow.python.keras.datasets import imdb
from tensorflow.python.keras.datasets import cifar10
from tensorflow.python.keras.datasets import boston_housing
from tensorflow.python.keras.datasets import cifar100
from tensorflow.python.keras.datasets import reuters
from tensorflow.python.keras.utils import tf_utils
from tensorflow.python.keras.utils import conv_utils
from tensorflow.python.keras.utils import tf_inspect
from tensorflow.python.keras.utils import metrics_utils
from tensorflow.python.keras.utils import tf_contextlib
from tensorflow.python.keras.utils import data_utils
from tensorflow.python.keras.utils import control_flow_util
from tensorflow.python.keras.utils import vis_utils
from tensorflow.python.keras.utils import version_utils
from tensorflow.python.keras.utils import losses_utils
from tensorflow.python.keras.utils import generic_utils
from tensorflow.python.keras.utils import multi_gpu_utils
from tensorflow.python.keras.utils import kernelized_utils
from tensorflow.python.keras.utils import layer_utils
from tensorflow.python.keras.utils import io_utils
from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras.feature_column import base_feature_layer
from tensorflow.python.keras.feature_column import dense_features_v2
from tensorflow.python.keras.feature_column import sequence_feature_column
from tensorflow.python.keras.feature_column import dense_features
from tensorflow.python.keras.wrappers import scikit_learn
from tensorflow.python.keras.premade import wide_deep
from tensorflow.python.keras.premade import linear
from tensorflow.python.keras.benchmarks import distribution_util
from tensorflow.python.keras.benchmarks import benchmark_util
from tensorflow.python.keras.saving import saving_utils
from tensorflow.python.keras.saving import saved_model_experimental
from tensorflow.python.keras.saving import model_config
from tensorflow.python.keras.saving import hdf5_format
from tensorflow.python.keras.saving import save
from tensorflow.python.keras.applications import densenet
from tensorflow.python.keras.applications import mobilenet
from tensorflow.python.keras.applications import xception
from tensorflow.python.keras.applications import vgg16
from tensorflow.python.keras.applications import mobilenet_v3
from tensorflow.python.keras.applications import vgg19
from tensorflow.python.keras.applications import resnet
from tensorflow.python.keras.applications import imagenet_utils
from tensorflow.python.keras.applications import efficientnet
from tensorflow.python.keras.applications import nasnet
from tensorflow.python.keras.applications import mobilenet_v2
from tensorflow.python.keras.applications import inception_v3
from tensorflow.python.keras.applications import inception_resnet_v2
from tensorflow.python.keras.applications import resnet_v2
from tensorflow.python.keras.layers import einsum_dense
from tensorflow.python.keras.layers import kernelized
from tensorflow.python.keras.layers import multi_head_attention
from tensorflow.python.keras.layers import wrappers
from tensorflow.python.keras.layers import rnn_cell_wrapper_v2
from tensorflow.python.keras.layers import recurrent_v2
from tensorflow.python.keras.layers import convolutional
from tensorflow.python.keras.layers import serialization
from tensorflow.python.keras.layers import normalization_v2
from tensorflow.python.keras.layers import merge
from tensorflow.python.keras.layers import local
from tensorflow.python.keras.layers import core
from tensorflow.python.keras.layers import dense_attention
from tensorflow.python.keras.layers import noise
from tensorflow.python.keras.layers import recurrent
from tensorflow.python.keras.layers import advanced_activations
from tensorflow.python.keras.layers import pooling
from tensorflow.python.keras.layers import embeddings
from tensorflow.python.keras.layers import cudnn_recurrent
from tensorflow.python.keras.layers import normalization
from tensorflow.python.keras.layers import convolutional_recurrent
from tensorflow.python.keras.mixed_precision import autocast_variable
from tensorflow.python.keras.mixed_precision import loss_scale
from tensorflow.python.keras.mixed_precision import get_layer_policy
from tensorflow.python.keras.mixed_precision import loss_scale_optimizer
from tensorflow.python.keras.mixed_precision import test_util
from tensorflow.python.keras.mixed_precision import device_compatibility_check
from tensorflow.python.keras.mixed_precision import policy
from tensorflow.python.keras.optimizer_v2 import gradient_descent
from tensorflow.python.keras.optimizer_v2 import adagrad
from tensorflow.python.keras.optimizer_v2 import adamax
from tensorflow.python.keras.optimizer_v2 import ftrl
from tensorflow.python.keras.optimizer_v2 import nadam
from tensorflow.python.keras.optimizer_v2 import legacy_learning_rate_decay
from tensorflow.python.keras.optimizer_v2 import adadelta
from tensorflow.python.keras.optimizer_v2 import utils
from tensorflow.python.keras.optimizer_v2 import rmsprop
from tensorflow.python.keras.optimizer_v2 import learning_rate_schedule
from tensorflow.python.keras.optimizer_v2 import adam
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from tensorflow.python.keras.benchmarks.saved_model_benchmarks import saved_model_benchmark_util
from tensorflow.python.keras.saving.saved_model import network_serialization
from tensorflow.python.keras.saving.saved_model import load
from tensorflow.python.keras.saving.saved_model import json_utils
from tensorflow.python.keras.saving.saved_model import utils
from tensorflow.python.keras.saving.saved_model import metric_serialization
from tensorflow.python.keras.saving.saved_model import save
from tensorflow.python.keras.saving.saved_model import base_serialization
from tensorflow.python.keras.saving.saved_model import save_impl
from tensorflow.python.keras.saving.saved_model import serialized_attributes
from tensorflow.python.keras.saving.saved_model import model_serialization
from tensorflow.python.keras.saving.saved_model import layer_serialization
from tensorflow.python.keras.layers.preprocessing import string_lookup
from tensorflow.python.keras.layers.preprocessing import reduction
from tensorflow.python.keras.layers.preprocessing import hashing
from tensorflow.python.keras.layers.preprocessing import discretization
from tensorflow.python.keras.layers.preprocessing import integer_lookup_v1
from tensorflow.python.keras.layers.preprocessing import preprocessing_stage
from tensorflow.python.keras.layers.preprocessing import string_lookup_v1
from tensorflow.python.keras.layers.preprocessing import category_crossing
from tensorflow.python.keras.layers.preprocessing import table_utils
from tensorflow.python.keras.layers.preprocessing import category_encoding
from tensorflow.python.keras.layers.preprocessing import image_preprocessing
from tensorflow.python.keras.layers.preprocessing import index_lookup_v1
from tensorflow.python.keras.layers.preprocessing import text_vectorization
from tensorflow.python.keras.layers.preprocessing import category_encoding_v1
from tensorflow.python.keras.layers.preprocessing import index_lookup
from tensorflow.python.keras.layers.preprocessing import normalization_v1
from tensorflow.python.keras.layers.preprocessing import preprocessing_test_utils
from tensorflow.python.keras.layers.preprocessing import normalization
from tensorflow.python.keras.layers.preprocessing import text_vectorization_v1
from tensorflow.python.keras.layers.preprocessing import integer_lookup
from tensorflow.python.keras.layers.ops import core
from tensorflow.python.keras.layers.legacy_rnn import rnn_cell_impl
from tensorflow.python.keras.layers.legacy_rnn import rnn_cell_wrapper_impl
from tensorflow.python.ops.parallel_for import gradients
from tensorflow.python.ops.parallel_for import pfor
from tensorflow.python.ops.parallel_for import test_util
from tensorflow.python.ops.parallel_for import control_flow_ops
from tensorflow.python.ops.losses import losses_impl
from tensorflow.python.ops.losses import loss_reduction
from tensorflow.python.ops.losses import util
from tensorflow.python.ops.distributions import special_math
from tensorflow.python.ops.distributions import transformed_distribution
from tensorflow.python.ops.distributions import bijector_impl
from tensorflow.python.ops.distributions import dirichlet_multinomial
from tensorflow.python.ops.distributions import categorical
from tensorflow.python.ops.distributions import laplace
from tensorflow.python.ops.distributions import bernoulli
from tensorflow.python.ops.distributions import normal
from tensorflow.python.ops.distributions import student_t
from tensorflow.python.ops.distributions import uniform
from tensorflow.python.ops.distributions import distribution
from tensorflow.python.ops.distributions import util
from tensorflow.python.ops.distributions import exponential
from tensorflow.python.ops.distributions import beta
from tensorflow.python.ops.distributions import bijector_test_util
from tensorflow.python.ops.distributions import kullback_leibler
from tensorflow.python.ops.distributions import gamma
from tensorflow.python.ops.distributions import identity_bijector
from tensorflow.python.ops.distributions import multinomial
from tensorflow.python.ops.distributions import dirichlet
from tensorflow.python.ops.signal import reconstruction_ops
from tensorflow.python.ops.signal import util_ops
from tensorflow.python.ops.signal import window_ops
from tensorflow.python.ops.signal import mfcc_ops
from tensorflow.python.ops.signal import mel_ops
from tensorflow.python.ops.signal import fft_ops
from tensorflow.python.ops.signal import shape_ops
from tensorflow.python.ops.signal import spectral_ops
from tensorflow.python.ops.signal import dct_ops
from tensorflow.python.ops.linalg import linear_operator_kronecker
from tensorflow.python.ops.linalg import linear_operator_block_diag
from tensorflow.python.ops.linalg import registrations_util
from tensorflow.python.ops.linalg import matmul_registrations
from tensorflow.python.ops.linalg import linear_operator_adjoint
from tensorflow.python.ops.linalg import linear_operator_test_util
from tensorflow.python.ops.linalg import linear_operator_block_lower_triangular
from tensorflow.python.ops.linalg import linear_operator_inversion
from tensorflow.python.ops.linalg import linear_operator_full_matrix
from tensorflow.python.ops.linalg import linear_operator_tridiag
from tensorflow.python.ops.linalg import linalg_impl
from tensorflow.python.ops.linalg import adjoint_registrations
from tensorflow.python.ops.linalg import linear_operator_circulant
from tensorflow.python.ops.linalg import linear_operator_addition
from tensorflow.python.ops.linalg import cholesky_registrations
from tensorflow.python.ops.linalg import inverse_registrations
from tensorflow.python.ops.linalg import linear_operator_diag
from tensorflow.python.ops.linalg import linear_operator_zeros
from tensorflow.python.ops.linalg import linear_operator
from tensorflow.python.ops.linalg import linear_operator_lower_triangular
from tensorflow.python.ops.linalg import linear_operator_util
from tensorflow.python.ops.linalg import linear_operator_householder
from tensorflow.python.ops.linalg import linear_operator_algebra
from tensorflow.python.ops.linalg import linear_operator_toeplitz
from tensorflow.python.ops.linalg import linear_operator_identity
from tensorflow.python.ops.linalg import linear_operator_permutation
from tensorflow.python.ops.linalg import solve_registrations
from tensorflow.python.ops.linalg import linear_operator_composition
from tensorflow.python.ops.linalg import linear_operator_low_rank_update
from tensorflow.python.ops.structured import structured_tensor
from tensorflow.python.ops.numpy_ops import np_dtypes
from tensorflow.python.ops.numpy_ops import np_export
from tensorflow.python.ops.numpy_ops import np_arrays
from tensorflow.python.ops.numpy_ops import np_math_ops
from tensorflow.python.ops.numpy_ops import np_array_ops
from tensorflow.python.ops.numpy_ops import np_random
from tensorflow.python.ops.numpy_ops import np_utils
from tensorflow.python.ops.ragged import ragged_functional_ops
from tensorflow.python.ops.ragged import ragged_tensor
from tensorflow.python.ops.ragged import ragged_concat_ops
from tensorflow.python.ops.ragged import ragged_operators
from tensorflow.python.ops.ragged import row_partition
from tensorflow.python.ops.ragged import ragged_string_ops
from tensorflow.python.ops.ragged import ragged_getitem
from tensorflow.python.ops.ragged import ragged_array_ops
from tensorflow.python.ops.ragged import ragged_factory_ops
from tensorflow.python.ops.ragged import ragged_map_ops
from tensorflow.python.ops.ragged import segment_id_ops
from tensorflow.python.ops.ragged import ragged_tensor_value
from tensorflow.python.ops.ragged import ragged_squeeze_op
from tensorflow.python.ops.ragged import ragged_batch_gather_ops
from tensorflow.python.ops.ragged import ragged_config
from tensorflow.python.ops.ragged import ragged_dispatch
from tensorflow.python.ops.ragged import ragged_gather_ops
from tensorflow.python.ops.ragged import ragged_tensor_shape
from tensorflow.python.ops.ragged import ragged_math_ops
from tensorflow.python.ops.ragged import ragged_where_op
from tensorflow.python.ops.ragged import ragged_conversion_ops
from tensorflow.python.ops.ragged import ragged_util
from tensorflow.python.ops.ragged import ragged_batch_gather_with_default_op
from tensorflow.python.ops.linalg.sparse import gen_sparse_csr_matrix_ops
from tensorflow.python.ops.linalg.sparse import sparse_csr_matrix_ops
from tensorflow.python.ops.linalg.sparse import sparse_csr_matrix_grad
from tensorflow.python.ops.linalg.sparse import conjugate_gradient
from tensorflow.python.training.experimental import loss_scale
from tensorflow.python.training.experimental import loss_scale_optimizer
from tensorflow.python.training.experimental import loss_scaling_gradient_tape
from tensorflow.python.training.experimental import mixed_precision
from tensorflow.python.training.saving import checkpoint_options
from tensorflow.python.training.saving import functional_saver
from tensorflow.python.training.saving import saveable_object
from tensorflow.python.training.saving import saveable_object_util
from tensorflow.python.training.saving import saveable_hook
from tensorflow.python.training.tracking import graph_view
from tensorflow.python.training.tracking import base
from tensorflow.python.training.tracking import data_structures
from tensorflow.python.training.tracking import util
from tensorflow.python.training.tracking import tracking
from tensorflow.python.training.tracking import python_state
from tensorflow.python.training.tracking import layer_utils
from tensorflow.python.eager.memory_tests import memory_test_util
from tensorflow.python.tools.api.generator import create_python_api
from tensorflow.python.tools.api.generator import doc_srcs
from tensorflow.python.summary.writer import event_file_writer_v2
from tensorflow.python.summary.writer import writer
from tensorflow.python.summary.writer import writer_cache
from tensorflow.python.summary.writer import event_file_writer
from tensorflow.python.kernel_tests.signal import test_util
from tensorflow.python.kernel_tests.random import util
from tensorflow.python.autograph.impl import conversion
from tensorflow.python.autograph.impl import api
from tensorflow.python.autograph.core import config_lib
from tensorflow.python.autograph.core import ag_ctx
from tensorflow.python.autograph.core import converter_testing
from tensorflow.python.autograph.core import converter
from tensorflow.python.autograph.core import unsupported_features_checker
from tensorflow.python.autograph.core import function_wrappers
from tensorflow.python.autograph.utils import testing
from tensorflow.python.autograph.utils import misc
from tensorflow.python.autograph.utils import context_managers
from tensorflow.python.autograph.utils import tensor_list
from tensorflow.python.autograph.utils import py_func
from tensorflow.python.autograph.utils import compat_util
from tensorflow.python.autograph.utils import tensors
from tensorflow.python.autograph.utils import ag_logging
from tensorflow.python.autograph.operators import variables
from tensorflow.python.autograph.operators import conditional_expressions
from tensorflow.python.autograph.operators import py_builtins
from tensorflow.python.autograph.operators import control_flow
from tensorflow.python.autograph.operators import data_structures
from tensorflow.python.autograph.operators import control_flow_deprecated_py2
from tensorflow.python.autograph.operators import logical
from tensorflow.python.autograph.operators import slices
from tensorflow.python.autograph.operators import exceptions
from tensorflow.python.autograph.converters import variables
from tensorflow.python.autograph.converters import conditional_expressions
from tensorflow.python.autograph.converters import logical_expressions
from tensorflow.python.autograph.converters import control_flow
from tensorflow.python.autograph.converters import asserts
from tensorflow.python.autograph.converters import directives
from tensorflow.python.autograph.converters import control_flow_deprecated_py2
from tensorflow.python.autograph.converters import slices
from tensorflow.python.autograph.converters import lists
from tensorflow.python.autograph.converters import call_trees
from tensorflow.python.autograph.converters import functions
from tensorflow.python.autograph.converters import list_comprehensions
from tensorflow.python.autograph.converters import continue_statements
from tensorflow.python.autograph.converters import break_statements
from tensorflow.python.autograph.converters import return_statements
from tensorflow.python.autograph.pyct import anno
from tensorflow.python.autograph.pyct import transformer
from tensorflow.python.autograph.pyct import inspect_utils
from tensorflow.python.autograph.pyct import naming
from tensorflow.python.autograph.pyct import parser
from tensorflow.python.autograph.pyct import error_utils
from tensorflow.python.autograph.pyct import cfg
from tensorflow.python.autograph.pyct import templates
from tensorflow.python.autograph.pyct import ast_util
from tensorflow.python.autograph.pyct import qual_names
from tensorflow.python.autograph.pyct import transpiler
from tensorflow.python.autograph.pyct import origin_info
from tensorflow.python.autograph.pyct import loader
from tensorflow.python.autograph.pyct import cache
from tensorflow.python.autograph.pyct import pretty_printer
from tensorflow.python.autograph.pyct import errors
from tensorflow.python.autograph.pyct import gast_util
from tensorflow.python.autograph.lang import directives
from tensorflow.python.autograph.lang import special_functions
from tensorflow.python.autograph.pyct.common_transformers import anf
from tensorflow.python.autograph.pyct.testing import decorators
from tensorflow.python.autograph.pyct.testing import basic_definitions
from tensorflow.python.autograph.pyct.static_analysis import activity
from tensorflow.python.autograph.pyct.static_analysis import reaching_definitions
from tensorflow.python.autograph.pyct.static_analysis import reaching_fndefs
from tensorflow.python.autograph.pyct.static_analysis import liveness
from tensorflow.python.autograph.pyct.static_analysis import type_inference
from tensorflow.python.autograph.pyct.static_analysis import annos
from tensorflow.python.lib.io import file_io
from tensorflow.python.lib.io import tf_record


tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import inspect
from tensorflow.instrumentation.decorators import dump_signature_of_class, dump_signature_of_function
def hijack(output_dir="signature_db"):
    hijack_all(output_dir)


def hijack_api(obj, func_name_str, obj_hint, output_dir):
    """
    Function to hijack an API.

    Args:
        obj: the base module. This function is currently specific to TensorFlow.
            So obj should be tensorflow.
        func_name_str: A string. The full name of the api (except 'tf.'). For example, the name of
            `tf.keras.losses.MeanSquaredError` should be 'keras.losses.MeanSquaredError'.

    Returns:
        A boolean, indicating if hijacking is successful.


    The targeted API can be either a function or a class (the type will be detected by this function).
    This function would replace the original api with the new decorated api we created. This is achieved
    in a fairly simple and straight-forward way. For the example above, we just set the attribute by calling
    `setattr(tf.keras.losses, 'MeanSquaredError', wrapped_func)`.
    """
    func_name_list = func_name_str.split('.')
    func_name = func_name_list[-1]

    # Get the module object and the api object.
    module_obj = obj
    if len(func_name_list) > 1:
        for module_name in func_name_list[:-1]:
            module_obj = getattr(module_obj, module_name)
    orig_func = getattr(module_obj, func_name)

    # Utilities.
    def is_class(x):
        return inspect.isclass(x)
    def is_callable(x):
        return callable(x)
    def is_built_in_or_extension_type(x):
        if is_class(x) and hasattr(x, '__dict__') and not '__module__' in x.__dict__:
            return True
        else:
            return False
    # Handle special cases of types.
    if is_built_in_or_extension_type(orig_func):
      return False
    if is_class(orig_func):
        if hasattr(orig_func, '__slots__'):
            return False
        wrapped_func = dump_signature_of_class(orig_func, func_name_str, obj_hint, output_dir=output_dir)
        setattr(module_obj, func_name, wrapped_func)
        return True
    else:
      if is_callable(orig_func):
        wrapped_func = dump_signature_of_function(orig_func, func_name_str, obj_hint, output_dir=output_dir)
        setattr(module_obj, func_name, wrapped_func)
        return True
      else:
        return False

def should_skip(api):

    skip_list = [
        'tf.keras.layers.Layer',
        'tf.compat.v1.keras.layers.Layer',
        'tf.Module',
        'tf.compat.v1.Module',
        'tf.compat.v1.flags.FLAGS',
        'tf.compat.v1.app.flags.EnumClassListSerializer',
        'tf.compat.v1.app.flags.EnumClassSerializer',
        'tf.compat.v1.flags.EnumClassListSerializer',
        'tf.compat.v1.flags.EnumClassSerializer',
        'tf.init_scope',
        'tf.TensorShape',
        'tf.Variable',
        'tf.compat.v1.Variable',
        'tf.ResourceVariable',
        'tf.Tensor',
        'tf.compat.v1.Tensor',
        'tf.compat.v1.flags.tf_decorator.make_decorator',
        'tf.compat.v1.flags.tf_decorator.tf_stack.extract_stack',
        'tf.compat.v1.flags.tf_decorator.unwrap',
        'tf.compat.v1.flags.tf_decorator.rewrap',
        'tf.compat.v1.app.flags.tf_decorator.make_decorator',
        'tf.compat.v1.app.flags.tf_decorator.rewrap',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack.CurrentModuleFilter',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack.FrameSummary',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackSummary',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackTraceFilter',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackTraceMapper',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack.StackTraceTransform',
        'tf.compat.v1.app.flags.tf_decorator.tf_stack.extract_stack',
        'tf.compat.v1.app.flags.tf_decorator.unwrap',

    ]
    skip_key_word = [
        'tf.compat.v1',
        'tf.debugging',
        'tf.distribute',
        'tf.errors',
        'tf.profiler',
        'tf.test',
        'tf.tpu',
        'tf.summary',
        'tpu',
        'TPU',
    ]
    
    if api.find('tf.') != 0:
        return True
    # Skip the current api if it's in the skip list.
    if api in skip_list:
        return True
    # Skip the current api if it has some keywords.
    for kw in skip_key_word:
        if kw in api:
            return True

import re, json
def hijack_all(output_dir, verbose=False):
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    success_list = []
    failed_list = []
    skip_list = []
    import os
    api_file = __file__.replace("hijack.py", "tf_valid_APIs_new.txt")
    with open(api_file, 'r') as fr:
        apis = fr.readlines()
    print('Number of total apis: ', len(apis)) 
    skip_apis = False
    cnt = 0

    # module_list = [tf, array_ops]
    # for obj in module_list:
    import sys
    module_members = inspect.getmembers(sys.modules[__name__], inspect.ismodule)

    f = open ('/home/nimashiri/.local/lib/python3.8/site-packages/tensorflow/instrumentation/tf_apis.json', "r")
    data = json.loads(f.read())
    for key, value in data.items():
        for v in value:
            api_name = key+'.'+v
            # print(api_name)
            try:
                result = next((v[1] for i, v in enumerate(module_members) if v[0] == key), None)
                x = repr(result)
                obj_hint = x.split('from')[0].split('module')[1]
                obj_hint = obj_hint.replace("'",'')
                obj_hint = obj_hint.replace(" ",'')
                hijack_api(result, v, obj_hint, output_dir)
            except:
                continue
    # for i, api in enumerate(apis):
    #     api = api.strip()
    #     if skip_apis:
    #         if should_skip(api):
    #             skip_list.append(api + "\n")
    #             continue

    #     hijack_api(clip_ops, api, output_dir)

   