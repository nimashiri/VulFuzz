from bs4 import BeautifulSoup as soup
from numpy import isin
from selenium import webdriver
# driver = webdriver.Firefox(executable_path= r"/home/nimashiri/geckodriver-v0.32.0-linux64/geckodriver")
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import re
from csv import writer
import pandas as pd
import ast
import subprocess
import json
import requests
import os

ROOT_MODULES = ['tf', 'tf.compat.v1']
ROOT_DIR = os.getcwd()


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data


def write_list_to_txt4(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data+'\n')


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


def parse_api(api):

    write_list_to_txt4(api, 'api_code.py')

    with open("api_code.py", "r") as source:
        ast_tree = ast.parse(source.read())

    subprocess.call('rm -rf api_code.py', shell=True)

    # pprint(ast.dump(ast_tree))
    flag = parse_recursive_api_tree(ast_tree.body[0].value)
    return flag


def write_list_to_txt2(data, filename):
    with open(filename, "w") as file:
        for row in data:
            file.write(row+'\n')


def parse_sub_element_with_regex(data):
    for elem in data.contents:
        if isinstance(elem, str):
            if re.findall(r'torch\.(.*)\.(.*)\(', elem):
                return elem
        else:
            return parse_sub_element_with_regex(elem)


def parse_sub_element(data):
    for elem in data.contents:
        if isinstance(elem, str):
            return elem
        else:
            return parse_sub_element(elem)


def recursive_parse_api_description(data):
    g = []
    for elem in data.contents:
        if isinstance(elem, str):
            g.append(elem)
        else:
            x = parse_sub_element(elem)
            g.append(x)
    return g


def recursive_parse_api_sequence(data):
    if isinstance(data.contents[0], str):
        return data.contents[0]
    for elem in data.contents:
        if not isinstance(elem, str):
            return recursive_parse_api_sequence(elem)

def scrape_torch_v2():
    data = pd.read_csv('data/api_root_torch.csv')
    for i in range(len(data)):
        sub_content = requests.get(data.iloc[i, 1])
        page_soup2 = soup(sub_content.text, "html.parser")
        x = page_soup2.prettify()
        list_of_apis = re.findall(r'href\=\"generated((.|\n)*?)\.html', x)
        list_of_apis = [item[0] for item in list_of_apis]
        list_of_apis = set(list_of_apis)

        for api_ in list_of_apis:
            api_link = 'https://pytorch.org/docs/stable/generated{0}.{1}'.format(
                api_, 'html')
            sub_content2 = requests.get(api_link)
            page_soup3 = soup(sub_content2.text, "html.parser")
            content3 = page_soup3.contents[7]
            current_api_detailed = content3.contents[7].contents[5].contents[
                3].contents[1].contents[1].contents[1].contents[1].contents[1]

            # API sequence
            token_sequence_api = []
            for elem in current_api_detailed.contents[3].contents[1].contents:
                if isinstance(elem, str):
                    token_sequence_api.append(elem)
                else:
                    if not isinstance(elem, str):
                        api_token = recursive_parse_api_sequence(elem)
                        token_sequence_api.append(api_token)

            # token_sequence_api = token_sequence_api[: len(token_sequence_api) - 2]
            token_sequence_api = " ".join(token_sequence_api)

            print('{0}'.format(token_sequence_api))

            # API example
            global_example = []
            for counter, elem in enumerate(current_api_detailed.contents[3].contents[3].contents):
                if not isinstance(elem, str):
                    if not bool(elem.attr):
                        out_temp = recursive_parse_api_description(elem)
                        if 'Example' in out_temp or 'Example:' in out_temp:
                            all_examples = []
                            for h in current_api_detailed.contents[3].contents[3].contents[counter+2:-1]:
                                if not isinstance(h, str):
                                    if bool(h.attrs) and h.attrs['class'][0] == 'highlight-default':
                                        all_examples.append(h)

                            for sub_elem in all_examples:
                                example_store = []
                                if not isinstance(sub_elem, str):
                                    for e in sub_elem.contents[0].contents[0].contents:
                                        if e == '\n':
                                            example_store.append('\n')
                                        else:
                                            if not isinstance(e, str):
                                                example_code = recursive_parse_api_description(
                                                    e)
                                                example_store.append(
                                                    example_code)

                                    global_example.append(example_store)
                            break
            temp = []
            for item in global_example:
                t = []
                for sub_item in item:
                    if sub_item:
                        t.append(sub_item[0])
                t = "".join(t)
                temp.append(t)

            # API description
            token_sequence_descp = []
            for i in range(len(current_api_detailed.contents[3].contents[3].contents)):
                if not isinstance(current_api_detailed.contents[3].contents[3].contents[i], str):
                    desc_token = recursive_parse_api_description(
                        current_api_detailed.contents[3].contents[3].contents[i])
                    token_sequence_descp.append(desc_token)

            token_sequence_descp = [j for i in token_sequence_descp for j in i]
            token_sequence_descp = [
                i for i in token_sequence_descp if i is not None]
            token_sequence_descp = " ".join(token_sequence_descp)

            my_data = [token_sequence_api, token_sequence_descp]
            my_data = my_data + temp

            with open('scrapers/pytorch_APIs_signatures.csv', 'a', newline='\n') as fd:
                writer_object = writer(fd)
                writer_object.writerow(my_data)


def scrape_torch_v1():
    torch_link = 'https://pytorch.org/docs/stable/index.html'
    #content = requests_retry_session().get(torch_link)

    # page_soup = soup(content.text, "html.parser")
    #content = page_soup.contents[7]
    # listt = content.contents[7].contents[5].contents[3].contents[1].contents[1].contents[1].contents[1].contents[1].contents[13].contents[3]

    data = pd.read_csv('data/api_root_torch.csv')

    for i in range(len(data)):
        # for item in listt.contents:
        # if not isinstance(item, str):
        #x = item.contents[0].contents[0].replace('torch.', '')
        #x = x.lower()

        # new_link = 'https://pytorch.org/docs/stable/{0}.html'.format(x)
        # time.sleep(2)
        sub_content = requests.get(data.iloc[i, 1])
        page_soup2 = soup(sub_content.text, "html.parser")
        content2 = page_soup2.contents[7]
        _modules = content2.contents[7].contents[5].contents[3].contents[1].contents[1].contents[1].contents[1].contents[1]
        for item in _modules:
            if not isinstance(item, str):
                if 'class' in item.attrs:
                    if item.attrs['class'][0] == 'section':
                        try:
                            _apis = item.contents[3].contents[1].contents

                            for _api in _apis:
                                if not isinstance(_api, str):
                                    # title_ = parse_sub_element_with_regex(_api)

                                    api_link = 'https://pytorch.org/docs/stable/generated/{0}.{1}'.format(
                                        _api.contents[0].contents[0].contents[1].attrs['title'], 'html')

                                    api_details = requests.get(api_link)
                                    page_soup_details = soup(
                                        api_details.text, "html.parser")
                                    content3 = page_soup_details.contents[7]
                                    current_api_detailed = content3.contents[7].contents[5].contents[
                                        3].contents[1].contents[1].contents[1].contents[1].contents[1]

                                    # API signature
                                    token_sequence_api = []
                                    for elem in current_api_detailed.contents[3].contents[1].contents:
                                        if not isinstance(elem, str):
                                            api_token = recursive_parse_api_sequence(
                                                elem)
                                            token_sequence_api.append(
                                                api_token)

                                    token_sequence_api = token_sequence_api[: len(
                                        token_sequence_api) - 2]
                                    token_sequence_api = " ".join(
                                        token_sequence_api)
                                    print(token_sequence_api)

                                    # API description
                                    token_sequence_descp = []
                                    for i in range(len(current_api_detailed.contents[3].contents[3].contents)):
                                        if not isinstance(current_api_detailed.contents[3].contents[3].contents[i], str):
                                            desc_token = recursive_parse_api_description(
                                                current_api_detailed.contents[3].contents[3].contents[i])
                                            token_sequence_descp.append(
                                                desc_token)

                                    token_sequence_descp = [
                                        j for i in token_sequence_descp for j in i]
                                    token_sequence_descp = [
                                        i for i in token_sequence_descp if i is not None]
                                    token_sequence_descp = " ".join(
                                        token_sequence_descp)

                                    with open('scrapers/pytorch_APIs_signature.csv', 'a', newline='\n') as fd:
                                        writer_object = writer(fd)
                                        writer_object.writerow(
                                            [token_sequence_api, token_sequence_descp])

                        except Exception as e:
                            print(e)


def x1(sub_item):
    for item in sub_item.contents:
        if isinstance(item, str):
            return item
        else:
            return x1(item)


def recursive_parse_item(item):
    if bool(item.contents):
        for sub_item in item.contents:
            if isinstance(sub_item, str):
                if sub_item.startswith('tf.'):
                    if not sub_item.endswith('\n)\n'):
                        if not sub_item.endswith(')'):
                            if not sub_item.endswith(')\n'):
                                if '(' in sub_item:
                                    out = []
                                    for c in item.contents:
                                        if not isinstance(c, str):
                                            x = x1(c)
                                            out.append(x)
                                        else:
                                            out.append(c)
                                    out = "".join(out)
                                    return out
                                    #flag = parse_api(out)
                                    # if flag:
                                    #     return out
                                    # else:
                                    #     return None
                    else:
                        return sub_item
                        # flag = parse_api(sub_item)
                        # if flag:
                        #     return sub_item
                        # else:
                        #     return None

            if not isinstance(sub_item, str):
                return recursive_parse_item(sub_item)


def ckeckList(lst):
    return len(set(lst)) == 1


def search_dict(d, q):
    if any([True for k, v in d.items() if v == q]):
        return True
    else:
        return False


def scrape_tensorflow_symbols(all_symbols_link):
    data = []
    content = requests.get(all_symbols_link)
    page_soup = soup(content.text, "html.parser")

    content_ = page_soup.contents[2].contents[3].contents[3].contents[4].contents[1].contents[3].contents[1]
<<<<<<< HEAD
    primary_symbols_2 = content_.contents[9].contents[11].contents
    compat_v1_symbols_2 = content_.contents[9].contents[15].contents
=======
<<<<<<< HEAD
    primary_symbols_2 = content_.contents[9].contents[11].contents
    compat_v1_symbols_2 = content_.contents[9].contents[15].contents
=======
    primary_symbols_2 = content_.contents[11].contents[11].contents
    compat_v1_symbols_2 = content_.contents[11].contents[15].contents
>>>>>>> major changes
>>>>>>> stable release

    # out_json = os.path.join(ROOT_DIR+'/scrapers', f'trash.json')
    _path = '/media/nimashiri/DATA/vsprojects/FSE23_2/scrapers/trash.json'
    jsonfile = open(_path, 'a', encoding='utf-8')
    jsonfile.write('[')

    for sec in [primary_symbols_2, compat_v1_symbols_2]:
        for api in sec:
            if not isinstance(api, str):
                if api.contents[0].contents[0].contents[0] not in ROOT_MODULES:
                    _link = api.contents[0].attrs['href']
                    print(_link)
                    # _link = 'https://www.tensorflow.org/api_docs/python/tf/compat/v1/scan'
                    #_link = 'https://www.tensorflow.org/api_docs/python/tf/compat/as_bytes'
                    # _link = 'https://www.tensorflow.org/api_docs/python/tf/Tensor'
                    sub_content = requests.get(_link)
                    page_soup2 = soup(sub_content.text, "html.parser")
                    content_2 = page_soup2.contents[2].contents[3].contents[
                        3].contents[4].contents[1].contents[3].contents[1]
<<<<<<< HEAD
                    d = content_2.contents[9].contents
=======
<<<<<<< HEAD
                    d = content_2.contents[9].contents
=======
                    d = content_2.contents[11].contents
>>>>>>> major changes
>>>>>>> stable release

                    token_sequence_descp = []
                    i_found_api_sig = False
                    for i, item in enumerate(d):
                        if not isinstance(item, str):
                            if 'class' in item.attrs and 'devsite-click-to-copy' in item.attrs['class']:
                                signature_ = recursive_parse_item(item)
                                if signature_ is not None:
                                    i_found_api_sig = True
                                    for elem in range(1, i-1):
                                        if not isinstance(d[elem], str):
                                            description = recursive_parse_api_description(
                                                d[elem])
                                            if bool(description):
                                                token_sequence_descp.append(
                                                    description)

                                    token_sequence_descp = [
                                        i for i in token_sequence_descp if i is not None]
                                    token_sequence_descp = [
                                        item for item in token_sequence_descp if not ckeckList(item)]
                                    token_sequence_descp = [
                                        item for item in token_sequence_descp if 'View aliases' not in item]
                                    # token_sequence_descp = "".join(token_sequence_descp[0])
                                    # token_sequence_descp = token_sequence_descp.replace('\n','')
                                    break

                    if i_found_api_sig:
                        all_examples = []
                        # # Typical example boxes
                        # for i, item in enumerate(d):
                        #     if not isinstance(item, str):
                        #         for sub_item in item.contents:
                        #             if not isinstance(sub_item, str):
                        #                 if 'class' in sub_item.attrs:
                        #                     if 'orange' in sub_item.attrs['class']:
                        #                         out = recursive_parse_api_description(sub_item)
                        #                         if 'Examples' in out:
                        #                             for e in d[i+2:-1]:
                        #                                 if not isinstance(e, str):
                        #                                     if 'class' in e.attrs and 'prettyprint' in e.attrs['class']:
                        #                                         example_i = recursive_parse_api_sequence(e)
                        #                                         all_examples.append(example_i)
                        #                             break
                        # Standalone usages
                        for i, item in enumerate(d):
                            if not isinstance(item, str):
                                #     for sub_item in item.contents:
                                #         if sub_item == 'Standalone usage:':
                                #             for e in d[i+2:-1]:
                                #                 local_example = []
                                #                 if not isinstance(e, str):
                                if 'class' in item.attrs and 'prettyprint' in item.attrs['class']:
                                    local_code_area = []
                                    for sub_e in item:
                                        if sub_e == '\n':
                                            local_code_area.append(sub_e)
                                        else:
                                            if not isinstance(sub_e, str):
                                                example_i = recursive_parse_api_description(
                                                    sub_e)
                                                if example_i:
                                                    local_code_area.append(
                                                        example_i[0])
                                                else:
                                                    local_code_area.append(
                                                        example_i)
                                    all_examples.append(local_code_area)

                        temp = []
                        for item in all_examples:
                            for sub_item in item:
<<<<<<< HEAD
                                if sub_item != '\n':
                                    temp.append(sub_item)
=======
<<<<<<< HEAD
                                if sub_item != '\n':
                                    temp.append(sub_item)
=======
                                if bool(sub_item) == True and sub_item != '\n':
                                    temp.append(sub_item)
                        if temp:
                            del temp[0]
                            temp = "\n".join(temp)
>>>>>>> major changes
>>>>>>> stable release

                    if i_found_api_sig:
                        # jsonfile.write('\n')
                        # temp_dict = {'signature': signature_, 'description': token_sequence_descp, 'example': temp}
                        # json.dump(temp_dict, jsonfile, indent=4)
                        # jsonfile.write(',')
                        # jsonfile.write(']')
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> stable release
                        my_data = [signature_, token_sequence_descp]
                        my_data = my_data + temp

                        with open('scrapers/tf_APIs_signatures.csv', 'a', newline='\n') as fd:
                            writer_object = writer(fd)
                            # for ex in all_examples:
<<<<<<< HEAD
=======
=======
                        my_data = [signature_, token_sequence_descp, temp]
                        # my_data = my_data + temp

                        with open('/media/nimashiri/DATA/vsprojects/FSE23_2/scrapers/tf_APIs_signatures.csv', 'a', newline='\n') as fd:
                            writer_object = writer(fd)
>>>>>>> major changes
>>>>>>> stable release
                            writer_object.writerow(my_data)


def scrape_mxnet():

    _path = '/media/nimashiri/DATA/vsprojects/FSE23_2/scrapers/mxnet_apis.json'
    jsonfile = open(_path, 'a', encoding='utf-8')
    jsonfile.write('[')

    full_api_parent_list = []
    root_api_link = 'https://mxnet.apache.org/versions/1.9.1/api/python/docs/api/'
    content = requests.get(root_api_link)
    page_soup = soup(content.text, "html.parser")
    api_list_left_bar = page_soup.contents[2].contents[3].contents[2].contents[
        1].contents[1].contents[3].contents[1].contents[3].contents[1].contents
    for item in api_list_left_bar:
        if not isinstance(item, str):
            if len(item.contents) > 1:
                for sub_api in item.contents[1]:
                    if not isinstance(sub_api, str):
                        # out = recursive_parse_api_description(sub_api)
                        _link = os.path.join(
                            root_api_link, sub_api.contents[0].attrs['href'])
                        full_api_parent_list.append(_link)
            else:
                _link = os.path.join(
                    root_api_link, item.contents[0].attrs['href'])
                full_api_parent_list.append(_link)

    for l in full_api_parent_list:
        content = requests.get(l)
        page_soup = soup(content.text, "html.parser")
        api_main_content = page_soup.contents[2].contents[3].contents[
            2].contents[3].contents[7].contents[1].contents[1].contents

        for com in api_main_content:
            if not isinstance(com, str):
                if bool(com.attrs) and 'class' in com.attrs:
                    if com.attrs['class'][0] == 'function' or com.attrs['class'][0] == 'class':
                        # API signature
                        current_api = []
                        for api_elem in com.contents[1]:
                            if isinstance(api_elem, str):
                                current_api.append(api_elem)
                            else:
                                if not isinstance(api_elem, str):
                                    api_si = recursive_parse_api_sequence(
                                        api_elem)
                                    current_api.append(api_si)

                        current_api = "".join(current_api)
                        if current_api[-1] == '[source]':
                            del current_api[-1]

                        print(current_api)
                        # API description
                        local_desc = []
                        for desc_elem in com.contents[3]:
                            if desc_elem == '\n':
                                local_desc.append(desc_elem)
                            else:
                                if not isinstance(desc_elem, str):
                                    current_desc = recursive_parse_api_description(
                                        desc_elem)
                                    local_desc.append(current_desc)

                        final_api_description = []
                        for item in local_desc:
                            if item == '\n':
                                final_api_description.append(item)
                            else:
                                for sub_item in item:
                                    final_api_description.append(sub_item)
                        final_api_description.append(item)

                        # API example
                        current_api_examples = []
                        for i, example_elem in enumerate(com.contents[3]):
                            if not isinstance(example_elem, str):
                                out = recursive_parse_api_description(
                                    example_elem)
                                if 'Example' in out:
                                    con = com.contents[3].contents
                                    for d in con:
                                        local_example = []
                                        if not isinstance(d, str):
                                            if bool(d.attrs):
                                                if 'class' in d.attrs:
                                                    for k in d.attrs['class']:
                                                        if k == 'highlight-default':
                                                            for e in d.contents[0].contents[0].contents:
                                                                if e == '\n':
                                                                    local_example.append(
                                                                        '\n')
                                                                else:
                                                                    if not isinstance(e, str):
                                                                        example_code = recursive_parse_api_description(
                                                                            e)
                                                                        local_example.append(
                                                                            example_code)

                                                            current_api_examples.append(
                                                                local_example)
                        temp = []
                        for item in current_api_examples:
                            t = []
                            for sub_item in item:
                                if sub_item:
                                    t.append(sub_item[0])
                            t = "".join(t)
                            temp.append(t)

                        my_data = [current_api, final_api_description]
                        my_data = my_data + temp

                        with open('scrapers/mxnet_APIs_signatures.csv', 'a', newline='\n') as fd:
                            writer_object = writer(fd)
                            # for ex in all_examples:
                            writer_object.writerow(my_data)
    #                     jsonfile.write('\n')
    #                     temp_dict = {'signature': current_api, 'description': final_api_description, 'example': out_ex}
    #                     json.dump(temp_dict, jsonfile, indent=4)
    #                     jsonfile.write(',')
    # jsonfile.write(']')


def main():
    all_symbols_link = 'https://www.tensorflow.org/api_docs/python/tf/all_symbols'
<<<<<<< HEAD
    code = 'mx'
=======
<<<<<<< HEAD
    code = 'mx'
=======
    code = 'tf'
>>>>>>> major changes
>>>>>>> stable release

    if code == 'tf':
        scrape_tensorflow_symbols(all_symbols_link)
    elif code == 'pytorch':
        scrape_torch_v2()
    else:
        scrape_mxnet()


def count_examples():
    tf_data = pd.read_csv('scrapers/tf_APIs_signatures.csv', skiprows=1)
    pytorch_data = pd.read_csv('scrapers/tf_APIs_signatures.csv', skiprows=1)
    mxnet_data = pd.read_csv('scrapers/tf_APIs_signatures.csv', skiprows=1)

    counter = 0
    for i in range(len(tf_data)):
        if tf_data.iloc[i, 2]:
            counter = counter + 1
    print(counter)


if __name__ == '__main__':
    main()
    # count_examples()
