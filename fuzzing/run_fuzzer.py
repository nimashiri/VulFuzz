
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


def run_fuzzer():
    dbname = 'TF'
    mydb = myclient[dbname]
    check_connection()
    TFDatabase.database_config('localhost', 27017, 'TF')
    for api_ in mydb.list_collection_names():
        try:
            res = subprocess.run(["python3", "fuzzing_code.py", "TF", api_], shell=False, timeout=100)
        except subprocess.TimeoutExpired:
            print('')
        except Exception as e:
            print('')
        else:
            if res.returncode != 0:
                print('')

if __name__ == '__main__':
    run_fuzzer()