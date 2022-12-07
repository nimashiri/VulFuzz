import subprocess, os
from multiprocessing import Pool
import multiprocessing, threading
from threading import Thread
import logging, re

logging.basicConfig(level = logging.INFO)

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')

class KillableThread(Thread):
    def __init__(self, sleep_interval, input_addr):
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self.input_addr = input_addr

    def run(self):
        while True:
            process_prerun(self.input_addr)

            # If no kill signal is set, sleep for the interval,
            # If kill signal comes in while sleeping, immediately
            #  wake up and handle
            is_killed = self._kill.wait(self._interval)
            if is_killed:
                break

        print("Killing Thread")

    def kill(self):
        self._kill.set()

def process_prerun(input_addr):
    print("Executed:#: {}.".format(input_addr))
    command = 'python3 '+input_addr
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

class RunTestFiles():
    def __init__(self, test_files) -> None:
        self.test_files = test_files

    def pre_run_test_files(self):
        self.p = multiprocessing.Pool(2)
        m = multiprocessing.Manager()
        self.event = m.Event()
        status = self.p.apply_async(process_prerun, (self.test_files, ))
        print('')

def run_tf_tests(data):
    import os

    _path_clean_tests = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_test_files/history.txt'
    _path_corrupted_tests = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_test_files/corrupted.txt'


    mode = 'a' if os.path.exists(_path_clean_tests) else 'w'
    f1 = open(_path_clean_tests, mode=mode)

    mode = 'a' if os.path.exists(_path_corrupted_tests) else 'w'
    f2 = open(_path_corrupted_tests, mode=mode)


    hist = read_txt(_path_clean_tests)
    corr = read_txt(_path_corrupted_tests)

    for i, t in enumerate(data):
        if t not in hist and t not in corr:
            write_list_to_txt4(t, _path_clean_tests)
            logging.info('###############################################')
            logging.info(f'Current test is: {t}: {i}/{len(data)} test files has been executed!')
            logging.info('###############################################')

            status = subprocess.run(['nc', '-zvv', 'localhost', '27017'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if re.findall(r'(succeeded!)', status.stderr):
                try:
                    subprocess.run(['python3', t])
                except Exception as e:
                    print(e)
            else:
                subprocess.call('rm -rf /media/nimashiri/DATA/mongodata/mongod.lock', shell=True)
                subprocess.run(['mongod', '--dbpath', '/media/nimashiri/DATA/mongodata/', '--logpath', '/media/nimashiri/DATA/mongolog/mongo.log', '--fork'])

        subprocess.call('find . -name "*.pb" -type f -delete', shell=True)
        subprocess.call('find . -name "*.ckpt" -type f -delete', shell=True)
        subprocess.call('find . -name "*.meta" -type f -delete', shell=True)
        subprocess.call('find . -name "*.saver" -type f -delete', shell=True)

if __name__ == '__main__':
    # subprocess.call('cp -r /media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_test_files/write_tools.py /home/nimashiri/.local/lib/python3.8/site-packages/tensorflow/instrumentation/', shell=True)

    tf_tests = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/tf/tf_test_files/tf_tests_v2.4.0.txt'
    data = read_txt(tf_tests)
    run_tf_tests(data)
    #obj_ = RunTestFiles(data)
    #obj_.pre_run_test_files()