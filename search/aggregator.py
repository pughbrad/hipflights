from Queue import Queue
from threading import Thread
import heapq
import requests

class FlightAggregator(object):
    def __init__(self, url_list):
        self.url_list = url_list
        self.results = []
        self.queue = Queue()

    def search(self):
        return self.get_aggregated_results()
        
    def get_aggregated_results(self):
        for url in self.url_list:
            self.queue.put(url)

        for url in self.url_list:
            t = Thread(target=self.get_provider_results)
            t.Daemon = True
            t.start()

        self.queue.join()

        iterable = heapq.merge(*self.results)
        return {'results': list(iterable)}

    def get_provider_results(self):
        while True:
            url = self.queue.get()
            r = requests.get(url).json()
            self.results.append(r['results'])
            self.queue.task_done()
