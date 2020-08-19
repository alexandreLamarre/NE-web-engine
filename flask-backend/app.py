import flask
import os
from src.CommandManager import CommandManager

app = flask.Flask("__main__")

@app.route("/")
def my_index():
    return "Hello World"

@app.route("/input/<commands>")
def interpret_command(commands):

    new_command_manager = CommandManager(commands)
    #
    label , sublabels_and_frame_info_tuple = new_command_manager.run_initial()
    # resp = {"input": [label, sublabels_and_frame_info_tuple] }
    # res = flask.make_response(flask.jsonify({"message":"Ok"}),200)
    return flask.jsonify({"label": label, "interpreted": sublabels_and_frame_info_tuple[0],\
                                    "uninterpreted": sublabels_and_frame_info_tuple[1],\
                                    "Errors": sublabels_and_frame_info_tuple[2]})

app.run(debug = True)
