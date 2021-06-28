import re, time
import requests
from bs4 import BeautifulSoup
from urllib import parse

baseUrl = 'http://www.htqyy.com'

homeUrl = 'http://www.htqyy.com/top/musicList/hot?pageIndex={}&pageSize=20'


def getUrl(page):
    return homeUrl.format(page)


header = {
    'Referer': 'http://www.htqyy.com/top/hot',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

}


def get_page(url, encoding='utf8'):
    try:
        rsp = requests.get(url, headers=header)
        return rsp.content.decode(encoding) if requests.codes.ok == rsp.status_code else None
    except requests.exceptions.HTTPError:
        print('HttpError')
    except requests.exceptions.ConnectionError:
        print('ConnectionError')


def getLikesCount(url, encoding='utf8'):
    rsp = get_page(url, encoding=encoding)
    if rsp:
        soup = BeautifulSoup(rsp, 'lxml')
        likeCount = soup.select('#likeCount')[0].string
        # bdsCount = soup.select('.bdsharebuttonbox a.bds_count')[0].string
    return likeCount


def getBdsCount(url):
    data = {
        'url': url,
        'callback': 'bd__cbs__8zonuy'
    }

    header = {
        'Accept': '* / *',
        'Host': 'api.share.baidu.com',
        'Referer': 'http://www.htqyy.com/',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

    url = 'http://api.share.baidu.com/getnum?' + parse.urlencode(data)
    rsp = requests.get(url,headers=header)
    r = re.search('"(\d+)"', rsp.text)
    return r.group(1)

# print(getBdsCount('http://www.htqyy.com/play/3'))
def parse_hotpage(rsp):
    soup = BeautifulSoup(rsp, 'lxml')
    lis = soup.select('#musicList .mItem')
    for li in lis:
        num = li.select('span')[0].string
        title = li.select('span.title')[0].string
        songUrl = baseUrl + li.select('span.title a')[0].get('href')
        artistName = li.select('span.artistName')[0].string
        artistUrl = baseUrl + li.select('span.artistName a')[0].get('href')
        albumName = li.select('span.albumName')[0].string
        albumUrl = baseUrl + li.select('span.albumName a')[0].get('href')
        playCount = li.select('span.playCount')[0].string
        r = re.search('(\d+)', playCount)
        playCount = r.group(1)
        # try:
        #     r = re.search('(\d+)', playCount)
        #     playCount = r.group(1)
        # except:
        #     print('*'*120)
        #     print(playCount)
        likeCount = getLikesCount(songUrl)
        bdsCount = getBdsCount(songUrl)
        yield {
            'num': num,
            'title': title,
            'songUrl': songUrl,
            'artistName': artistName,
            'artistUrl': artistUrl,
            'albumName': albumName,
            'albumUrl': albumUrl,
            'playCount': playCount,
            'likeCount': likeCount,
            'bdsCount': bdsCount,
        }

startTime = time.time()

for page in range(25):
    rsp = get_page(getUrl(page))
    for info in parse_hotpage(rsp):
        print(info)

print('花费的时间：', time.time() - startTime)
