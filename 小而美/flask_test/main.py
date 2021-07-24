from flask import Flask

app = Flask(__name__)


@app.route('/mtest', methods=['POST'])
def hello():
    return ' hello docker&flask'


if __name__ == '__main__':
    app.run(debug= True, port=2021, host='0.0.0.0')
