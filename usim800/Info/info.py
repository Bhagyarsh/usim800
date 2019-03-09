from usim800.Parser.ATParser import Parser
import time
from usim800.Communicate import communicate
from usim800.Parser import JsonParser


class info(communicate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._IMEI = None
        self._ModuleVersion = None
        self._RSSI = None
        self._simoprator = None
        self._simostats = None
        self._APN = None
        self._Latitude , self._Longitude = None,None

    @property
    def APN(self):
        return self._APN

    @property
    def Location(self):
        return self._Latitude , self._Longitude


    @APN.setter
    def APN(self,val):
        self._APN = val

    @property
    def IMEI(self):
        return self._IMEI

    @property
    def simoprator(self):
        return self._simoprator

    @property
    def ModuleVersion(self):
        return self._ModuleVersion

    def getoprator(self):
        # https://stackoverflow.com/questions/39930218/sim800-gsm-module-returns-0-on-atcops
        cmd = "AT+CSPN?"
        data = self._send_cmd(cmd, return_data=True)
        try:
            simoprator = data.decode().split(":")[1].split(",")[
                0].replace('"', "")
        except:
            simoprator = None
        self._simoprator = simoprator
        print("simoprator ->", self._simoprator)
        return self._simoprator

    def getModuleVersion(self):
        """
        Get the module firmware version.
        """
        cmd = "AT+CGMR"
        data = self._send_cmd(cmd, return_data=True)
        # print(data)
        try:
            moduleVersion = data.decode().split()[1].split(":")[1].split()[0]
        except:
            moduleVersion = None
        self._ModuleVersion = moduleVersion
        print("ModuleVersion ->", self._ModuleVersion)

    def getIMEI(self):
        """
        Get the IMEI number of the module
        """
        cmd = "AT+GSN"
        data = self._send_cmd(cmd, return_data=True)
        # print(data.decode().split())
        try:
            IMEI = data.decode().split()[1]
        except:
            IMEI = None
        self._IMEI = IMEI
        print("IMEI->", self._IMEI)

    def checkSim(self):
        cmd = "AT+CMEE=2"  # enable the extended error codes to get a verbose format
        self._send_cmd(cmd)
        cmd = "AT+cpin?"
        data = self._send_cmd(cmd, return_data=True,t=2)
       
        try:
            simostats = data.decode().split(":")[1].split()[0]
        except:
            simostats = None
        self._simostats = simostats
        print("_simostats->", self._simostats)

    def getRSSI(self):
        """
        Get the current signal strength in 'bars'
        """
        cmd = "AT+CSQ"
        data = self._send_cmd(cmd, return_data=True)    
        try:
            RSSI = data.decode().split(":")[1].split()[0]
        except:
            RSSI = None
        self._RSSI = RSSI
        print("RSSI->", self._RSSI)
    def getLoctions(self):
        self._bearer(self._APN)
        cmd = "AT+CIPGSMLOC=1,1"
        data = self._send_cmd(cmd, return_data=True)   
        cmd = "AT+CIPGSMLOC=2,1"
        
        data = self._send_cmd(cmd, return_data=True)   
        try:
            
            self._Latitude , self._Longitude = data.decode().split()[1].split(",")[1] ,data.decode().split()[1].split(",")[2]
        except:
            self._Latitude , self._Longitude = None,None

        cmd = "AT +SAPBR=0,1"
        self._send_cmd(cmd)
        print(self._Latitude , self._Longitude )
    def getCBC(self):
        "battery info"
        cmd = "AT+CBC"
        data = self._send_cmd(cmd, return_data=True)  
        battery , voltage =  data.decode().split()[2].split(',')[1] ,data.decode().split()[2].split(',')[2]
        print(battery,int(voltage)/1000)
    
    def all(self):
        self.getCBC()
        self.getLoctions()
        self.getRSSI()
        self.checkSim()
        self.getIMEI()
        self.getModuleVersion()
        self.getoprator()
        
