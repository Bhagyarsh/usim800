# from ATRequests import requests
from usim800.Sms import sms
from usim800.Communicate import  communicate
from usim800.Request import request
from usim800.Info import info
import serial

class sim800(communicate):
    TIMMEOUT = 1

    def __init__(self, baudrate, path):
        self.port = serial.Serial(path, baudrate, timeout=sim800.TIMMEOUT)
        super().__init__(self.port)
        self.requests = request(self.port)
        self.info = info(self.port)
        self.sms = sms(self.port)

