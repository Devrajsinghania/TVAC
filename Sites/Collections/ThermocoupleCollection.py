#!/usr/bin/env python3.5
from datetime import datetime

from DataContracts.ThermocoupleContract import ThermocoupleContract

from Logging.Logging import Logging



class ThermocoupleCollection:

    def __init__(self, num = 120):
        Logging.logEvent("Debug","Status Update", 
                {"message": "Creating ThermocoupleCollection",
                 "level": 2})
        self.tcList = self.buildCollection(num)
        self.time = datetime.now()
        self.ValidTCs = []
        self.InvalidTCs = []
        for tc in self.tcList:
            self.updateValidTCs(tc)
        ## TODO add alarms list

    def buildCollection(self, num):
        TCs = []
        for i in range(1, num+1):
            TCs.append(ThermocoupleContract(i))
        return TCs

    def update(self, d):
        '''
        Given a new diciatary of TC data, this will update the 
        collection with the new data
        '''
        if 'time' in d:
            self.time = d['time'] # Start of scan time
        for updateTC in d['tcList']:
            tc = self.getTC(updateTC['Thermocouple'])
            tc.update(updateTC)
            self.updateValidTCs(tc)

    def getTC(self, n):
        for tc in self.tcList:
            if tc.Thermocouple == n:
                return tc
        raise RuntimeError('Thermocouple #: %s is out of range' % n)


    def updateValidTCs(self, tc):
        if tc.working:
            if tc in self.InvalidTCs:
                self.InvalidTCs.remove(tc)
            if tc not in self.ValidTCs:
                self.ValidTCs.append(tc)
        else:
            if tc in self.ValidTCs:
                self.ValidTCs.remove(tc)
            if tc not in self.InvalidTCs:
                self.InvalidTCs.append(tc)

    def getJson(self, temp_units = 'K', whichTCs = 'all'):
        # temp_units values: ['K', 'C', 'F']
        # whichTCs values: ['all', 'Working', 'NotWorking']
        message = []
        message.append('{"time":"%s",' % self.time)
        if whichTCs == 'Working':
            message.append('"TCs":[%s]' %','.join([tc.getJson(temp_units) for tc in self.ValidTCs]))
        elif whichTCs == 'NotWorking':
            message.append('"TCs":[%s]' %','.join([tc.getJson(temp_units) for tc in self.InvalidTCs]))
        else:
            message.append('"TCs":[%s]' %','.join([tc.getJson(temp_units) for tc in self.tcList]))
        message.append('}')
        return ''.join(message)

if __name__ == '__main__':
    tcColl = ThermocoupleCollection(5)
    units = 'K'
    print(' ')
    print(tcColl.getJson())
    print(tcColl.getJson(units,'Working'))
    tcColl.update({'time': datetime.now(), 'tcList': [
        {'Thermocouple': 2, 'temp': 34},
        {'Thermocouple': 4, 'temp': 300, 'working': True}]})
    print(' ')
    print(tcColl.getJson())
    print(tcColl.getJson(units,'Working'))
    print(tcColl.getJson(units,'NotWorking'))
    tcColl.update({'time': datetime.now(), 'tcList': [
        {'Thermocouple': 4, 'temp': 342},
        {'Thermocouple': 3, 'temp': 303, 'working': True}]})
    print(' ')
    print(tcColl.getJson(units,'Working'))
    print(tcColl.getJson())
