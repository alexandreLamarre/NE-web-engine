import flask
import os
from src.CommandManager import CommandManager
import asyncio

CACHE = {}
app = flask.Flask("__main__")

async def run_next(command_manager):
    res1,res2 = await command_manager.run_next()

    return (res1,res2)


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
    label_list = []
    sub_labels_and_info_list = []
    label , sublabels_and_info = asyncio.run(run_next(new_command_manager))
    label_list.append(label)
    sub_labels_and_info_list.append(sublabels_and_info)
    while(label, sublabels_and_info) != (None,None):
        label , sublabels_and_info = asyncio.run(run_next(new_command_manager))
        if(label != None and sublabels_and_info!= None):
            label_list.append(label)
            sub_labels_and_info_list.append(sublabels_and_info)

    return flask.jsonify({"labels": label_list, "info": sub_labels_and_info_list})

app.run(debug = True)
