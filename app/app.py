import json
import logging
import os

from flask import Flask, request

app = Flask(__name__)

logger = logging.getLogger(__name__)

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    logger.info("query string: " + request.query_string)
    logger.info(json.dumps({"query_string": request.query_string}))
    return "Hello {}!".format(name)

if __name__ == "__main__":
    if "DEBUG" in os.environ:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)
    port=int(os.environ.get("PORT", "8080"))
    app.run(debug=True, host="0.0.0.0", port=port)
