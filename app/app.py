import json
import logging
import os

import googlecloudprofiler

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

    debug=False
    if "DEBUG" in os.environ:
        debug=True
        logging.basicConfig(level=logging.DEBUG)

    try:
        googlecloudprofiler.start(service='example')
    except Exception as e:
        app.logger.error("failed to start Google Cloud Profiler: " + str(e))

    app.run(debug=debug, host="0.0.0.0", port=port)