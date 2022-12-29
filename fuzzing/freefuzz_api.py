import sys
from constants.enum import OracleType
import configparser
from os.path import join
from utils.converter import str_to_bool


def make_api_name_unique(api):
    api_split = api.split('tensorflow')
    new_api_name = 'tensorflow'+api_split[-1]
    return new_api_name


if __name__ == "__main__":
    config_name = sys.argv[1]
    library = sys.argv[2]
    api_name = sys.argv[3]

    freefuzz_cfg = configparser.ConfigParser()
    freefuzz_cfg.read(join(__file__.replace(
        "freefuzz_api.py", "config"), config_name))

    # database configuration
    mongo_cfg = freefuzz_cfg["mongodb"]
    host = mongo_cfg["host"]
    port = int(mongo_cfg["port"])

    # oracle configuration
    oracle_cfg = freefuzz_cfg["oracle"]
    crash_oracle = str_to_bool(oracle_cfg["enable_crash"])
    cuda_oracle = str_to_bool(oracle_cfg["enable_cuda"])
    precision_oracle = str_to_bool(oracle_cfg["enable_precision"])

    diff_bound = float(oracle_cfg["float_difference_bound"])
    time_bound = float(oracle_cfg["max_time_bound"])
    time_thresold = float(oracle_cfg["time_thresold"])

    # output configuration
    output_cfg = freefuzz_cfg["output"]
    torch_output_dir = output_cfg["torch_output"]
    tf_output_dir = output_cfg["tf_output"]

    # mutation configuration
    mutation_cfg = freefuzz_cfg["mutation"]
    enable_value = str_to_bool(mutation_cfg["enable_value_mutation"])
    enable_type = str_to_bool(mutation_cfg["enable_type_mutation"])
    enable_db = str_to_bool(mutation_cfg["enable_db_mutation"])
    each_api_run_times = int(mutation_cfg["each_api_run_times"])

    if library.lower() in ["pytorch", "torch"]:
        import torch
        from classes.torch_library import TorchLibrary
        from classes.torch_api import TorchAPI
        from classes.database import TorchDatabase

        TorchDatabase.database_config(host, port, mongo_cfg["torch_database"])

        if cuda_oracle and not torch.cuda.is_available():
            print("YOUR LOCAL DOES NOT SUPPORT CUDA")
            cuda_oracle = False
        # Pytorch TEST
        MyTorch = TorchLibrary(torch_output_dir, diff_bound, time_bound,
                               time_thresold)
        for _ in range(each_api_run_times):
            api = TorchAPI(api_name)
            api.mutate(enable_value, enable_type, enable_db)
            if crash_oracle:
                MyTorch.test_with_oracle(api, OracleType.CRASH)
            if cuda_oracle:
                MyTorch.test_with_oracle(api, OracleType.CUDA)
            if precision_oracle:
                MyTorch.test_with_oracle(api, OracleType.PRECISION)
    elif library.lower() in ["tensorflow", "tf"]:
        import tensorflow as tf
        from classes.tf_library import TFLibrary
        from classes.tf_api import TFAPI
        from classes.database import TFDatabase

        TFDatabase.database_config(host, port, mongo_cfg["tf_database"])
        if cuda_oracle and not tf.test.is_gpu_available():
            print("YOUR LOCAL DOES NOT SUPPORT CUDA")
            cuda_oracle = False

        MyTF = TFLibrary(tf_output_dir, diff_bound, time_bound,
                         time_thresold)
        print("########################################################################################################################")
        print("The current API under test: ###{0}###. Mutating the parameter ###### using the rule #####".format(
            api_name))
        print("########################################################################################################################")

        api_keywords = api_name.split('.')
        if api_keywords.count('tensorflow') > 1:
            api_name = make_api_name_unique(api_name)

        for _ in range(each_api_run_times):

            api = TFAPI(api_name)
            api.args.pop('source')
            if '_id' in api.args:
                api.args.pop('_id')

            api.mutate(enable_value, enable_type, enable_db)
            if crash_oracle:
                MyTF.test_with_oracle(api, OracleType.CRASH)
                api.api = sys.argv[3]
            if cuda_oracle:
                MyTF.test_with_oracle(api, OracleType.CUDA)
