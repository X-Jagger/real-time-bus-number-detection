# collect imamges for obj detection online
# images number,images quality,

# import os
# 

# from bs4 import BeautifulSoup as Soup
# import json

# url_a = 'https://www.google.com/search?ei=1m7NWePfFYaGmQG51q7IBg&hl=en&q={}'
# url_b = '\&tbm=isch&ved=0ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ&start={}'
# url_c = '\&yv=2&vet=10ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ.1m7NWePfFYaGmQG51q7IBg'
# url_d = '\.i&ijn=1&asearch=ichunk&async=_id:rg_s,_pms:s'
# url_base = ''.join((url_a, url_b, url_c, url_d))

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

import os
import requests
from bs4 import BeautifulSoup
import re
import urllib.request as ulib

url_base = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1524123017900_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word={}'

# str = '"thumbURL":"http://img0.imgtn.bdimg.com/it/u=2000158775,786417739&fm=27&gp=0.jpg","replaceUrl".jpg'


def get_links(search_name):
    search_name = search_name.replace(' ', '+')
    url = url_base.format(search_name)
    print(url)
    r = requests.get(url,headers=headers)
    #use regular expression to extract the links 
    pattern = re.compile(r'thumbURL.*?http.*?.jpg')
    pattern2 = re.compile(r'http.*?.jpg')
    items = pattern.findall(r.text)
    links = [pattern2.findall(item)[0] for item in items]
    # request = ulib.Request(url, None, headers)
    # json_string = ulib.urlopen(request).read()
    # page = json.loads(json_string)
    # new_soup = Soup(page[1][1], 'lxml')
    # images = new_soup.find_all('img')
    # links = [image['src'] for image in images]
    return links


def save_images(links, search_name):
    directory = search_name.replace(' ', '_')
    if not os.path.isdir(directory):
        print('print')
        os.mkdir(directory)
    
    txt = url_base.format(search_name)
    txt_pathname = os.path.join(directory,'txt.txt')
    for i, link in enumerate(links):
        txt = txt + '\n' + link
        # print('txt is',txt)

        if i == len(links)-1:
            open(txt_pathname,'w').write(txt)
        savepath = os.path.join(directory, '{:06}.jpg'.format(i))
        ir = requests.get(link,headers=headers)
        print(i,ir.status_code)
        if ir.status_code == 200:
            open(savepath,'wb').write(ir.content)
        # ulib.urlretrieve(link, savepath)


if __name__ == '__main__':
    search_name = '公交车'
    links = get_links(search_name)
    save_images(links, search_name)

