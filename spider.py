#coding=utf-8
__author__ = 'Yiner'
import threading

import sys
from workermanager import WorkManager
from fetcher import Fetch
import time
from logger import Logger

resourcelist = []
urllist = []
class Timer(threading.Thread):
    def __init__(self, workmanager,max_size):
        super(Timer, self).__init__()
        self.workmanager = workmanager
        self.start()

    def run(self):
        while True:
            call_quit_flag = False
            #workmanager.check_thread()
            try:
                if not call_quit_flag and len(resourcelist) > max_size:#如果资源数达到 清空任务队列
                    call_quit_flag = True
                    self.workmanager.clear_queue()

                if call_quit_flag:
                    break
                time.sleep(1)
            except Exception,e:
                break

def do_work(argv):
    url = argv.get('url')
    workmanager = argv.get('workmanager')
    max_size = argv.get('max_size')
    fetcher = Fetch(url)
    for resource in fetcher.get_all_resource():
        if len(resourcelist) >max_size:
            break
        if resource not in resourcelist:
            resourcelist.append(resource)
            logger.get_logger.info(resource)


    for href in fetcher.get_all_link():
        if len(resourcelist) >max_size:
            break
        if href not in urllist:
            urllist.append(href)
            workmanager.add_job(do_work,workmanager=workmanager,url=href,max_size=max_size)


def main(workmanager,site,max_size):
    resourcelist.append(site)
    urllist.append(site)
    workmanager.add_job(do_work,workmanager=workmanager,url=site,max_size=max_size)
    time = Timer(workmanager,max_size)
    workmanager.start_thread_pool()
    workmanager.wait_allcomplete()

if __name__ =='__main__':
    site = sys.argv[2]
    max_size = int(sys.argv[4])
    logger = Logger(logname="spider-log", loglevel=1,callfile='spider')
    workmanager = WorkManager()
    main(workmanager,site,max_size)
