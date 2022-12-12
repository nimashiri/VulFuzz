
import json, codecs, subprocess, os, ast

skip_list = [
    '__init__.py',
    '__init__',
    'profiler',
    '__pycache__',
    'compat',
    'compiler',
    'data',
    'debug',
    'dis',
    'dlpack',
    'kernel_tests',
    'lib',
    'tools',
    'tpu'
]

def read_ast(file_to_be_processed):
    with open(file_to_be_processed, "r") as source:
        ast_tree = ast.parse(source.read())
    return ast_tree

def get_doc_string_examples(ast_tree):
    f_objects = [x for x in ast.walk(ast_tree) if isinstance(x, ast.FunctionDef) or isinstance(x, ast.ClassDef)]
    for f in f_objects:
        function = f.body[0]
        #ast.dump(function.args)
        # print(ast.get_docstring(f))

def write_list_to_txt(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

def write_to_disc(filecontent, target_path):
    with codecs.open(target_path, 'w') as f_method:
        for line in filecontent:
            f_method.write("%s\n" % line)
        f_method.close()

def save_objects(stmt):
    objects_path = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/import_objects/'+stmt+'.py'

    text_code = f'''\
from tensorflow.python.client import timeline
import pickle
with open('/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/import_objects/{stmt}', 'wb') as outp:  # Overwrites any existing file.
    pickle.dump(timeline, outp, pickle.HIGHEST_PROTOCOL)
    '''    
    write_to_disc([text_code], objects_path)
    subprocess.run(['python3 /media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/import_objects/'+stmt+'.py'], shell=True)
    subprocess.call('rm -rf '+stmt+'.py', shell=True)

def get_parent_module(file_addr):
    file_addr = file_addr.replace('.py', '')
    module_split = file_addr.split('site-packages')
    sub_split = module_split[1].split('/')
    x = ".".join(sub_split[1:-1])
    import_stmt = 'from '+x+' import '+sub_split[-1]
    return import_stmt, sub_split[-1]

def get_ast_functions(ast_tree):
    f_names = []
    filtered = []
    for x in ast.walk(ast_tree):
        if isinstance(x, ast.FunctionDef):
            if x.args:
                f_names.append(x.name)
            else:
                filtered.append(x.name)

        if isinstance(x, ast.ClassDef):
            if isinstance(x.bases[0], ast.Call):
                #if x.bases[0].args:
                f_names.append(x.name)
            else:
                filtered.append(x.name)
    return f_names, filtered

def get_tf_apis():
    dict_obj = {}
    counter = 0
    for root, dirs, files in os.walk('/home/nimashiri/.local/lib/python3.8/site-packages/tensorflow/python/'):
        for module in dirs:
            if module not in skip_list:
                current_module = os.path.join(root, module)
                current_files = os.listdir(current_module)
                for f in current_files:
                    if f not in skip_list:
                        
                        file_to_be_processed = os.path.join(current_module, f)
                        if os.path.isfile(file_to_be_processed):
                            try:
                                ast_tree = read_ast(file_to_be_processed)
                                f_names, filtered = get_ast_functions(ast_tree)
                                
                                if f_names:
                                    # get_doc_string_examples(ast_tree) 
                                    import_stmt, module_name = get_parent_module(file_to_be_processed)
                                    # save_objects(module_name)
                                    write_list_to_txt(import_stmt, '/media/nimashiri/SSD1/FSE23_2/data/tf/tf_internal_imports.txt')

                                    dict_obj[module_name] = []
                                    for module in f_names:
                                        if module not in skip_list:
                                            counter = counter + 1
                                            dict_obj[module_name].append(module)
                            except Exception as e:
                                print(e)

    
    with open('/media/nimashiri/SSD1/FSE23_2/data/tf/tf_apis/tf_apis.json', 'w') as fp:
        json.dump(dict_obj, fp, indent=4)

if __name__ == '__main__':
    get_tf_apis()

