import flask

app = flask.Flask("__main__")

@app.route("/")
def my_index():
    return "Hello World"

app.run(debug = True)