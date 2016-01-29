from Queue import Queue
from threading import Thread
import heapq
import requests
import logging

class FlightAggregator(object):
    def __init__(self, url_list):
        logging.debug('new FlightAggregator')
        self.url_list = url_list
        self.flights = []
        self.queue = Queue()

    def search(self):
        return self.get_aggregated_results()
        
    def get_aggregated_results(self):
        for url in self.url_list:
            self.queue.put(url)

        # start a thread for each url
        for url in self.url_list:
            t = Thread(target=self.get_provider_results)
            t.Daemon = True
            t.start()

        self.queue.join()
        # unpack tuple, throw out leading 'agony' value 
        flights = [t[1] for t in heapq.merge(*self.flights)]
        return {'results': flights} 

    def get_provider_results(self):
        try:
            url = self.queue.get()
            flights = requests.get(url).json()['results']

            # create tuple (agony, flight) for each flight to aid later merge
            self.flights.append([(f['agony'], f) for f in flights])
            self.queue.task_done()

        except Exception as e:
            logging.error(str(e))
