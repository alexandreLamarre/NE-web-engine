"""
Controller for data input from web user
"""

import flask
import os
from src.CommandManager import CommandManager
import asyncio
import multiprocessing

CACHE = {}
app = flask.Flask("__main__")

# async def run_next(command_manager):
#     res1,res2,res3 = await command_manager.run_next()
#
#     return (res1,res2,res3)

def run_next(req, return_dict):
    new_command_manager = CommandManager(req)
    return_dict["labels"], return_dict["sublabels_and_info"], return_dict["errors"] = new_command_manager.run_next()

@app.route("/")
def my_index():
    return "Hello World"

@app.route("/input", methods = ["POST"])
def interpret_command():

    req = flask.request.get_json()

    new_command_manager = CommandManager(req)
    ##TODO clean this up with a getter in CommandManager and Command
    next_commands = [c.original_input for c in new_command_manager.commands_queue]

    label , sublabels_and_frame_info_tuple = new_command_manager.run_initial()

    return flask.jsonify({"label": label, "input": sublabels_and_frame_info_tuple[0][1],\
                                    "interpreted": sublabels_and_frame_info_tuple[1][1],\
                                    "errors": sublabels_and_frame_info_tuple[2][1], \
                                    "commands": next_commands})

@app.route("/input/commands", methods = ["POST"])
def run_commands():

    req = flask.request.get_json()

    new_command_manager = CommandManager(req)
    print(new_command_manager.original_input)
    label_list = []
    sub_labels_and_info_list = []
    error_list = []

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p = multiprocessing.Process(target = run_next, args =(req,return_dict))
    time_limit = 5
    p.start()
    p.join(time_limit)
    if p.is_alive():
        p.terminate()
        p.join()
    label_list.append(return_dict["labels"] if "labels" in return_dict else new_command_manager.Commands_container[0].command)
    sub_labels_and_info_list.append(return_dict["sublabels_and_info"] if "sublabels_and_info" in return_dict else "")
    error_list.append(return_dict["errors"] if "errors" in return_dict else "Computation time exceeded ({} seconds)".format(time_limit))
    # label , sublabels_and_info, errors = new_command_manager.run_next()
    # label_list.append(label)
    # sub_labels_and_info_list.append(sublabels_and_info)
    # error_list.append(errors)


    return flask.jsonify({"labels": label_list, "info": sub_labels_and_info_list, "errors": error_list})

if __name__ == "__true__":
    app.run(debug = True,threaded=False)
