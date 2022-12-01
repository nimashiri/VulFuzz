import json
import os
import re
import requests
import random
import datetime
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from csv import writer

# (0, nimashiri2012@gmail.com, 1, cse19922021@gmail.com, 2, nshiri@yorku.ca, 3, nshiri@cse.yorku.ca)
tokens = {0: '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', 1: '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',
          2: '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', 3: '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'}

tokens_status = {'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': True, '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': True,
                 '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': True, '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': True}


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


retries = 10
#potential_commits = []
now = datetime.datetime.now()


def get_commits(githubUser, currentRepo, qm, page, amp, sh_string, last_com, page_number, branch_sha, potential_commits, current_token):

    page_number += 1

    print("Current page number is: {}".format(page_number))

    if page_number == 1:
        first_100_commits = "https://api.github.com/repos/" + \
                githubUser + "/"+ currentRepo+"/issues" + \
                qm + page

        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})
    else:
        response = requests_retry_session().get(last_com, headers={
            'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    if response.status_code != 200:
        tokens_status[current_token] = False
        current_token = select_access_token(current_token)
        response = requests_retry_session().get(first_100_commits, headers={
            'Authorization': 'token {}'.format(current_token)})

    first_100_commits = json.loads(response.text)

    if len(first_100_commits) == 1:
        return None
    for i, commit in enumerate(first_100_commits):

        memory_related_rules = r"(denial of service|DOS|remote code execution|CVE|ReDoS|NVD|malicious|attack|exploit|RCE|advisory|insecure|security|infinite.loop|bypass|injection|overflow|(in)?secur(e|ity)|Heap buffer overflow|Integer division by zero|Undefined behavior|Heap OOB write|Division by zero|Crashes the Python interpreter|Heap overflow|Uninitialized memory accesses|Heap OOB access|Heap underflow|Heap OOB|Heap OOB read|Segmentation faults|Segmentation fault|seg fault|Buffer overflow|Null pointer dereference|FPE runtime|segfaults|segfault|attack|corrupt|crack|craft|CVE-|deadlock|deep recursion|denial-of-service|divide by 0|divide by zero|divide-by-zero|division by zero|division by 0|division-by-zero|division-by-0|double free|endless loop|leak|initialize|insecure|invalid|info leak|null deref|null-deref|NULL dereference|null function pointer|null pointer dereference|null-ptr|null-ptr-deref|OOB|out of bound|out-of-bound|overflow|protect|race|race condition|RCE|remote code execution|sanity check|sanity-check|security|security fix|security issue|security problem|snprintf|undefined behavior|underflow|uninitialize|use after free|use-after-free|violate|violation|vsecurity|vuln|vulnerab)"
        _rule = r"(denial of service|DOS|XXE|remote code execution|bopen redirect|OSVDB|bvuln|CVE|XSS|ReDoS|NVD|malicious|x−frame−options|attack|cross-site|exploit|directory traversal|RCE|XSRF|clickjack|session-fixation|hijack|advisory|insecure|security|cross-origin|unauthori[z|s]ed|infinite.loop|brute force|bypass|constant time|crack|credential|expos(e|ing|ure)|hack|harden|injection|lockout|overflow|password|PoC|proof of concept|priveale|(in)?secur(e|ity)|Heap buffer overflow|Integer division by zero|Undefined behavior|Heap OOB write|Division by zero|Crashes the Python interpreter|Heap overflow|Uninitialized memory accesses|Heap OOB access|Heap underflow|Heap OOB|Heap OOB read|Segmentation faults|Segmentation fault|seg fault|Buffer overflow|Null pointer dereference|FPE runtime|segfaults|segfault|attack|authenticate|authentication|checkclickjack|compromise|constant-time|corrupt|crack|craft|credential|cross Site Request Forgery|cross-Site Request Forgery|CVE-|Dan Rosenberg|deadlock|deep recursion|denial-of-service|directory traversal|disclosure|divide by 0|divide by zero|divide-by-zero|division by zero|division by 0|division-by-zero|division-by-0|double free|endless loop|exhaust|dos|fail|fixes CVE-|forgery|fuzz|general protection fault|GPF|grsecurity|guard|leak|initialize|insecure|invalid|KASAN|info leak|limit|lockout|long loop|loop|man in the middle|man-in-the-middle|mishandle|MITM|negative|null deref|null-deref|NULL dereference|null function pointer|null pointer dereference|null-ptr|null-ptr-deref|off-by-one|OOB|oops|open redirect|oss-security|out of array|out of bound|out-of-bound|overflow|overread|override|overrun|panic|password|poison|prevent|privesc|privilege|protect|race|race condition|RCE|remote code execution|replay|sanity check|sanity-check|security|security fix|security issue|security problem|session fixation|snprintf|spoof|syzkaller|trinity|unauthorized|undefined behavior|underflow|unexpected|uninitialize|unrealize|use after free|use-after-free|valid|verification|verifies|verify|violate|violation|vsecurity|vuln|vulnerab|XML External Entity)"
        
        memory_related_rules_strict = r"(\bdenial of service\b|\bDOS\b|\bremote code execution\b|\bCVE\b|\bNVD\b|\bmalicious\b|\battack\b|\bexploit\b|\bRCE\b|\badvisory\b|\binsecure\b|\bsecurity\b|\binfinite\b|\bbypass\b|\binjection\b|\boverflow\b|\bHeap buffer overflow\b|\bInteger division by zero\b|\bUndefined behavior\b|\bHeap OOB write\b|\bDivision by zero\b|\bCrashes the Python interpreter\b|\bHeap overflow\b|\bUninitialized memory accesses\b|\bHeap OOB access\b|\bHeap underflow\b|\bHeap OOB\b|\bHeap OOB read\b|\bSegmentation faults\b|\bSegmentation fault\b|\bseg fault\b|\bBuffer overflow\b|\bNull pointer dereference\b|\bFPE runtime\b|\bsegfaults\b|\bsegfault\b|\battack\b|\bcorrupt\b|\bcrack\b|\bcraft\b|\bCVE-\b|\bdeadlock\b|\bdeep recursion\b|\bdenial-of-service\b|\bdivide by 0\b|\bdivide by zero\b|\bdivide-by-zero\b|\bdivision by zero\b|\bdivision by 0\b|\bdivision-by-zero\b|\bdivision-by-0\b|\bdouble free\b|\bendless loop\b|\bleak\b|\binitialize\b|\binsecure\b|\binfo leak\b|\bnull deref\b|\bnull-deref\b|\bNULL dereference\b|\bnull function pointer\b|\bnull pointer dereference\b|\bnull-ptr\b|\bnull-ptr-deref\b|\bOOB\b|\bout of bound\b|\bout-of-bound\b|\boverflow\b|\bprotect\b|\brace\b|\brace condition\b|RCE|\bremote code execution\b|\bsanity check\b|\bsanity-check\b|\bsecurity\b|\bsecurity fix\b|\bsecurity issue\b|\bsecurity problem\b|\bsnprintf\b|\bundefined behavior\b|\bunderflow\b|\buninitialize\b|\buse after free\b|\buse-after-free\b|\bviolate\b|\bviolation\b|\bvsecurity\b|\bvuln\b|\bvulnerab\b)"


        title_match = False
        body_match = False
        if re.findall(memory_related_rules_strict, commit['title']):
            title_match = True
        
        if bool(commit['body']) and re.findall(memory_related_rules_strict, commit['body']):
            body_match = True

        _date = commit['created_at']
        sdate = _date.split('-')

        if title_match or body_match and re.findall(r'(torch\.)', commit['body']) or re.findall(r'(torch\.)', commit['title']):
            _date = commit['created_at']
            sdate = _date.split('-')

            potential_commits.append(commit['html_url'])


        if i == len(first_100_commits)-1:
            last_com = response.links['next']['url']

            with open('./issues/'+currentRepo, 'a') as f:
                for item in potential_commits:
                    f.write("%s\n" % item)
            
            potential_commits = []

            get_commits(githubUser, currentRepo, qm, page, amp, sh_string,
                        last_com, page_number, branch_sha, potential_commits, current_token)


def search_comit_data(c, commit_data):
    t = []

    for item in commit_data:
        temp = item.split('/')
        t.append('/' + temp[3] + '/' + temp[4] + '/')

    r_prime = c.split('/')
    x = '/' + r_prime[3] + '/' + r_prime[4] + '/'
    if any(x in s for s in t):
        return True
    else:
        return False


def select_access_token(current_token):
    x = ''
    if all(value == False for value in tokens_status.values()):
        for k, v in tokens_status.items():
            tokens_status[k] = True

    for k, v in tokens.items():
        if tokens_status[v] != False:
            x = v
            break
    current_token = x
    return current_token



def main():

    repo_list = [
        'https://github.com/pytorch/pytorch'
    ]

    if not os.path.exists('./issues'):
        os.makedirs('./issues')

    current_token = tokens[0]
    for lib in repo_list:
        x = []

        potential_commits = []
              
        r_prime = lib.split('/')

        qm = '?'
        page = 'per_page='+str(100)
        amp = '&'
        sh_string = "sha="

        branchLink = "https://api.github.com/repos/{0}/{1}/branches".format(
                    r_prime[3], r_prime[4])

        response = requests_retry_session().get(
                    branchLink, headers={'Authorization': 'token {}'.format(current_token)})
                    
        if response.status_code != 200:
                    tokens_status[current_token] = False
                    current_token = select_access_token(current_token)
                    response = requests_retry_session().get(
                        branchLink, headers={'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
                    tokens_status[current_token] = False
                    current_token = select_access_token(current_token)
                    response = requests_retry_session().get(
                        branchLink, headers={'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
                    tokens_status[current_token] = False
                    current_token = select_access_token(current_token)
                    response = requests_retry_session().get(
                        branchLink, headers={'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
                    tokens_status[current_token] = False
                    current_token = select_access_token(current_token)
                    response = requests_retry_session().get(
                        branchLink, headers={'Authorization': 'token {}'.format(current_token)})

        branches = json.loads(response.text)


        selected_branch = random.choice(branches)
        branch_sha = selected_branch['commit']['sha']

        page_number = 0

        # first_100_commits = "https://api.github.com/repos/" + \
        #     r_prime[3] + "/"+r_prime[4]+"/issues" + \
        #      qm + page + amp + sh_string + branch_sha


        first_100_commits = "https://api.github.com/repos/" + \
            r_prime[3] + "/"+r_prime[4]+"/issues" + \
             qm + page

        response = requests_retry_session().get(first_100_commits, headers={
                        'Authorization': 'token {}'.format(current_token)})
        if response.status_code != 200:
                        tokens_status[current_token] = False
                        current_token = select_access_token(current_token)
                        response = requests_retry_session().get(first_100_commits, headers={
                            'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
                        tokens_status[current_token] = False
                        current_token = select_access_token(current_token)
                        response = requests_retry_session().get(first_100_commits, headers={
                            'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
                        tokens_status[current_token] = False
                        current_token = select_access_token(current_token)
                        response = requests_retry_session().get(first_100_commits, headers={
                            'Authorization': 'token {}'.format(current_token)})

        if response.status_code != 200:
                        tokens_status[current_token] = False
                        current_token = select_access_token(current_token)
                        response = requests_retry_session().get(first_100_commits, headers={
                            'Authorization': 'token {}'.format(current_token)})

        first_100_commits = json.loads(response.text)

        if len(first_100_commits) >= 100:
            last_com = response.links['last']['url']

            get_commits(r_prime[3], r_prime[4], qm, page, amp, sh_string, last_com,
                                    page_number, branch_sha, potential_commits, current_token)

            # with open('./issues/'+r_prime[4], 'a') as f:
            #     for item in potential_commits:
            #         f.write("%s\n" % item)
        else:
            #memory_related_rules = r"(denial of service|DOS|remote code execution|CVE|ReDoS|NVD|malicious|attack|exploit|RCE|advisory|insecure|security|infinite.loop|bypass|injection|overflow|(in)?secur(e|ity)|Heap buffer overflow|Integer division by zero|Undefined behavior|Heap OOB write|Division by zero|Crashes the Python interpreter|Heap overflow|Uninitialized memory accesses|Heap OOB access|Heap underflow|Heap OOB|Heap OOB read|Segmentation faults|Segmentation fault|seg fault|Buffer overflow|Null pointer dereference|FPE runtime|segfaults|segfault|attack|corrupt|crack|craft|CVE-|deadlock|deep recursion|denial-of-service|divide by 0|divide by zero|divide-by-zero|division by zero|division by 0|division-by-zero|division-by-0|double free|endless loop|leak|initialize|insecure|invalid|info leak|null deref|null-deref|NULL dereference|null function pointer|null pointer dereference|null-ptr|null-ptr-deref|OOB|out of bound|out-of-bound|overflow|protect|race|race condition|RCE|remote code execution|sanity check|sanity-check|security|security fix|security issue|security problem|snprintf|undefined behavior|underflow|uninitialize|use after free|use-after-free|violate|violation|vsecurity|vuln|vulnerab)"
            #_rule = r"(denial of service|DOS|XXE|remote code execution|bopen redirect|OSVDB|bvuln|CVE|XSS|ReDoS|NVD|malicious|x−frame−options|attack|cross-site|exploit|directory traversal|RCE|XSRF|clickjack|session-fixation|hijack|advisory|insecure|security|cross-origin|unauthori[z|s]ed|infinite.loop|brute force|bypass|constant time|crack|credential|expos(e|ing|ure)|hack|harden|injection|lockout|overflow|password|PoC|proof of concept|priveale|(in)?secur(e|ity)|Heap buffer overflow|Integer division by zero|Undefined behavior|Heap OOB write|Division by zero|Crashes the Python interpreter|Heap overflow|Uninitialized memory accesses|Heap OOB access|Heap underflow|Heap OOB|Heap OOB read|Segmentation faults|Segmentation fault|seg fault|Buffer overflow|Null pointer dereference|FPE runtime|segfaults|segfault|attack|authenticate|authentication|checkclickjack|compromise|constant-time|corrupt|crack|craft|credential|cross Site Request Forgery|cross-Site Request Forgery|CVE-|Dan Rosenberg|deadlock|deep recursion|denial-of-service|directory traversal|disclosure|divide by 0|divide by zero|divide-by-zero|division by zero|division by 0|division-by-zero|division-by-0|double free|endless loop|exhaust|dos|fail|fixes CVE-|forgery|fuzz|general protection fault|GPF|grsecurity|guard|leak|initialize|insecure|invalid|KASAN|info leak|limit|lockout|long loop|loop|man in the middle|man-in-the-middle|mishandle|MITM|negative|null deref|null-deref|NULL dereference|null function pointer|null pointer dereference|null-ptr|null-ptr-deref|off-by-one|OOB|oops|open redirect|oss-security|out of array|out of bound|out-of-bound|overflow|overread|override|overrun|panic|password|poison|prevent|privesc|privilege|protect|race|race condition|RCE|remote code execution|replay|sanity check|sanity-check|security|security fix|security issue|security problem|session fixation|snprintf|spoof|syzkaller|trinity|unauthorized|undefined behavior|underflow|unexpected|uninitialize|unrealize|use after free|use-after-free|valid|verification|verifies|verify|violate|violation|vsecurity|vuln|vulnerab|XML External Entity)"
            
            memory_related_rules_strict = r"(mx.|\bdenial of service\b|\bDOS\b|\bremote code execution\b|\bCVE\b|\bNVD\b|\bmalicious\b|\battack\b|\bexploit\b|\bRCE\b|\badvisory\b|\binsecure\b|\bsecurity\b|\binfinite\b|\bbypass\b|\binjection\b|\boverflow\b|\bHeap buffer overflow\b|\bInteger division by zero\b|\bUndefined behavior\b|\bHeap OOB write\b|\bDivision by zero\b|\bCrashes the Python interpreter\b|\bHeap overflow\b|\bUninitialized memory accesses\b|\bHeap OOB access\b|\bHeap underflow\b|\bHeap OOB\b|\bHeap OOB read\b|\bSegmentation faults\b|\bSegmentation fault\b|\bseg fault\b|\bBuffer overflow\b|\bNull pointer dereference\b|\bFPE runtime\b|\bsegfaults\b|\bsegfault\b|\battack\b|\bcorrupt\b|\bcrack\b|\bcraft\b|\bCVE-\b|\bdeadlock\b|\bdeep recursion\b|\bdenial-of-service\b|\bdivide by 0\b|\bdivide by zero\b|\bdivide-by-zero\b|\bdivision by zero\b|\bdivision by 0\b|\bdivision-by-zero\b|\bdivision-by-0\b|\bdouble free\b|\bendless loop\b|\bleak\b|\binitialize\b|\binsecure\b|\binfo leak\b|\bnull deref\b|\bnull-deref\b|\bNULL dereference\b|\bnull function pointer\b|\bnull pointer dereference\b|\bnull-ptr\b|\bnull-ptr-deref\b|\bOOB\b|\bout of bound\b|\bout-of-bound\b|\boverflow\b|\bprotect\b|\brace\b|\brace condition\b|RCE|\bremote code execution\b|\bsanity check\b|\bsanity-check\b|\bsecurity\b|\bsecurity fix\b|\bsecurity issue\b|\bsecurity problem\b|\bsnprintf\b|\bundefined behavior\b|\bunderflow\b|\buninitialize\b|\buse after free\b|\buse-after-free\b|\bviolate\b|\bviolation\b|\bvsecurity\b|\bvuln\b|\bvulnerab\b)"
            doc_errors = r'(documentation)'
            try:
                temp = []
                for i, com in enumerate(first_100_commits):

                    title_match = re.findall(memory_related_rules_strict, com['title'])
                    body_match = re.findall(memory_related_rules_strict, com['body'])

                    if title_match or body_match:
                        x = requests_retry_session().get(com['url'])
                        x = json.loads(x.text)

                        temp.append(com['html_url'])
     
            except Exception as e:
                print(e)

            with open('./issues/'+r_prime[4], 'a') as f:
                for item in temp:
                    f.write("%s\n" % item)

if __name__ == "__main__":
    main()