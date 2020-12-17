import selenium
from selenium import webdriver as wd
import time
from collections import Counter
from random import shuffle
from bs4 import BeautifulSoup as bs
import re
import argparse
import requests
import urllib
import ssl
from webdriver_manager.chrome import ChromeDriverManager

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', default=False, action='store_true')
parser.add_argument('--test', '-t', default=False, action='store_true')
args = parser.parse_args()

tag_list = []

explore_url = "https://www.instagram.com/explore/tags/"
insta_url = "https://www.instagram.com"

top_posts = '_9AhH0'

top_posts = 'v1Nh3 kIKUG  _bz0w'
top_posts = 'v1Nh3'

# open chrome headless
op = wd.ChromeOptions()
if not args.verbose:
    op.add_argument('headless')
d = wd.Chrome(
    executable_path=ChromeDriverManager().install(),
    chrome_options=op)
# b = wd.Chrome()

# adjust these params

spc_search = [
    'tokyospc',
    'nycspc',
    'myspc',
    'magnumphotos',
    'myspcstory',
    'spicollective',
    'everydayeverywhere',
    'storyofthestreet',
    'everybodystreet',
    'streetizm',
    'life_is_street',
    'eyeshotmag',
    'voidtokyo'
]
bnw_search = [
    'friendsinbnw',
    'streetphoto_bnw',
    'bnwstreet'
]
tokyo_search = [
    'tokyospc',
    'voidtokyo',
]
fuji_search = [
    'x100f',
    'fujifeed',
]
gr_search = [
    'ricohgr'
]
eva_search = [
   'animecover','evangelion','エヴァンゲリオン','animepiano','pianocover','pianist','guitarcover', 
]
nyc_search = [
    'newyorkcity',
    'nyc'
]
tokyo_search = [
    'tokyo',
    '東京'
]
pj_search = ['protest','onassignment','photojournalism']
cornell_search = [
    'cornell','ithacaisgorges'
]



search_list = spc_search+fuji_search+tokyo_search
search_list = pj_search+spc_search[1:-1]+fuji_search
search_list = cornell_search+gr_search+spc_search

# search_list = fuji_search+['ithaca','cornell','tokyospc']
# search_list = ['tokyo']


remove_list = ['instagram','urbanphotography','photographer']
search_len = len(search_list)

if args.test:
    search_list = ['instagram']
    search_len = 1

for s in range(search_len):
    print('Searching #' + search_list[s])
    try:
        d.get(explore_url+search_list[s])
        # print(d.page_source)
    except:
        continue
    b = bs(d.page_source,'html.parser')
    # b.get(explore_url+'/'+search_list[s])

    # # print(b.page_source)
    # time.sleep(3)

    # # close login prompt
    # if (s==0):
    #     b.find_elements_by_class_name('Ls00D')[0].click()

    # # get posts
    # posts = b.find_elements_by_class_name(top_posts)

    # print(b.prettify())
    # imgs = b.find_all('div',class_='KL4Bh')
    imgs = b.find_all('div',class_=top_posts)
    print("Images: {}".format(len(imgs)))

    for img in imgs[:9]:
        img_url = img.find('a').get('href')

        img_page = insta_url+img_url
        img_page = requests.get(img_page)
        img_soup = bs(img_page.text, 'html.parser')

        [tag_list.append(c.get('content')) for c in img_soup.find_all('meta',attrs={'property':'instapp:hashtags'})]
        # print(tag_list)

        # if (not cmt is None):
        #     splt_str = re.split('(#)',cmt)
        #     tag_idx = [i+1 for i,x in enumerate(splt_str) if x == '#']
        #     tags = [splt_str[i] for i in tag_idx]
        #     print(tags)
        #     # tags = cmt.split('#')
        #     # print(tags)
        #     try:
        #         tags = [t.split()[0] for t in tags]
        #         [tag_list.append(tag) for tag in tags]
        #     except:
        #         pass


    # print(tag_list)


    # # only get tags from the top 9 posts
    # for i in range(9):
    # # for i in range(1):

    #     # click on the first post
    #     posts[i].click()
    #     time.sleep(1)
    #     # print(b.page_source)

    #     # get all hashtag links
    #     tags = b.find_elements_by_partial_link_text('#')

    #     for t in tags:
    #         try:
    #             tag_list.append(t.get_attribute('innerHTML').encode().lower()) 
    #         except UnicodeEncodeError:
    #             print('Could not add tag: ' + t.get_attribute('innerHTML'))
    #     # print(tag_list)

    #     # try to close out unless click failed
    #     try:
    #         b.find_element_by_class_name('ckWGn').click()
    #         time.sleep(1)
    #     except:
    #         pass

    # print(Counter(tag_list))
    for remove_tag in remove_list:
        try:
            tag_list.remove(remove_tag)
        except:
            pass

    most_common_tags = Counter(tag_list).most_common()
    top_tags = list(list(zip(*Counter(tag_list).most_common(30)))[0])
    shuffle(top_tags)
    # print(" ".join(top_tags))

    next_search_idx = 0
    while(most_common_tags[next_search_idx][0] in search_list):
        next_search_idx = next_search_idx+1
    search_list.append(most_common_tags[next_search_idx][0])

# [tag_list.remove(t) for t in search_list]
tag_list = [t for t in tag_list if t not in search_list]
print(len(tag_list))
# get the 25 most used tags plus search list
top_tags = list(list(zip(*Counter(tag_list).most_common(30-search_len)))[0])
# top_tags = list(list(zip(*Counter(tag_list).most_common()))[0])

print(top_tags)
len_tt = len(top_tags)
# len_tt = len_tt//4
# top_tags = top_tags[(len_tt-(30-len(search_list))):len_tt]
# print(top_tags)
shuffle(top_tags)
top_tags = search_list[:search_len]+top_tags
print('\n')
print('\n.'.join(['']*6))
print("#"+" #".join(top_tags))
