#coding=utf-8

from BeautifulSoup import BeautifulSoup
import urllib2
import re
from urlparse import urlparse,urljoin
from logger import Logger

logger = Logger(logname='fetcher-log', loglevel=3,callfile='fetcher')

class Fetch(object):

    def __init__(self, url):
        self.html = urllib2.urlopen(url).read()
        self.url = url
        self.sh = urlparse(self.url)[0]+"://"+urlparse(self.url)[1]
        self.soup = BeautifulSoup(self.html)
        self.hostname = '.'.join(urlparse(self.url).hostname.split('.')[-2:])

    def filter_link(self,link,attr):
        """
            对连接进行过滤 返回满足要求的链接
        """
        for dom in self.soup.findAll(link):
            href= dom.get(attr)
            if not href:
                continue
            if '#' in href or 'javascript' in href or 'void(' in href:
                continue
            if not href.startswith('http://') and not href.startswith('https://'):
                href = urljoin(self.sh,href)
            yield href


    def get_all_link(self):
        """
            找到所有满足要求的a标签中的链接
        """

        logger.get_logger.info("start to find a in "+self.url)
        a = []
        if self.soup:
            for href in self.filter_link('a','href'):
                pat = re.compile("http://[a-z0-9A-Z]+.%s"%self.hostname)#判断路径是不是xxx.hao123.com下的
                if pat.search(href):
                    a.append(href)
        logger.get_logger.info("find a end in "+self.url)
        return a

    def get_all_resource(self):
        """
            找到所有满足要求资源链接
        """
        logger.get_logger.info("start to find resource in "+self.url)
        resource = []
        if self.soup:
            for href in self.filter_link('a','href'):
                resource.append(href)
            for href in self.filter_link('img','src'):
                resource.append(href)
            for href in self.filter_link('script','src'):
                resource.append(href)
            for href in self.filter_link('link','href'):
                resource.append(href)
            for href in self.filter_link('iframe','href'):
                resource.append(href)
        logger.get_logger.info("find resource end in "+self.url)
        return resource

if __name__ == '__main__':
    fetch = Fetch('http://video.hao123.com/')
    for link in  fetch.get_all_link():
        print link