import pymongo

DB = pymongo.MongoClient(host='localhost', port=27017)['Torch']

counter = 0
for name in DB.list_collection_names():
    counter = counter + 1

from csv import writer





def getstat():
    memoy = []

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Torch"]
    for name in mydb.list_collection_names():
        print(name)
        mycol = mydb[name]
        for doc in mycol.find():
            if doc['source'] == 'models':
                mydata = [name, doc['source']]
                with open('/media/nimashiri/DATA/vsprojects/FSE23_2/stat.csv', 'a', newline='\n') as fd:
                    writer_object = writer(fd)
                    writer_object.writerow(mydata)
                break

def countall():
    DB = pymongo.MongoClient(host='localhost', port=27017)['Torch']

    counter = 0
    for name in DB.list_collection_names():
        counter = counter + 1
    print(counter)

if __name__ == '__main__':
    countall()