import pandas as pd
import torch
from csv import writer
# addr = '/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/torch_apis.csv'
# data = pd.read_csv(addr, sep=',')
# d = data.drop_duplicates('API')
# d.to_csv('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/torch_apis_no_dup.csv', sep=',', encoding='utf-8')

extracted_df = '/media/nimashiri/DATA/vsprojects/FSE23_2/statistics/Torch-VulFuzz_all_apis.csv'
doc_df = '/media/nimashiri/DATA/vsprojects/FSE23_2/statistics/Torch-VulFuzz_doc_all.csv'
data_e = pd.read_csv(extracted_df, sep=',')
data_doc = pd.read_csv(doc_df, sep=',')

extracted_data = list(data_e['API'])
document_data = list(data_doc['API'])


union = set(document_data).union(extracted_data)
inter = set(document_data) & set(extracted_data)
res = union - inter
res = list(res)
for item in res:
    with open(f'/media/nimashiri/DATA/vsprojects/FSE23_2/statistics/torch_not_discovered.csv', 'a', newline='\n') as fd:
        writer_object = writer(fd)
        writer_object.writerow([item])