from flask import Flask
from flask import request
from model import get_route_json
from utils import verify_md5_sign
import json
import requests

app = Flask(__name__)


@app.route('/test', methods=['POST'])
def return_route():
    request_data = request.get_data().decode('utf-8')
    print(request_data)
    data = json.loads(request_data)
    if verify_md5_sign(data['deliveryNo'], data['sign']):
        result = get_route_json(data)
        print(result)
        # requests.post(url, data=result)
        return result
    else:
        return 'Sign verification failed!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
