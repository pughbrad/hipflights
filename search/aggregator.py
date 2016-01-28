from Queue import Queue
#import threading
from threading import Thread
import heapq
import requests
import logging

class FlightAggregator(object):
    def __init__(self, url_list):
        logging.debug('new FlightAggregator')
        self.url_list = url_list
        self.results = []
        self.queue = Queue()

    def search(self):
        return self.get_aggregated_results()
        
    def get_aggregated_results(self):
        for url in self.url_list:
            self.queue.put(url)

        #thread_list = []

        # start a thread for each url
        for url in self.url_list:
            t = Thread(target=self.get_provider_results)
            #thread_list.append(t)
            t.Daemon = True
            t.start()

        self.queue.join()

        iterable = heapq.merge(*self.results)
        return {'results': list(iterable)}

    def get_provider_results(self):
        try:
            url = self.queue.get()
            r = requests.get(url).json()
            self.results.append(r['results'])
            self.queue.task_done()
        except Exception as e:
            logging.error(str(e))
