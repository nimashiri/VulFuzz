import pymongo, os, re, subprocess, logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from csv import writer
logging.basicConfig(level = logging.INFO)

"""
MongoDB configurations
"""

DB = pymongo.MongoClient(host='localhost', port=27017)['TF']
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=10, connectTimeoutMS=300)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


"""
Constants
"""

QUERIED_APIS_ADDRESS = '/media/nimashiri/SSD1/FSE23_2/misc/torch_queried_apis.txt'



def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def get_unique_documents(dbname, new_db_name):
    new_db = pymongo.MongoClient(host="localhost", port=27017)[new_db_name]
    mydb = myclient[dbname]

    if not os.path.exists(QUERIED_APIS_ADDRESS):
        f1 = open(QUERIED_APIS_ADDRESS, 'a') 

    hist = read_txt(QUERIED_APIS_ADDRESS)

    
    for api_name in mydb.list_collection_names():
        if api_name not in hist:
            logging.info("Geting unique records for API: {0}".format(api_name))
            mycol = mydb[api_name]
            x = mycol.aggregate(
                [
                { "$group": { 
                    "_id": "$parameter:0", 
                    "doc": { "$first": "$$ROOT" }
                }},
                { "$replaceRoot": {
                    "newRoot": "$doc"
                }}
                ]
            )

            x = list(x)
            for item in x:
                new_db[api_name].insert_one(item)
            write_list_to_txt4(api_name, QUERIED_APIS_ADDRESS)
        else:
            logging.info('{0} already inserted!'.format(api_name))
        

def drop_database(dbname):
    myclient.drop_database(dbname)

def drop_document(dbname):
    mydb = myclient[dbname]
    for name in mydb.list_collection_names():
        print(name)
        mycol = mydb[name]
        mycol.delete_many({"source": "tests" })

def count_sources_per_api(dbname):
    
    mydb = myclient[dbname]
    counter = 0
    
    if not os.path.exists(QUERIED_APIS_ADDRESS):
        f1 = open(QUERIED_APIS_ADDRESS, 'a') 

    hist = read_txt(QUERIED_APIS_ADDRESS)

    for name in mydb.list_collection_names():
        if name not in hist:
            print("{}:{}".format(name, counter))
            write_list_to_txt4(name, QUERIED_APIS_ADDRESS)
            counter = counter + 1
            mycol = mydb[name]
            source_dict = {}
            for source in ['docs', 'tests', 'models']:
                source_dict[source] = mycol.count_documents({"source": source})

            for k,v in source_dict.items():
                if v != 0:
                    mydata = [name, k]
                    with open(f'/media/nimashiri/SSD1/FSE23_2/statistics/{dbname}_api_coverage.csv', 'a', newline='\n') as fd:
                        writer_object = writer(fd)
                        writer_object.writerow(mydata)

def count_all_apis(dbname):
    DB = pymongo.MongoClient(host='localhost', port=27017)[dbname]

    counter = 0
    for name in DB.list_collection_names():
        counter = counter + 1
    print(counter)

def main():

    '''
    Please put the database name you want to work on.
    '''
    db_name = "Torch"
    new_db_name = 'Torch-Unique'

    get_unique_documents(db_name, new_db_name)

if __name__ == '__main__':
    main()
    
