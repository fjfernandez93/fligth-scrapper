import datetime
from model.skyscanner_query import SkyscannerQuery
import modules.combinations_module
from flask_cors import CORS, cross_origin
from flask import Flask, request
import json
import threading
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


@app.route('/testPost',methods=["POST"])
@cross_origin()
def test_post():

    data = json.loads(request.data)

    print(request.data)

    # ori = request.form['ori']
    # dest = request.form['dest']
    # first = datetime.datetime.strptime(request.form['first-day'], '%Y-%m-%d').date()
    # last = datetime.datetime.strptime(request.form['last-day'], '%Y-%m-%d').date()
    # days = int(request.form['num-days'])
    ori = data["ori"]
    dest = data["dest"]
    first = datetime.datetime.strptime(data['first-day'], '%Y-%m-%d').date()
    last = datetime.datetime.strptime(data['last-day'], '%Y-%m-%d').date()
    days = int(data["num-days"])
    filter = int(data["filter"])

    #print(ori, dest, days, first.month, last.month)

    sky_query = SkyscannerQuery(ori, dest, days, first, last, filter)
    matraka = modules.combinations_module.get_trip_list(sky_query)
    #print(sky_query.ori, sky_query.dest, sky_query.first_day, sky_query.last_day, sky_query.length, sky_query.filter_mode)
    #print(len(sky_query.trip_list))
    order_matraka = sorted(matraka, key=lambda trip: trip.total_price)

    msg = list()
    output = list()
    for trip in order_matraka:
        msg.append("Ida: {} el dia {} - Vuelta: {} el dia {}, cuesta {}€".format(trip.ori_combi, trip.ori_date,
                                                                                 trip.dest_combi, trip.dest_date,trip.total_price))
        output.append({
            "trip1": str(trip.ori_combi),
            "day1": str(trip.ori_date),
            "trip2": str(trip.dest_combi),
            "day2": str(trip.dest_date),
            "price": trip.total_price,

        })

    #return str([["hola", "adios"]])
    return json.dumps(output)


@app.route('/scrap', methods=['POST'])
@cross_origin()
def scrap():
    print(request.data)
    data = json.loads(request.data)
    #modules.api_module.scrap_site(data["site"], data["ori"], data["dest"], data["year"], data["month"])
    return "OK"


@app.route('/loki', methods=['POST'])
@cross_origin()
def loki():
    print(request.data)
    #data = json.loads(request.data)
    #modules.api_module.scrap_site(data["site"], data["ori"], data["dest"], data["year"], data["month"])
    output = {"result": "ok"}
    return json.dumps(output)


def start_api():
    app.run(port=5000, debug=True)