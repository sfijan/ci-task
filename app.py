from flask import Flask
from models import Player, database
import json
from playhouse.shortcuts import model_to_dict, dict_to_model

database.connect()

app = Flask(__name__)

@app.route("/player", methods=['GET'])
def player():
    player = Player.select().get()
    return json.dumps(model_to_dict(player), indent=4, default=str)

