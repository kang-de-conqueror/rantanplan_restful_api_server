from flask import Flask, jsonify, request
import flask_monitoringdashboard as dashboard
from utils.general_util import GeneralUtil
from utils.my_connection import MyConnection
from daos.place_dao import PlaceDAO

app = Flask(__name__)
dashboard.bind(app)



@app.route("/")
def hello():
    return "Welcome to Rantanplan server"


@app.route("/place/signal", methods=['POST'])
def post_unidentified_place():
    try:
        id = GeneralUtil.generate_32_chars_string()
        dao = PlaceDAO()
        if (dao.add_signal_identified_place(id, request.json)):
            return jsonify({
                "place_id": id
            })
        else:
            return jsonify({
                "place_id": None
            })
    except Exception as e:
        return jsonify({
            "message": str(e)
        })


@app.route("/place/<string:id>/signal", methods=['POST'])
def post_identified_place(id):
    try:
        dao = PlaceDAO()
        if (dao.add_signal_existed_place(id, request.json)):
            return jsonify({
                "place_id": id
            })
        else:
            return jsonify({
                "place_id": None
            })
    except Exception as e:
        return jsonify({
            "message": str(e)
        })


@app.route("/place/search", methods=['POST'])
def post_search_place():
    try:
        signal_list = list(request.json)
        if not signal_list or len(signal_list) == 0:
            return jsonify({
                "message": "List input not valid"
            })
        dao = PlaceDAO()
        map_place = {}
        map_place_signal = {}
        for signal in signal_list:
            dao.search_place(signal, map_place, map_place_signal)
        if len(map_place_signal) == 0:
            return jsonify([])

        match_place_list = []
        for index, (key, value) in enumerate(map_place_signal.items()):
            match_place_list.append({
                "place_id": key,
                "place_name": map_place[key].name,
                "place_address": map_place[key].address,
                "score": len(value) / len(signal_list)
            })
        return jsonify(match_place_list)
    except Exception as e:
        return jsonify({
            "message": str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)
