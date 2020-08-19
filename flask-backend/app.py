import flask
import os
from src.CommandManager import CommandManager

CACHE = {}
app = flask.Flask("__main__")

@app.route("/")
def my_index():
    return "Hello World"

@app.route("/input", methods = ["POST"])
def interpret_command():

    req = flask.request.get_json()

    new_command_manager = CommandManager(req)
    #
    label , sublabels_and_frame_info_tuple = new_command_manager.run_initial()

    return flask.jsonify({"label": label, "interpreted": sublabels_and_frame_info_tuple[0][1],\
                                    "uninterpreted": sublabels_and_frame_info_tuple[1][1],\
                                    "Errors": sublabels_and_frame_info_tuple[2][1]})

@app.route("/input/commands", methods = ["POST"])
def run_commands():

    req = flask.request.get_json()

    new_command_manager = CommandManager(req)
    #
    label , sublabels_and_frame_info_tuple = new_command_manager.run_next()
    while(label, sublabels_and_frame_info_tuple) != (None,None):
        label , sublabels_and_frame_info_tuple = new_command_manager.run_next()

    return flask.jsonify({"commmands": None})

app.run(debug = True)
