import pandas as pd
import numpy as np
import re, codecs
import subprocess
import logging
from csv import writer
logging.basicConfig(level = logging.INFO)


def write_to_disc(filecontent, target_path):
    with codecs.open(target_path, 'w') as f_method:
        for line in filecontent:
            f_method.write("%s\n" % line)
        f_method.close()

def preprocess_examples(row):
    ex_split = row.split('\n')
    new_ex = []
    for line in ex_split:
        if re.findall(r'(\>\>\>)', line):
            new_ex.append(line)
    final_ex = []
    for line in new_ex:
        line = line.replace('>>> ', '')
        final_ex.append(line)
    final_ex.insert(0, 'import torch')
    # final_ex = "\n".join(final_ex)
    return final_ex

def run_example(api_, data):
    write_to_disc(data, 'example.py')
    try:
        result = subprocess.run(['python3', 'example.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(e)
    if result.stderr:
        mydata = [api_, result.stderr]
        with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/corrupted_doc_example.csv', 'a', newline='\n') as fd:
            writer_object = writer(fd)
            writer_object.writerow(mydata)
    subprocess.call('rm -rf example.py', shell=True)

if __name__ == '__main__':

    subprocess.call('cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/write_tools.py /home/nimashiri/.local/lib/python3.8/site-packages/torch/', shell=True)

    data = pd.read_csv('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/pytorch_APIs_signatures.csv')
    for id_, row in data.iterrows():
        logging.info(f'{id_}/{len(data)} examples has been executed!')
        if isinstance(row['Example'], str):
            example = preprocess_examples(row['Example'])
            run_example(row['API'],example)