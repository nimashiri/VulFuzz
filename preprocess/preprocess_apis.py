import pandas as pd
import re
from csv import writer
import re, subprocess, codecs
from csv import writer
import logging, xmltodict
import ast
from pprint import pprint

logging.basicConfig(level = logging.INFO)

def parse_recursive_api_tree(_tree):
    try:
        if _tree.args or _tree.keywords:
            return True
        else:
            return False
    except Exception as e:
        if _tree.attr:
            return parse_recursive_api_tree(_tree.value)
        else:
            return False

def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

def write_to_disc_tf(filecontent, target_path):
    with codecs.open(target_path, 'w') as f_method:
        f_method.write("%s\n" % filecontent)
        f_method.close()

def write_to_disc(filecontent, target_path):
    with codecs.open(target_path, 'w') as f_method:
        for line in filecontent:
            f_method.write("%s\n" % line)
        f_method.close()

def find_valid_apis_torch(data):
    for k, v in data.iterrows():
        if re.findall(r'\(([^()]+)\)', v['API']):
            api_ = re.findall(r'.+?(?=\()', v['API'])[0]
            api_ =  api_.replace(' ','')
            api_  = api_ + '()'

            if re.findall(r'(class)', api_):
                api_ = re.sub('(class)', '', api_)
                d = ['import torch', api_]
            else:
                if re.findall(r'(Tensor)', api_):
                    api_ = 'torch.'+api_
                    d = ['import torch', api_]
                elif re.findall(r'torch.', api_):
                    d = ['import torch', api_]
                else:
                    api_ = 'torch.'+api_
                    d = ['import torch', api_]
        
            write_to_disc(d, 'example.py')
            try:
                result = subprocess.run(['python3', 'example.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                subprocess.call('rm -rf example.py', shell=True)
            except Exception as e:
                print(e)

            d = "\n".join(d)
            if re.findall(r'(missing)', result.stderr):
                logging.info('valid api')
                mydata = [api_, 'valid api', d]
            elif re.findall(r'(needs an argument)', result.stderr):
                logging.info('valid api')
                mydata = [api_, 'valid api', d]
            elif re.findall(r'(Expected)', result.stderr) or re.findall(r'(expects)', result.stderr):
                logging.info('valid api')
                mydata = [api_, 'valid api', d]
            elif re.findall(r'(ValueError:)', result.stderr):
                logging.info('valid api')
                mydata = [api_, 'valid api', d]
            elif re.findall(r'(received an invalid combination of arguments)', result.stderr):
                logging.info('valid api')
                mydata = [api_, 'valid api', d]
            elif re.findall(r'takes exactly', result.stderr):
                logging.info('valid api')
                mydata = [api_, 'valid api', d]
            elif re.findall(r'(AttributeError\:\smodule\s\'torch\'\shas\sno\sattribute)', result.stderr):
                logging.info('invalid api')
                mydata = [api_, 'AttributeError: module torch has no attribute', d]
            else:
                logging.info('Unknown')
                mydata = [api_, result.stderr, d]
        else:
            mydata = [v['API'], 'No input params', 'No example']
        
        with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/APIs_validation_status.csv', 'a', newline='\n') as fd:
            writer_object = writer(fd)
            writer_object.writerow(mydata)

def get_torch_apis_raw_symbols_v2(data):
    for k,v in data.iterrows():
        if v['Status'] == 'valid api':
            v_split = v['API'].split('.')
            if len(v_split) == 2:
                symbol_part = re.findall(r'.+?(?=\()', v['API'])[0]
                symbol_part = symbol_part.replace('torch.','')
                mydata = [symbol_part, 'function']
            else:
                symbol_part = re.findall(r'.+?(?=\()', v['API'])[0]
                symbol_part = symbol_part.replace('torch.','')
                mydata = [symbol_part, 'class']

        with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/torch_apis.csv', mode='a', newline='\n') as fd:
            writer_object = writer(fd)
            writer_object.writerow(mydata)

    subprocess.call('chmod +w /media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/torch_apis.csv', shell=True)
    subprocess.call('echo "nima1370" | sudo cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/torch_apis.csv /home/nimashiri/.local/lib/python3.8/site-packages/torch', shell=True)     
    

def find_valid_apis_tf(data):
    for k, v in data.iterrows():
        
        api_ = re.findall(r'.+?(?=\()', v['API'])[0]        
        api_ =  api_.replace(' ','')
        api_no_sig = api_
        api_  = api_ + '()'
        logging.info(api_)
        v['API'] = v['API'].replace('-> str', '')
        d = ['import tensorflow as tf', v['API']]
        d = "\n".join(d)

        write_to_disc_tf(d, 'example.py')
        
        try:
            with open("example.py", "r") as source:
                ast_tree = ast.parse(source.read())
   
            has_api = parse_recursive_api_tree(ast_tree.body[1].value)

            if has_api:
                write_list_to_txt4(api_no_sig,'/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_apis/tf_valid_APIs.txt')
                # d = ['import tensorflow as tf', api_]

                # write_to_disc(d, 'example.py')
                # try:
                #     result = subprocess.run(['python3', 'example.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                #     subprocess.call('rm -rf example.py', shell=True)
                # except Exception as e:
                #     print(e)

                # d = "\n".join(d)

                # if re.findall(r'(Missing required positional argument)', result.stderr):
                #     mydata = [api_no_sig, 'Missing required positional argument', d]
                # else:
                #     mydata = [api_no_sig, result.stderr, d]
            else:
                mydata = [v['API'], 'No input params', 'No example']

                with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_apis/filtered_apis.csv', 'a', newline='\n') as fd:
                    writer_object = writer(fd)
                    writer_object.writerow(mydata)
                
        except Exception as e:
            mydata = [v['API'], e, 'No example']
            with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_apis/filtered_apis.csv', 'a', newline='\n') as fd:
                writer_object = writer(fd)
                writer_object.writerow(mydata)

def find_valid_apis_mxnet(data):
    cls_flag = False
    for k, v in data.iterrows():

        if re.findall(r'(class\smxn)', v['API']):
            cls_flag = True

        v['API'] = v['API'].replace('\nclass ', '')
        v['API'] = v['API'].replace('[source]', '')
        v['API'] = v['API'].replace('Â¶', '')
        
        
        d = ['import mxnet', v['API']]
        d = "\n".join(d)

        write_to_disc_tf(d, 'example.py')
        
        try:
            with open("example.py", "r") as source:
                ast_tree = ast.parse(source.read())
   
            has_api = parse_recursive_api_tree(ast_tree.body[1].value)

            if has_api:
                if cls_flag:
                    mydata = [v['API'].split('(')[0].split('.')[-1], 'class']
                else:
                    mydata = [v['API'].split('(')[0].split('.')[-1], 'function']
                with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/mxnet/mxnet_apis/mxnet_valid_apis.csv', mode='a', newline='\n') as fd:
                    writer_object = writer(fd)
                    writer_object.writerow(mydata)
            else:
                mydata = [v['API'], 'No input params', 'No example']
                with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/mxnet/mxnet_apis/mxnet_invalid_apis.csv', mode='a', newline='\n') as fd:
                    writer_object = writer(fd)
                    writer_object.writerow(mydata)  
        
        except:
            continue
        
        cls_flag = False

def get_apis_raw_symbols(data):
    c = 0
    for k,v in data.iterrows():
        v['API'] = v['API'].replace('\n','')
              
        if re.findall(r'\(([^()]+)\)', v['API']):
            symbol_part = re.findall(r'.+?(?=\()', v['API'])[0]
            symbol_part =  symbol_part.replace(' ','')
            
            if re.findall(r'(class)', symbol_part):
                symbol_part = re.sub('(class)', '', symbol_part)
                symbol_part = symbol_part.replace('torch.','')
                mydata = [symbol_part, 'class']
            else:
                symbol_part = symbol_part.replace('torch.','')
                mydata = [symbol_part, 'function']

            with open('data/torch/torch_apis/torch_apis.csv', mode='a', newline='\n') as fd:
                writer_object = writer(fd)
                writer_object.writerow(mydata)                

if __name__ == '__main__':
    lib_name = 'torch'
    data = pd.read_csv(f'/media/nimashiri/DATA/vsprojects/FSE23_2/data/{lib_name}/{lib_name}_apis/APIs_validation_status.csv')
    get_torch_apis_raw_symbols_v2(data)
    
    
    # if lib_name == 'torch':
    #     find_valid_apis_torch(data)
    # elif lib_name == 'tf':
    #     find_valid_apis_tf(data)
    # else:
    #     find_valid_apis_mxnet(data)
