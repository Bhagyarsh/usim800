from usim800.Parser.ATParser import Parser
import time
from usim800.Communicate import communicate
from usim800.Parser import JsonParser


class request(communicate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._status_code = None
        self._json = None
        self._text = None
        self._content = None
        self._url = None
        self._IP = None

    def init(self):
        self._status_code = None
        self._json = None
        self._text = None
        self._content = None
        self._url = None
        self._IP = None

    @property
    def text(self):
        return self._text

    @property
    def IP(self):
        return self._IP

    @property
    def APN(self):
        return self._APN

    @APN.setter
    def APN(self, APN):
        self._APN = APN

    @property
    def url(self):
        return self._url

    @property
    def content(self):
        return self._content

    @property
    def status_code(self):
        return self._status_code

    def json(self):
        return self._json

    def get(self, url, header=None):
        self.init()
        self._url = url
        self._IP = self._bearer(self._APN)

        cmd = "AT + HTTPINIT"
        self._send_cmd(cmd)
        cmd = 'AT + HTTPPARA="CID",1'
        self._send_cmd(cmd)

        cmd = 'AT + HTTPPARA="URL","{}"'.format(url)
        self._send_cmd(cmd)
        time.sleep(3)
        cmd = "AT +HTTPACTION=0"

        self._send_cmd(cmd)
        time.sleep(2)
        cmd = "AT +HTTPREAD"
        self._send_cmd(cmd, get_decode_data=True)
        data = self._getdata(
            data_to_decode=[], string_to_decode=None, till=b'\n', count=2, counter=0)
        tk = Parser(data)
        token = tk.tokenizer()
        self._content = tk.parser
        if (len(token) == 4):
            self._status_code = token[2]
            read_bytes = token[3]
            string = self._read_sent_data(int(read_bytes)+1000)
            tk = Parser(string)

            self._content = tk.bytesparser
            self._text = tk.parser
            jph = JsonParser.ATJSONObjectParser(string)
            self._json = jph.JSONObject
        cmd = "AT +SAPBR=0,1"
        self._send_cmd(cmd)

        return self._status_code

    def post(self, url, data, waittime=4000, bytes_data=None, headers=None):
        bytes_data = len(data) +100
        self.init()
        self._url = url
        self._IP = self._bearer(self._APN)
        cmd = "AT+HTTPINIT"
        self._send_cmd(cmd)
        cmd = 'AT+HTTPPARA="CID",1'
        self._send_cmd(cmd)
        cmd = 'AT+HTTPPARA="URL","{}"'.format(url)
        self._send_cmd(cmd)
        cmd = 'AT+HTTPPARA="CONTENT","application/json"'
        self._send_cmd(cmd)
        cmd = 'AT+HTTPDATA={},{}'.format(bytes_data, waittime)
        self._send_cmd(cmd)
        # self.post.write(data)
        self._send_cmd(data)
        time.sleep(4)
        cmd = 'AT+HTTPACTION=1'
        self._send_cmd(cmd)
        time.sleep(4)
        cmd = 'AT+HTTPREAD'
        self._send_cmd(cmd, get_decode_data=True)
        data = self._getdata(
            data_to_decode=[], string_to_decode=None, till=b'\n', count=2, counter=0)
        tk = Parser(data)
        self._content = tk.parser
        token = tk.tokenizer()
        if (len(token) == 4):
            self._status_code = token[2]
            read_bytes = token[3]
            string = self._read_sent_data(int(read_bytes)+1000)
            tk = Parser(string)
            self._content = tk.bytesparser
            self._text = tk.parser
            jph = JsonParser.ATJSONObjectParser(string)
            self._json = jph.JSONObject
        cmd = "AT +SAPBR=0,1"
        self._send_cmd(cmd)

        return self._status_code
