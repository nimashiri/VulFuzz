import pymongo, os

DB = pymongo.MongoClient(host='localhost', port=27017)['Torch-VulFuzz']

counter = 0
for name in DB.list_collection_names():
    counter = counter + 1

from csv import writer

misc_addr = '/media/nimashiri/DATA/vsprojects/FSE23_2/misc/tf_queried_apis.txt'

def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def drop_database(dbname):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    myclient.drop_database(dbname)

def drop_document(dbname):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[dbname]
    for name in mydb.list_collection_names():
        print(name)
        mycol = mydb[name]
        mycol.delete_many({"source": "tests" })

def retrieve_source(dbname):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[dbname]
    counter = 0
    
    if not os.path.exists(misc_addr):
        f1 = open(misc_addr, 'a') 

    hist = read_txt(misc_addr)

    for name in mydb.list_collection_names():
        # with open(f'/media/nimashiri/DATA/vsprojects/FSE23_2/statistics/{dbname}_all_apis.csv', 'a', newline='\n') as fd:
        #     writer_object = writer(fd)
        #     writer_object.writerow([name])
        if name not in hist:
            print("{}:{}".format(name, counter))
            write_list_to_txt4(name, misc_addr)
            counter = counter + 1
            mycol = mydb[name]
            source_dict = {}
            for source in ['docs', 'tests', 'models']:
                source_dict[source] = mycol.count_documents({"source": source})

            for k,v in source_dict.items():
                if v != 0:
                    mydata = [name, k]
                    with open(f'/media/nimashiri/DATA/vsprojects/FSE23_2/statistics/{dbname}_api_coverage.csv', 'a', newline='\n') as fd:
                        writer_object = writer(fd)
                        writer_object.writerow(mydata)

def countall(dbname):
    DB = pymongo.MongoClient(host='localhost', port=27017)[dbname]

    counter = 0
    for name in DB.list_collection_names():
        counter = counter + 1
    print(counter)


if __name__ == '__main__':
    countall('TF')
