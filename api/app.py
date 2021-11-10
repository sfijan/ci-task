from flask import Flask, request, abort
from models import Player, database
import json
from playhouse.shortcuts import model_to_dict, dict_to_model

app = Flask(__name__)
database.connect()

def to_json(player):
    return json.dumps(model_to_dict(player), indent=4, sort_keys=True, default=str)

@app.route("/player", methods=['POST', 'GET'])
@app.route("/player/<player_id>", methods=['GET', 'PUT', 'DELETE'])
def player(player_id=None):
    if request.method == 'GET':
        if player_id:
            try:
                player = Player.get_by_id(player_id)
            except:
                abort(404)
            return to_json(player)
        else:
            s = '['
            for p in Player.select():
                s += to_json(p) + ','
            if s[-1] == ',':
                s = s[:-1]
            s += ']'
            return s

    elif request.method == 'POST':
        player = Player.create(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            current_club=request.form['current_club'],
            nationality=request.form['nationality'],
            dob=request.form['dob'],
            preffered_pos=request.form['preffered_pos']
        )
        return to_json(player)

    elif request.method == 'PUT':
        try:
            player_dict = model_to_dict(Player.get_by_id(player_id))
            fields = list(player_dict.keys())
            fields.remove('player_id')
        except:
            abort(404)

        for field in request.form.keys():
            if field in fields:
                player_dict[field] = request.form[field]
            else:
                abort(400)

        player = dict_to_model(Player, player_dict)
        player.save()
        return to_json(player)

    elif request.method == 'DELETE':
        try:
            Player.get_by_id(player_id).delete_instance()
        except:
            abort(404)
        return '', 204

