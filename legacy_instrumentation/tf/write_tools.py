import pymongo

"""
You should configure the database
"""
tf_db = pymongo.MongoClient(host="localhost", port=27017)["TF"]

def write_fn(obj_hint, func_name, params, input_signature, output_signature):
    params = dict(params)
    out_fname = obj_hint+"." + func_name
    if input_signature != None:
        params['input_signature'] = input_signature
    params['output_signature'] = output_signature
    params['source'] = 'tests'
    tf_db[out_fname].insert_one(params)
