from flask import Flask, request
from services.parser import ReceiptReaderThread
from data.callbackData import CallbackData
from uuid import uuid4

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/parse', methods=['POST'])
def acceptFile():
    _ = request.data
    file = request.files['file']
    data = request.form

    isAsync = int(data.get("isAsync", 0))
    url = data.get("url", None)
    uuid = data.get("uuid", str(uuid4()))
    header = data.get("additionalHeaders", None)

    if file and allowed_file(file.filename):
        data = CallbackData(
            url if isAsync else None,
            header if isAsync else None,
            file,
            uuid
        )
        th = ReceiptReaderThread(data)
        th.start()

        if (isAsync):
            return {"message": "processing started"}
        else:
            th.join()
            return th.getCompletedData()


@app.route('/echo', methods=['POST'])
def testCB():
    res = {
        "body": request.get_json(),
        "header": str(request.headers),
    }
    return res

@app.route('/', methods=['GET'])
def testHello():
    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)
