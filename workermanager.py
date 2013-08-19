#coding=utf-8
import Queue
import threading
from logger import Logger
import sys

logger = Logger(logname='thread-log', loglevel=3,callfile='thread')

class WorkManager(object):
    def __init__(self, thread_num=10):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.thread_num = thread_num

    '''
        启动线程
    '''
    def start_thread_pool(self):
        for i in range(self.thread_num):
            worker = Work(self.work_queue)
            worker.setDaemon(True)
            worker.start()
            logger.get_logger.info("one thread start")
            self.threads.append(worker)

    """
        添加一项工作入队
    """
    def add_job(self, func, **kwargs):
        self.work_queue.put((func, kwargs))#任务入队，Queue内部实现了同步机制
    """
        检查剩余队列任务
    """
    def check_queue(self):
        return self.work_queue.qsize()

    def check_thread(self):
        """
            检查剩余线程数
            如果线程数小于给定，且任务量大于线程的十倍，则增加一个线程
        """
        counter = 0
        for thread in self.threads:
            if thread.isAlive():
                counter += 1
        if counter*100 < self.work_queue.qsize and counter < self.thread_num:
            worker = Work(self.work_queue)
            worker.setDaemon(True)
            worker.start()
            logger.get_logger.info("one thread start")
            self.threads.append(worker)
        return counter

    """
        等待所有线程运行完毕
    """   
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()
    '''
        设置超时退出
    '''
    def quit_thread(self):
        for item in self.threads:
            item.join(1)
        sys.exit()

    def clear_queue(self):
        while not self.work_queue.empty():
            self.work_queue.get_nowait()


class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue

    def run(self):
        """
            死循环，从而让创建的线程在一定条件下关闭退出
        """
        while True:
            try:
                if self.work_queue.qsize() < 1:
                    logger.get_logger.info("one thread quit")
                    break
                do, kwargs = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                do(kwargs)
                self.work_queue.task_done()#通知系统任务完成
            except SystemExit:
                return
            except Exception,e:
                if self.work_queue.qsize() < 1:
                    logger.get_logger.info("one thread quit")
                    break
                continue

