from access.tesseract import read_image
from services.parser import ReceiptReaderThread
from data.callbackData import CallbackData

#read_image('./testImages/test.jpg', debug=True)

f = open('./testImages/test.jpeg', "rb")
data = CallbackData(
    None, 
    f,
    None
)
th = ReceiptReaderThread(data)
th.start()
th.join()