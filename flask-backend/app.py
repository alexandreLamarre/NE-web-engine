import flask
import os
from src.CommandManager import CommandManager

app = flask.Flask("__main__")

@app.route("/")
def my_index():
    return "Hello World"

@app.route("/input/<string:commands>")
def interpret_command(commands):
    new_command_manager = CommandManager(commands)

    label , sublabels_and_frame_info_tuple = new_command_manager.run_initial()
    resp = {"input": [label, sublabels_and_frame_info_tuple] }
    return flask.jsonify(resp)

app.run(debug = True)
