from flask import Flask, request
from services.parser import ReceiptReaderThread
from data.callbackData import CallbackData
from uuid import uuid4
import json

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/parse', methods=['POST'])
def acceptFile():
    file = request.files['file']
    data = request.form

    isAsync = int(data.get("isAsync", 0))
    url = data.get("url", None)
    uuid = data.get("uuid", str(uuid4()))

    if file and allowed_file(file.filename):
        data = CallbackData(
            url if isAsync else None, 
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
    res = request.get_json()
    return res

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5001, debug=True)