import requests
import random
import json
from hashlib import md5
import time
import threading
mutex = threading.Lock()

# Set your own appid/appkey. 
appid = '20211020000977904' #your personel appid which you can apply for free from baidu
appkey = '58TUwilYmErjJBZDmD0n' #your personel appkey

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
last_send_time = 0


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


#auto to target
def translate2auto(query_txt, from_lang = "auto", to_lang = "zh"):
    global last_send_time;
    mutex.acquire()
    cur_time = time.time() * 1000
    diff = cur_time - last_send_time
    # print("diff: ", diff)
    if diff < 1000:
        time.sleep((1000 - diff) / 1000.0)

    salt = random.randint(32768, 65536)
    print(query_txt)
    sign = make_md5(appid + query_txt + str(salt) + appkey)
    payload = {'appid': appid, 'q': query_txt, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    print(result)
    last_send_time = time.time()*1000
    # print("last_send_time: ", last_send_time)
    mutex.release()
    return result["from"], result["trans_result"][0]["dst"]


if __name__=="__main__":
    #free version only got 1
    print(translate2auto("Guten Tag!", "auto", "en"))
    print(translate2auto("study hard", "auto", "en"))
    print(translate2auto("everything will be ok", "auto", "zh"))