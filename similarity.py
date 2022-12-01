
import pandas as pd
from csv import writer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

model = SentenceTransformer('bert-base-nli-mean-tokens', device='cuda')


def make_api_raw():
    data = pd.read_csv('scrapers/tf_APIs_signature3.csv', sep=',', encoding='utf-8')

    x = []
    for i in range(len(data)):
        api_ = []
        for c in data.iloc[i, 0]:
            if c == '(':
                break
            else:
                api_.append(c)
        api_ = "".join(api_)
        
        with open('scrapers/d.csv', 'a', newline='\n') as fd:
            writer_object = writer(fd)
            writer_object.writerow([api_, data.iloc[i, 0], data.iloc[i, 1]])

def match_source_target():
    target_APIs = pd.read_csv('scrapers/d.csv', sep=',', encoding='utf-8')
    source_APIs = pd.read_csv('scrapers/securityData.csv', sep=',', encoding='utf-8')
    
    for s in source_APIs['API']:
        i=target_APIs[target_APIs['Raw_API']==s]
        if not i.empty:
            with open('scrapers/final_data.csv', 'a', newline='\n') as fd:
                writer_object = writer(fd)
                writer_object.writerow([i.iloc[0, 1], i.iloc[0, 0]])

def calculate_similarity():
    target_APIs = pd.read_csv('scrapers/d.csv', sep=',', encoding='utf-8')
    source_APIs = pd.read_csv('scrapers/final_data.csv', sep=',', encoding='utf-8')

    # if not os.path.isfile('model/t_encode.pkl'):
    #     os.mkdir('model')
    #     t_encode = model.encode(f_api)
    #     with open('model/t_encode.pkl','wb') as f:
    #         pickle.dump(t_encode, f)
    # else:
    #     with open('model/t_encode.pkl','rb') as f:
    #         t_encode = pickle.load(f)     

    for j in range(len(source_APIs)):
        for i in range(len(target_APIs)):
            print('Source/Target: {}/{}'.format(j, i))
            s_encode = model.encode(source_APIs.iloc[j, 0])
            t_encode = model.encode(target_APIs.iloc[i, 1])

            x = cosine_similarity([s_encode], [t_encode])
            # df = pd.DataFrame(x, index=None)
            # final_df = pd.concat((final_df, df), axis=0)
            my_data = [target_APIs.iloc[i, 0], str(x[0][0])]
            with open('data/tf_match/'+source_APIs.iloc[j, 1]+'.json', 'a') as f:
                json.dump(my_data, f)
                f.write('\n')


if __name__ == '__main__':
    calculate_similarity()