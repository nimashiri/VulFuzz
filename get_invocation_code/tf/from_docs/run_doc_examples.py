import pandas as pd
import numpy as np
import re, codecs, os
import subprocess
import logging
from csv import writer
logging.basicConfig(level = logging.INFO)

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data
    
def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

def write_to_disc(filecontent, target_path):
    with codecs.open(target_path, 'w') as f_method:
        for line in filecontent:
            f_method.write("%s\n" % line)
        f_method.close()

def preprocess_examples(api, row):
    api_name_only = api.split('(')[0]
    api_name_only = api_name_only.split('.')[-1]
    if re.findall(r'('+api_name_only+r')', row) or re.findall(r'(tf.'+api_name_only+')', row):
        if re.findall(r'('+api_name_only+r'\()', row):
            code = ['from tensorflow import '+ api_name_only, row]
            row = "\n".join(code)
        else:
            pass

        ex_split = row.split('\n')
        new_ex = []
        for line in ex_split:
            if re.findall(r'(\<)', line):
                new_ex.append(line)
            if not re.findall(r'(\#)', line) or not re.findall(r'(\#\s)', line):
                new_ex.append(line)
        
        new_ex.insert(0, 'import tensorflow as tf')
        new_ex.insert(0, 'import numpy as np')
        new_ex.insert(0, 'import pandas as pd')
        return new_ex
    else:
        return False

def run_example(api_, data):
    write_to_disc(data, 'example.py')
    try:
        result = subprocess.run(['python3', 'example.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(e)
    if result.stderr:
        mydata = [api_, result.stderr]
        with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_apis/corrupted_doc_example.csv', 'a', newline='\n') as fd:
            writer_object = writer(fd)
            writer_object.writerow(mydata)
    subprocess.call('rm -rf example.py', shell=True)

if __name__ == '__main__':
    misc_addr = '/media/nimashiri/SSD1/FSE23_2/get_invocation_code/tf/from_docs/hist.txt'
    
    if not os.path.exists(misc_addr):
        f1 = open(misc_addr, 'a') 

    hist = read_txt(misc_addr)

    # subprocess.call('cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_apis/write_tools.py /home/nimashiri/.local/lib/python3.8/site-packages/torch/', shell=True)
    
    data = pd.read_csv('/media/nimashiri/SSD1/FSE23_2/data/tf/tf_apis/api_with_doc_example.csv')
    data = data.drop_duplicates('API')
    for id_, row in data.iterrows():
        d = row['Examples'].split('\n')
        api_splt = row['API'].split('(')
        if api_splt[0] not in hist:
            write_list_to_txt4(api_splt[0], misc_addr)
            write_to_disc(d, f'/media/nimashiri/SSD1/FSE23_2/tensorflow_API_examples/{api_splt[0]}{id_}.py')
        # if isinstance(row['Example'], str):
            
        #     example = preprocess_examples(row['API'], row['Example'])
        #     if example:
        #         example = "\n".join(example)
        #         mydata = [row['API'], example]
        #         with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_apis/api_with_doc_example.csv', 'a', newline='\n') as fd:
        #             writer_object = writer(fd)
        #             writer_object.writerow(mydata)
        #         logging.info(f'{id_}/{len(data)} examples has been executed!')
        #         logging.info(row['API'])
                #run_example(row['API'],example)