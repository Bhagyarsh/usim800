
from usim800.Communicate import communicate

def _try_decode_utf16_encoded_string(s):
    # Check if the input string is a valid UTF-16 hex string. If it is, decode it. Otherwise, return it as-is. 
    #   is_utf16_encoded_string('60A87684') == '您的'
    #   is_utf16_encoded_string('hello') == 'hello'
    # Recolic K <root@recolic.net>
    prepared = s.strip().lower()
    if len(prepared) % 4 != 0:
        return s
    for c in prepared:
        if c not in '0123456789abcdef':
            return s
    # It is an utf16 encoded string. Let's decode it. 
    result_str = ''
    for i in range(len(prepared)//4):
        decoded_char = chr(int(prepared[i*4:(i+1)*4], 16))
        result_str += decoded_char
    return result_str



def _parse_cmgl_response(cmgl_response_str):
    # There is usually many lines in the response, and there may be duplicate entries and useless prefix&postfix. 
    # This function will trim these useless prefix/postfix, and parse the response. 
    # Recolic K <root@recolic.net>

    ENTRY_HEADLINE_PREFIX = '+CMGL: '
    # List entry headline format: ENTRY_HEADLINE_PREFIX ID ," READ_OR_UNREAD "," NUMBER ",""," DATETIME "
    result_dict = {}
    curr_entry = None
    for line in cmgl_response_str.replace('\r','\n').split('\n'):
        if line.startswith(ENTRY_HEADLINE_PREFIX):
            # New entry starts! End the previous entry and parse the new one. 
            if curr_entry is not None:
                result_dict[curr_entry[0]] = (curr_entry)
                curr_entry = None
            
            headline_fields = line.split(',"') # DATETIME string contains ','
            if len(headline_fields) != 5:
                print('Warning: Command AT+CMGL response is invalid. Expecting 5 fields in headline, but actually got {}. Skipping this bad response...'.format(len(headline_fields)))
                continue
            headline_fields = [f.strip('"') for f in headline_fields]
            msg_id = headline_fields[0][len(ENTRY_HEADLINE_PREFIX):]

            # Parsed. Now fill the curr_entry
            curr_entry = headline_fields
            curr_entry[0] = msg_id
            curr_entry.append('') # Body text
        else:
            # This line might be body of an entry, might be junk data. 
            if curr_entry is None:
                continue
            if line.strip() == '':
                continue
            if line.strip().lower() == 'ok':
                break
            # Not junk... Let's add text to curr_entry
            curr_entry[-1] += _try_decode_utf16_encoded_string(line) + '\n'

    # Exiting loop. Add the last entry to result! 
    if curr_entry is not None:
        result_dict[curr_entry[0]] = (curr_entry)
    return result_dict
 

class sms(communicate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send(self, number, sms):
        cmd = "AT"
        self._send_cmd(cmd)
        cmd = "AT+CMGF=1"
        # Sets the GSM Module in Text Mode
        self._send_cmd(cmd)
        cmd = 'AT+CMGS="{}"'.format(number)
        self._send_cmd(cmd)
        SMS = sms
        self._send_cmd(SMS,t=0.5)
        cmd = "\x1A"
        self._send_cmd(cmd,t=0.1)
        cmd = "AT +SAPBR=0,1"
        data = self._send_cmd(cmd,return_data=True,t=0.5)
        try:
            stats = (data.decode().split()[-1])
            if "OK" in stats:
                stats = True
        except:
            stats = False
        return stats

    def readAll(self,index=None):
        # Sample Usage: 
        #   from usim800 import sim800
        #   gsm = sim800(baudrate=9600,path="/dev/ttyUSB0")
        #   res_dict = gsm.sms.readAll()
        #   for k in res_dict:
        #       print(res_dict[k])

        cmd = "AT"
        self._send_cmd(cmd)
        cmd = "AT+CMGF=1"
        # Sets the GSM Module in Text Mode
        self._send_cmd(cmd)
        cmd = 'AT+CMGL="ALL"'
        # Sets the GSM Module in Text Mode
        self._send_cmd(cmd,read=False)
        data = self._readtill("OK")
        return _parse_cmgl_response(data)

    def deleteAllReadMsg(self,index=None):
        # Delete all read message. Leave unread message and outgoing message untouched. 
        # You can provide the index of ANY existing message to make this function runs faster. 

        # API forces you to provide an index. So we must readAll()
        if index is None:
            msgs = self.readAll()
            if len(msgs) == 0:
                return
            index = list(msgs.keys())[0]
        if not isinstance(index, str):
            index = str(index)

        cmd = "AT"
        self._send_cmd(cmd)
        cmd = "AT+CMGD=" + index + ",1"
        # Sets the GSM Module in Text Mode
        self._send_cmd(cmd)


