import threading
import requests
import cv2
import numpy

from receiptparser.config import read_config
from receiptparser.receipt import Receipt
from data.callbackData import CallbackData
from access.tesseract import read_image

config = read_config('./config/config.yml')

class ReceiptReaderThread(threading.Thread):
    def __init__(self, cb: CallbackData):
        threading.Thread.__init__(self)
        self.cb = cb
        img = cv2.imdecode(numpy.fromstring(
            cb.fileContent.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

        self.text = read_image(img)

    def run(self):
        receipt = Receipt.from_text(config, self.text)

        data = {
            "uuid": self.cb.uuid,
            "name": receipt.filename,
            "company": receipt.company,
            "postal": receipt.postal,
            "date": receipt.date,
            "sum": receipt.sum
        }

        print(data)

        if self.cb.url:
            r = requests.post(url=self.cb.url, data=data)
            status = r.status_code
            if (status != 200):
                ...
