import pandas as pd
data = pd.read_csv('/media/nimashiri/DATA/vsprojects/FSE23_2/data/torch/torch_apis/torch_APIs_signatures.csv')
data = data.drop_duplicates('API')
print(data.shape)
