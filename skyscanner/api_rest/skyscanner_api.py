import datetime
from model.skyscanner_query import SkyscannerQuery
import modules.combinations_module
from flask_cors import CORS, cross_origin
from flask import Flask, request
import json
import modules.api_module

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/test')
def test():
    date1 = datetime.date(2018, 9, 1)
    date2 = datetime.date(2018, 9, 30)
    sky_query = SkyscannerQuery("spain", "poland", 4, date1, date2, 3)
    matraka = modules.combinations_module.get_trip_list(sky_query)
    order_matraka = sorted(matraka, key=lambda trip: trip.total_price)

    msg = list()
    for trip in order_matraka:
        msg.append("Ida: {} el dia {} - Vuelta: {} el dia {}, cuesta {}€".format(trip.ori_combi, trip.ori_date,
                                                                            trip.dest_combi, trip.dest_date,
                                                                            trip.total_price))
    return json.dump(str(msg))


@app.route('/search', methods=["POST"])
@cross_origin()
def search():

    # Getting data from request
    data = json.loads(request.data)
    ori = data["ori"]
    dest = data["dest"]
    first = datetime.datetime.strptime(data['first-day'], '%Y-%m-%d').date()
    last = datetime.datetime.strptime(data['last-day'], '%Y-%m-%d').date()
    days = int(data["num-days"])
    filter_mode = int(data["filter"])

    sky_query = SkyscannerQuery(ori, dest, days, first, last, filter_mode)
    output = modules.api_module.search_data(sky_query)

    return json.dumps(output)


@app.route('/scrap', methods=['POST'])
@cross_origin()
def scrap():
    print(request.data)
    data = json.loads(request.data)
    modules.api_module.scrap_site(data["site"], data["ori"], data["dest"], data["year"], data["month"])
    return "OK"


def start_api():
    app.run(port=5000, debug=True)