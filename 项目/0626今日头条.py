import requests
from bs4 import BeautifulSoup
from urllib import parse
import os
from hashlib import md5


class Toutiao():
    def __init__(self):
        self.baseUrl = 'https://so.toutiao.com/search?'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": "_S_DPR=1; _S_IPAD=0; MONITOR_WEB_ID=6978069671490061860; ttwid=1%7C09li-SEtruoOloDbuvPZ1UqnY_9dFpinrkHjZTtYk4A%7C1624709628%7C85e238db8937fc09053d05ef1b212b8ff588c7e11e25a15da1031cd52ea7a1f8; _S_WIN_WH=1920_362",
            "Host": "so.toutiao.com",
            "Referer": "https://www.toutiao.com/"
        }

    def getImgUrl(self, kw):
        self.data = {
            'dvpf': 'pc',
            'source': 'input',
            'keyword': kw
        }
        self.baseUrl = self.baseUrl + parse.urlencode(self.data)

        rsp = requests.get(self.baseUrl, headers=self.headers)
        soup = BeautifulSoup(rsp.text, 'lxml')
        firstItem = soup.select('div.result-content ')[0]
        aHrefs = firstItem.select('a')
        aHref = [alinks for alinks in aHrefs if alinks.string == '图片'][0]
        return self.baseUrl + aHref.get('href')

    def getPics(self, url):
        rsp = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(rsp.text, 'lxml')
        imgs = soup.select('img')
        return [img.get('src') for img in imgs] if imgs else None

    def downloadImgs(self,url):
        rsp = requests.get(url)
        return rsp.content if rsp else None

    def saveImg(self,content):
        fn = '{0}/toutiaoImg/{1}.{2}'.format(os.getcwdb(), md5(content).hexdigest(), 'webp')
        with open(fn, 'wb') as f:
            f.write(content)
            f.close()


tt = Toutiao()
# tt.getPics(tt.getImgUrl('街拍'))
mmUrl = tt.getImgUrl('街拍')
if mmUrl:
    imgUrls = tt.getPics(mmUrl)
    if imgUrls:
        for url in imgUrls:
            content = tt.downloadImgs(url)
            if content:
                tt.saveImg(content)

