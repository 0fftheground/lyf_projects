from flask import Flask, jsonify
from flask import request
from model import get_route_json
from utils import verify_md5_sign
import json
import requests
import logging
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(1)

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

logging.basicConfig(filename='record.log', level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/test')
def hello():
    return 'hello docker&flask'


def do_calculation(j_data):
    flag, result = get_route_json(j_data)
    if flag == 0:
        app.logger.error("calculation failed!")
        app.logger.error(result)
        return 0
    # print(result)
    # daily_url = "https://tms.xsyxsc.com/api/delivery/receiveLocalDeliverySort"
    test_url = "http://0.0.0.0:5000/test"
    try:
        header = {"content-type": "application/json"}
        res = requests.post(test_url, data=result, headers=header)
        app.logger.info(str(res.status_code) + ':' + res.text)
    except Exception as e:
        app.logger.error(" request failed!")
        app.logger.error(e)


@app.route('/xrmRouting', methods=['POST'])
def return_route():
    request_data = request.get_data().decode('utf-8')
    # print(request_data)
    response_result = {}
    try:
        data = json.loads(request_data)
    except:
        response_result['code'] = 1002
        response_result['message'] = 'invalid json data!'
        response_result['data'] = False
        return jsonify(response_result)

    if verify_md5_sign(data['deliveryNo'], data['sign']):

        executor.submit(do_calculation, data)
        response_result['code'] = 1001
        response_result['message'] = 'Request succeeded!'
        response_result['data'] = True
        return jsonify(response_result)

    else:
        app.logger.warning("Sign verification failed!")
        response_result['code'] = 1002
        response_result['message'] = 'Sign verification failed!'
        response_result['data'] = False
        return jsonify(response_result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
