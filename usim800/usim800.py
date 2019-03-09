# from ATRequests import requests
from usim800.Sms import sms
from usim800.Communicate import  communicate
from usim800.Request import request
from usim800.Info import info

class sim800(communicate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests = request(baudrate=self._baudrate,path=self._path)
        self.info = info(baudrate=self._baudrate,path=self._path)
        self.sms = sms(baudrate=self._baudrate,path=self._path)

