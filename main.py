import flask
import os
from flask import request, json
from controllers import mainController
from util import queryFilter
from database import database

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    env = os.environ.get("ENV")
    ping = database.ping()
    return 'Healthcheck ok! \nEnvironment: ' + env + '\nPing Status: ' + str(ping)


@app.route('/crawl', methods=['GET'])
def home():
    query = request.args.get('query')
    maximum = request.args.get('maximum')
    note = request.args.get('note')

    print('Starting execution...')

    queryValidation = queryFilter.verify(query)

    if queryValidation == False:
        return 'Error on filter', 404

    returnValue = mainController.exec(query, maximum, note)

    if returnValue == 0:
        return 'Error on crawling', 500

    print('Done execution!')

    return returnValue, 200


if __name__ == '__main__':
    app.run()
