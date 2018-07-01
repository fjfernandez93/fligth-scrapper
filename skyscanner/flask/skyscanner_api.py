import datetime
from model.skyscanner_query import SkyscannerQuery
import modules.combinations_module
from flask_cors import CORS, cross_origin
from flask import Flask

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
    return str(msg)


@app.route('/')
@cross_origin()
def index():
    return "Hola amic"


if __name__ == '__main__' :
    app.run(port=5000, debug=True)