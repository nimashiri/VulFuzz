import pandas as pd
import numpy as np
import re, codecs
import subprocess
import logging
from csv import writer
import os
logging.basicConfig(level = logging.INFO)


def write_to_disc(filecontent, target_path):
    with codecs.open(target_path, 'w') as f_method:
        for line in filecontent:
            f_method.write("%s\n" % line)
        f_method.close()

def preprocess_examples(row):
    ex_split = row.split('\n')
    new_ex = []
    for j, line in enumerate(ex_split):
        if line and line[0] != '#':
            if line and line[0] == '>':
                new_ex.append(line)
            elif line and re.findall(r'(\>\>\>)', line) and line[0] != '>':
                sub_split = line.split('>>>')
                sub_split[-1] =  sub_split[-1].lstrip()
                new_ex.append(sub_split[-1])
            elif re.findall(r'(\.\.\.)' , line):
                line = line.replace('... ', '')
                new_ex[-1] = "".join([new_ex[-1], line])
    final_ex = []
    for line in new_ex:
        line = line.replace('>>> ', '')
        final_ex.append(line)
    final_ex.insert(0, 'import torch')
    final_ex.insert(0, 'import numpy')
    final_ex.insert(0, 'import numpy as np')
    # final_ex = "\n".join(final_ex)
    return final_ex

def run_example(api_, ex_doc, data):
    write_to_disc(ex_doc, 'example.py')
    try:
        result = subprocess.run(['python3', 'example.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(e)
    if result.stderr:
        mydata = [api_, ex_doc , result.stderr]
        with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/x.csv', 'a', newline='\n') as fd:
            writer_object = writer(fd)
            writer_object.writerow(mydata)
    subprocess.call('rm -rf example.py', shell=True)

def run_example_v2():
    f_path = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/x.csv'
    # all_files = os.listdir(f_path)
    data = pd.read_csv(f_path, sep=',', encoding='utf-8')
    for idx, row in data.iterrows():
        print(row['Path'])
        try:
            result = subprocess.run(['python3', row['Path']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            print(e)
        if result.stderr:
            mydata = [row['Path'], result.stderr]
            with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/x2.csv', 'a', newline='\n') as fd:
                writer_object = writer(fd)
                writer_object.writerow(mydata)
        # subprocess.call('rm -rf example.py', shell=True)

if __name__ == '__main__':
    run_example_v2()
    # subprocess.call('cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/write_tools.py /home/nimashiri/.local/lib/python3.8/site-packages/torch/', shell=True)

    # data = pd.read_csv('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/torch_APIs_signatures.csv')
    # for id_, row in data.iterrows():
    #     logging.info(f'{id_}/{len(data)} examples has been executed!')
    #     examples = [row['Example1'], row['Example2']]
    #     for id_2, ex in enumerate(examples):
    #         if  isinstance(ex, str):
    #             example = preprocess_examples(ex)
    #             write_to_disc(example, f'/media/nimashiri/SSD1/torch_api_examples/{id_}{id_2}.py')
    #             # run_example(row['API'], ex, row['Bug'])





