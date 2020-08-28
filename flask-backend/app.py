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

def run_next(req, queue):
    new_command_manager = CommandManager(req)
    label,info, error = new_command_manager.run_next()
    queue.put(label)
    queue.put(info)
    queue.put(error)
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
    queue = manager.Queue()
    p = multiprocessing.Process(target = run_next, args =(req,queue))
    time_limit = 5
    p.start()
    p.join(time_limit)
    if p.is_alive():
        p.terminate()
        p.join()
    label_list.append(queue.get() if queue.empty() == False else new_command_manager.Commands_container[0].command.upper())
    sub_labels_and_info_list.append(queue.get() if queue.empty() == False else "")
    error_list.append(queue.get() if queue.empty() == False else "Computation time exceeded ({} seconds)".format(time_limit))
    # label , sublabels_and_info, errors = new_command_manager.run_next()
    # label_list.append(label)
    # sub_labels_and_info_list.append(sublabels_and_info)
    # error_list.append(errors)


    return flask.jsonify({"labels": label_list, "info": sub_labels_and_info_list, "errors": error_list})

if __name__ == "__true__":
    app.run(debug = True,threaded=False)
