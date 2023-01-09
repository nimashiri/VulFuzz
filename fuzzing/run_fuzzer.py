import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
import sys
import os
import traceback
from constants.enum import OracleType
from os.path import join
from utils.converter import str_to_bool
import tensorflow as tf

# from classes.tf_library import TFLibrary
# from classes.tf_api import TFAPI
from classes.database import TorchDatabase

# from classes.database import FDatabase
import subprocess
import re
from utils.printer import dump_data

logging.basicConfig(level=logging.INFO)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


def check_connection():
    client = MongoClient(
        "mongodb://localhost:27017/", serverSelectionTimeoutMS=10, connectTimeoutMS=300
    )

    try:
        info = client.server_info()

    except ServerSelectionTimeoutError:
        logging.info(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        )
        logging.info(
            "#### MongoDB Server is Down! I am trying initiating the server now. ####"
        )
        logging.info(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        )


def find_skip_list(api_):
    flag_ = True
    skip_list = [
        "python.autograph",
        "python.debug",
        "python.distribute",
        "python.eager",
        "python.framework",
        "python.grappler",
    ]
    if "tf." in api_:
        return False
    elif "torch." in api_:
        return True
    else:
        split_api = api_.split(".")
        target = ".".join([split_api[1], split_api[2]])
        if target in skip_list:
            flag_ = False
    return flag_


class InterpreterError(Exception):
    pass


def my_exec(cmd, globals=None, locals=None, description="source string"):
    existence_flag = False
    try:
        exec(cmd, globals, locals)
    except SyntaxError as err:
        error_class = err.__class__.__name__
        detail = err.args[0]
        if "SyntaxError" == error_class:
            existence_flag = True
        line_number = err.lineno
    except Exception as err:
        error_class = err.__class__.__name__
        detail = err.args[0]
        if "AttributeError" == error_class or "ModuleNotFoundError" == error_class:
            existence_flag = True
        cl, exc, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
    else:
        return existence_flag
    return existence_flag


def pre_run_check(api_):
    code = "import tensorflow as tf\n"
    if re.findall(r"(tensorflow\.python)", api_):
        part_from = ".".join(api_.split(".")[0:-2])
        code += f"from {part_from} import {api_.split('.')[-2]}\n"
        api_ = ".".join(api_.split(".")[-2:])
        flag = my_exec(code)

    else:
        code += api_
        flag = my_exec(code)
    return flag


def run_fuzzer():
    dbname = "TF"
    tool = "FreeFuzz"
    tf_output_dir = "/media/nimashiri/SSD/testing_results"

    if not os.path.exists(tf_output_dir):
        os.mkdir(tf_output_dir)

    mydb = myclient[dbname]
    TorchDatabase.database_config("localhost", 27017, dbname)
    config_name = "/media/nimashiri/SSD/FSE23_2/fuzzing/config/expr.conf"

    data = mydb.list_collection_names()
    for i, api_ in enumerate(data):
        # print("API {}/{}".format(i, len(data)))
        # api_ = 'tensorflow.python.ops.array_ops.batch_gather_nd'
        if not pre_run_check(api_):
            skip_flag = find_skip_list(api_)
            if skip_flag:
                try:
                    if tool == "orion":
                        res = subprocess.run(
                            [
                                "python3",
                                "/media/nimashiri/SSD/FSE23_2/fuzzing/orion_main.py",
                                "TF",
                                api_,
                                str(i),
                                tool,
                            ],
                            shell=False,
                            timeout=100,
                        )
                    elif tool == "FreeFuzz":
                        res = subprocess.run(
                            [
                                "python3",
                                "/media/nimashiri/SSD/FSE23_2/fuzzing/freefuzz_api_main.py",
                                config_name,
                                "tf",
                                api_,
                                str(i),
                                tool,
                            ],
                            shell=False,
                            timeout=100,
                        )
                    else:
                        print("No tool provided")
                except subprocess.TimeoutExpired:
                    dump_data(f"{api_}\n", join(tf_output_dir, "timeout.txt"), "a")
                except Exception as e:
                    dump_data(
                        f"{api_}\n  {e}\n", join(tf_output_dir, "runerror.txt"), "a"
                    )
                else:
                    if res.returncode != 0:
                        dump_data(f"{api_}\n", join(tf_output_dir, "runcrash.txt"), "a")
            else:
                print("API Skipped!")
        else:
            print("This module does not exist in tensorflow")


if __name__ == "__main__":
    run_fuzzer()
