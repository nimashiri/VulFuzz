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
        # if re.findall(r'('+api_name_only+r'\()', row):
        #     # code = [row]
        #     row = "\n".join(row)
        # else:
        #     pass

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
        with open('/media/nimashiri/SSD1/FSE23_2/data/tf/tf_apis/corrupted_doc_example.csv', 'a', newline='\n') as fd:
            writer_object = writer(fd)
            writer_object.writerow(mydata)
    subprocess.call('rm -rf example.py', shell=True)

if __name__ == '__main__':
    hist_addr = '/media/nimashiri/SSD1/FSE23_2/get_invocation_code/tf/from_docs/hist.txt'
    
    if not os.path.exists(hist_addr):
        f1 = open(hist_addr, 'a') 

    hist = read_txt(hist_addr)

    # subprocess.call('cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_apis/write_tools.py /home/nimashiri/.local/lib/python3.8/site-packages/torch/', shell=True)
    
    data = pd.read_csv('/media/nimashiri/SSD1/FSE23_2/data/tf/tf_apis/tf_APIs_signatures.csv')
    for id_, row in data.iterrows():
        if isinstance(row['Example'], str):
            if row['API'] not in hist:
                _api_name = row['API'].split('(')[0]
                example = preprocess_examples(row['API'], row['Example'])
                if example:
                    write_list_to_txt4(_api_name, hist_addr)
                    #write_to_disc(example, '/media/nimashiri/SSD1/tf_api_examples/'+_api_name+'.py')
                    logging.info(f'{id_}/{len(data)} examples has been executed!')
                    run_example(row['API'], example)