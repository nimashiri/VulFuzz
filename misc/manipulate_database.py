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


def count_value_space(dbname):
    source_dict = {'docs': 0, 'tests': 0, 'models': 0}
    mydb = myclient[dbname]
    for api_name in mydb.list_collection_names():
        logging.info(api_name)
        mycol = mydb[api_name]
        for source in ['docs', 'tests', 'models']:
            source_dict[source] += mycol.count_documents({"source": source})
            print(source_dict)

'''
This function returns a new database in which all documents are distinct.
The distinction is based the first parameter of each the documents in each collection.
'''
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

'''
Delete all documents in a collection based on the field source.
'''
def drop_document(dbname):
    mydb = myclient[dbname]
    for name in mydb.list_collection_names():
        print(name)
        mycol = mydb[name]
        mycol.delete_many({"source": "tests" })

'''
Count the number of APIs based on the source they have been collected. 
'''

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

def get_all_databases():
    print(myclient.list_database_names())

def main():
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=10, connectTimeoutMS=300)

    try:
        info = client.server_info()
                
    except ServerSelectionTimeoutError:
        logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        logging.info('#### MongoDB Server is Down! I am trying initiating the server now. ####')
        logging.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        subprocess.call('rm -rf /media/nimashiri/DATA/mongodata/mongod.lock', shell=True)
        subprocess.run(['mongod', '--dbpath', '/media/nimashiri/DATA/mongodata/', '--logpath', '/media/nimashiri/DATA/mongolog/mongo.log', '--fork'])

    db_name = "Torch-VulFuzz"

    get_all_databases()
    count_value_space(db_name)

if __name__ == '__main__':
    main()
    
