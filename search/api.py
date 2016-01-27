from bottle import Bottle, response, run 
#from aggregator import get_aggregated_results
from aggregator import FlightAggregator
import json

app = Bottle()

source_urls = [
    "http://localhost:9000/scrapers/Expedia",
    "http://localhost:9000/scrapers/Orbitz",
    "http://localhost:9000/scrapers/Priceline",
    "http://localhost:9000/scrapers/Travelocity",
    "http://localhost:9000/scrapers/United",
]


@app.route("/flights/search", ["GET"])
def test():
    response.content_type = "application/json"
    aggregator = FlightAggregator(source_urls)
    results = aggregator.search()
    return json.dumps(results)


def self_hosted_run():
    host = "0.0.0.0"
    port = 8000
    run(app, host=host, port=port, reloader=True)


if __name__ == "__main__":
    self_hosted_run()

