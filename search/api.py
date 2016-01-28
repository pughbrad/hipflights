from bottle import Bottle, response, run 
from aggregator import FlightAggregator
#from threading import Thread
import logging
import json

logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

app = Bottle()

source_urls = [
    "http://localhost:9000/scrapers/Expedia",
    "http://localhost:9000/scrapers/Orbitz",
    "http://localhost:9000/scrapers/Priceline",
    "http://localhost:9000/scrapers/Travelocity",
    "http://localhost:9000/scrapers/United",
]


@app.route("/flights/search", ["GET"])
def search():
    logging.debug('/flights/search')
    response.content_type = "application/json"
    aggregator = FlightAggregator(source_urls)
    results = aggregator.search()
    return json.dumps(results)


def self_hosted_run():
    host = "0.0.0.0"
    port = 8000

    try:
        run(app, host=host, port=port)
    except KeyboardInterrupt as e:
        print 'keyboard interrupt\n'


def self_hosted_thread(host, port):
        run(app, host=host, port=port)

if __name__ == "__main__":
    self_hosted_run()
