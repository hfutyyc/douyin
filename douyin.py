import re
import requests
from time import sleep


user_id = '91714153251'
headers = {
'user-agent':       "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}
url = 'https://www.amemv.com/share/user/{}?u_code=mh9l16ic&timestamp=1536574517&utm_source=weixin&utm_campaign=client_share&utm_medium=android&app=aweme&iid=43779124892'.format(user_id)
response = requests.get(url, headers=headers)

res = response.content.decode()
name = re.findall('<p class="nickname">(.*?)</p>', response.text)[0]
dytk = re.findall("dytk: '(.*?)'", response.text)[0]


URL_LIST = []

def get_all_video_urls(user_id, max_cursor, dytk):
    url = "https://www.amemv.com/aweme/v1/aweme/post/?user_id={}&count=21&max_cursor={}&aid=1128&dytk={}".format(user_id, max_cursor, dytk)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for li in data['aweme_list']:
            name = li.get('share_info').get('share_desc')
            url = li.get('video').get('play_addr').get('url_list')[0]
            URL_LIST.append([name, url])
            
        if data['has_more'] == 1 and data.get('max_cursor') != 0:
            sleep(1)
            return get_all_video_urls(user_id, data.get('max_cursor'), dytk)
        else:
            return
    else:
        print(response.status_code)
        return None

get_all_video_urls(user_id, 0, dytk)
print(URL_LIST)
print(len(URL_LIST))

