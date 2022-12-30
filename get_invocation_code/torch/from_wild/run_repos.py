import logging, re, os, subprocess

logging.basicConfig(level = logging.INFO)

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def has_test(data):
    test_files = []
    test_flag = False
    for f in data:
        if re.findall(r'\/tests\/', f) or re.findall(r'\/test\/', f) or re.findall(r'\/test.py', f):
            test_flag = True
            test_files.append(f)
    return test_files



def run_repos():
    repo_list = '/media/nimashiri/DATA/vsprojects/FSE23_2/get_invocation_code/torch/from_wild/tensorflow.txt'
    data = read_txt(repo_list)
    for repo in data:
        repo_l = repo.split('/')
        logging.info(repo)
        repo = "".join([repo,'.git'])

        if not os.path.exists('/media/nimashiri/DATA/vsprojects/FSE23_2/ml_repos_cloned/'+repo_l[4]):
            run_ = 'git clone '+repo+' /media/nimashiri/DATA/vsprojects/FSE23_2/ml_repos_cloned/'+repo_l[4]
            subprocess.call(run_, shell=True)
        dirs = getListOfFiles('/media/nimashiri/DATA/vsprojects/FSE23_2/ml_repos_cloned/'+repo_l[4])
        
        test_files = has_test(dirs)
        if test_files:
            write_list_to_txt4(repo, '/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/wild/tf_good_repos.txt')
        subprocess.call('rm -rf '+'/media/nimashiri/DATA/vsprojects/FSE23_2/ml_repos_cloned/'+repo_l[4], shell=True)

if __name__ == '__main__':
    subprocess.call('cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/wild/write_tools.py /home/nimashiri/.local/lib/python3.8/site-packages/torch/', shell=True)
    run_repos()