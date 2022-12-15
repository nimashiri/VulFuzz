import json
from datetime import date, timedelta
import os
import requests as r
import time
import math

token = os.getenv('GITHUB_TOKEN', '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')

def get_repos(_link, per_page, page_num, first_repo, counter, lib):
    repo_list = []
    try:
        response = r.get(_link, headers={'Authorization': 'token {}'.format('')})
        response = json.loads(response.text)
        for i, item in enumerate(response['items']):
            if response['items'][i+1]['id'] == first_repo:
                return repo_list
            else:
                print(lib)
                print('Total number of repositories extracted so far ---> {0}'.format(counter))
                repo_list.append(item['html_url'])
                counter += 1
    except Exception as e:
        print(e)
        page_num += 1
        _link = "https://api.github.com/search/repositories?q={0}%20in:name,description+created:2018-01-01..2018-01-31&python?language=python&sort=stars&per_page={1}&page={2}".format(lib, per_page, page_num)
        get_repos(_link, per_page, page_num, first_repo ,counter, lib)

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def write_list_to_txt2(data, filename):
    with open(filename+".txt", "a") as file:
        file.write(data+'\n')

def determine_page_number(lib, v , per_page):
    _pre_link = "https://api.github.com/search/repositories?q={0}%20in:name,description+created:{1}&python?language=python&sort=stars&per_page={2}".format(lib, v , per_page)
    response = r.get(_pre_link, headers={'Authorization': 'token {}'.format(token)})              
    response = json.loads(response.text)
    x = response['total_count']

    if x < 100:
        return 1
    else:
        return math.trunc(x / 100)

def main():
    page_num = 1
    per_page = 100
    k = 0
    i = 0

    # libs = [
    #     ['tensorflow', tensor_pg_size], 
    #     ['pytorch',torch_pg_size],
    #     ['keras',keras_pg_size],
    #     ['numpy',numpy_pg_size],
    #     ['pandas',pandas_pg_size],
    #     ['sklearn',sklearn_pg_size]
    #     ]
    libs = ['pytorch', 'tensorflow']
    years = [2020, 2021, 2022]

    # pg_list_size = [tensor_pg_size, torch_pg_size, keras_pg_size, numpy_pg_size, pandas_pg_size, sklearn_pg_size]
    
    for lib in libs:
        for item in years:
            start_dt = date(item, 1, 1)
            end_dt = date(item, 12, 29)
            d_list = []
            for dt in daterange(start_dt, end_dt):
                d_list.append(dt.strftime("%Y-%m-%d"))
            i = 0
            j = 6
            while(j < len(d_list)):
                try:
                    repo_list = []
                    v = d_list[i]+'..'+d_list[j]
                    i = j+1
                    j = j+7
                    #v2 = d_list[n+1]+'..'+d_list[n*2]
                    #for v in [v1, v2]:
                        # for sub_item in lib[1]:
                        #     for p in range(1, sub_item):

                    pg_size = determine_page_number(lib, v , per_page)

                    for p in range(1, pg_size+1):
                        _link = "https://api.github.com/search/repositories?q={0}%20created:{1}&python?language=python&sort=stars&per_page={2}&page={3}".format(lib, v , per_page, p)
                        time.sleep(0)
                        response = r.get(_link, headers={'Authorization': 'token {}'.format(token)})
                            
                        response = json.loads(response.text)

                        if response['total_count'] == 0:
                            print('Could not get any result!')
                        else:
                            print("Extracting from {0}, Year {1}, Period {2}, Page {3}".format(lib, item, v, p))
                            for x, rep in enumerate(response['items']):
                                if rep['watchers_count'] >= 1000 and rep['size'] >= 2000:
                                    write_list_to_txt2(rep['html_url'], lib)
                except Exception as e:
                    print(e)
                        
if __name__ == '__main__':
    main()