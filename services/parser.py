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
        self.data = None
        self.done = False
        img = cv2.imdecode(numpy.fromstring(
            cb.fileContent.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

        self.text = read_image(img)

    def makeRequest(self):
        if not self.done or not self.cb.url:
            return

        r = requests.post(self.cb.url, data={
            "uuid": self.cb.uuid,
            **self.data
        })

        if r.status_code != 200:
            ...

    def getCompletedData(self):
        if (not self.done):
            raise Exception("Not yet done")

        return self.data

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

        self.data = data
        self.done = True

        self.makeRequest()
