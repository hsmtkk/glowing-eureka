import json
import logging
import os

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")

    # log
    query_str = request.query_string.decode()
    app.logger.info("query string: " + query_str)
    app.logger.info(json.dumps({"query_string": query_str}))

    return "Hello {}!".format(name)

if __name__ == "__main__":
    port=int(os.environ.get("PORT", "8080"))
    if "DEBUG" in os.environ:
        logging.basicConfig(level=logging.DEBUG)
        app.run(debug=True, host="0.0.0.0", port=port)
    else:
        app.run(host="0.0.0.0", port=port)
