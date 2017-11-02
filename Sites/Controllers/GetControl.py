import json

from Collections.ProfileInstance import ProfileInstance
from Collections.HardwareStatusInstance import HardwareStatusInstance
from ThreadControls.ThreadCollectionInstance import ThreadCollectionInstance

from Logging.Logging import Logging

class GetControl:

    def checkTreadStatus(self):
        try:
            threadInstance = ThreadCollectionInstance.getInstance()
            threadInstance.threadCollection.checkThreadStatus()
            return "{'result':'success'}"
        except Exception as e:
            return "{'error':'{}'}".format(e)

    def getAllThermoCoupleData(self):
        Logging.debugPrint(2, "Calling: getAllThermoCoupleData")  #Todo Change to logEvent()
        hardwareStatusInstance = HardwareStatusInstance.getInstance()
        json = hardwareStatusInstance.Thermocouples.getJson('K')
        # print(json)
        return json


    def holdAllZones(self):
        try:
            threadInstance = ThreadCollectionInstance.getInstance()
            threadInstance.threadCollection.holdThread()
            return "{'result':'success'}"
        except Exception as e:
            return "{'error':'{}'}".format(e)

    def pauseAllZones(self):
        try:
            threadInstance = ThreadCollectionInstance.getInstance()
            threadInstance.threadCollection.pause()
            return "{'result':'success'}"
        except Exception as e:
            print("lol")
            return "{'error':'{}'}".format(str(e))

        
    def resumeAllZones(self):
        try:
            threadInstance = ThreadCollectionInstance.getInstance()
            threadInstance.threadCollection.removePause()
            return "{'result':'success'}"
        except Exception as e:
            return "{'error':'{}'}".format(e)

    def unHoldAllZones(self):
        print("!")
        try:
            threadInstance = ThreadCollectionInstance.getInstance()
            threadInstance.threadCollection.releaseHoldThread()
        except Exception as e:
            return "{'error':'{}'}".format(e)
        return "{'result':'success'}"


    def putUnderVacuum(self):
        try:
            ProfileInstance.getInstance().vacuumWanted = True
            return "{'result':'success'}"
        except Exception as e:
            return "{'error':'{}'}".format(e)

    def VacuumNotNeeded(self):
        try:
            profile = ProfileInstance.getInstance()
            if not profile.activeProfile:
                profile.vacuumWanted = False
                return "{'result':'success'}"
            else:
                return "{'result':'Not Changed: Active Profile Running.'}"

        except Exception as e:
            return "{'error':'{}'}".format(e)

    def getAllZoneData(self):
        # This doesn't work...
        Logging.debugPrint(2, "Calling: getAllZoneData")  #Todo Change to logEvent()
        profileInstance = ProfileInstance.getInstance()
        zones = profileInstance.zoneProfiles.zoneDict
        json = "{"
        for zone in zones:
            print(zones[zone].getJson())
        return "{'result':'success'}"

    def getLastError(self):
        # data unused
        Logging.debugPrint(2,"Calling: Get Last Err")  #Todo Change to logEvent()
        errorList = ThreadCollectionInstance.getInstance().threadCollection.safetyThread.errorList
        tempErrorList = dict(time=[],event=[],item=[],itemID=[],details=[],actions=[])
        for i, error in enumerate(errorList):
            tempErrorList['time'].append(error['time'])
            tempErrorList['event'].append(error['event'])
            tempErrorList['item'].append(error['item'])
            tempErrorList['itemID'].append(error['itemID'])
            tempErrorList['details'].append(error['details'])
            tempErrorList['actions'].append(error['actions'])

            errorList.pop(i)

        return json.dumps(tempErrorList)

    def hardStop(self):
        try:
            Logging.debugPrint(1,"Hard stop has been called")
            d_out = HardwareStatusInstance.getInstance().PC_104.digital_out
            ProfileInstance.getInstance().activeProfile = False
            d_out.update({"IR Lamp 1 PWM DC": 0})
            d_out.update({"IR Lamp 2 PWM DC": 0})
            d_out.update({"IR Lamp 3 PWM DC": 0})
            d_out.update({"IR Lamp 4 PWM DC": 0})
            d_out.update({"IR Lamp 5 PWM DC": 0})
            d_out.update({"IR Lamp 6 PWM DC": 0})
            d_out.update({"IR Lamp 7 PWM DC": 0})
            d_out.update({"IR Lamp 8 PWM DC": 0})
            d_out.update({"IR Lamp 9 PWM DC": 0})
            d_out.update({"IR Lamp 10 PWM DC": 0})
            d_out.update({"IR Lamp 11 PWM DC": 0})
            d_out.update({"IR Lamp 12 PWM DC": 0})
            d_out.update({"IR Lamp 13 PWM DC": 0})
            d_out.update({"IR Lamp 14 PWM DC": 0})
            d_out.update({"IR Lamp 15 PWM DC": 0})
            d_out.update({"IR Lamp 16 PWM DC": 0})

            HardwareStatusInstance.getInstance().TdkLambda_Cmds.append(['Platen Duty Cycle', 0])
            Logging.logEvent("Event","Profile",
                {"message": "Profile Halted:",
                "ProfileInstance": ProfileInstance.getInstance()})
            return {'result':'success'}
        except Exception as e:
            return {'result':'{}'.format(e)}

    def getShiTemps(self):
        return HardwareStatusInstance.getInstance().ShiCryopump.mcc_status.get_json_plots()


    def getEventList(self):
        # data unused
        Logging.debugPrint(2,"Calling: Get Event List")
        eventList = ProfileInstance.getInstance().systemStatusQueue
        # eventList.append({"time":str(datetime.now()),
        #                 "category":"System",
        #                 "message":"This is a test event"})
        tempEventList = dict(time=[],category=[],message=[])
        for i, event in enumerate(eventList):
            tempEventList['time'].append(event['time'])
            tempEventList['category'].append(event['category'])
            tempEventList['message'].append(event['message'])

            eventList.pop(i)
        Logging.debugPrint(2, "Events :" + str(eventList))

        return json.dumps(tempEventList)
    
    def getCryoPump_Status(self):
        return HardwareStatusInstance.getInstance().ShiCryopump.getJson_Status()

    def getCryoPump_Params(self):
        return HardwareStatusInstance.getInstance().ShiCryopump.getJson_Params()

    def getCryoPump_plots(self):
        return HardwareStatusInstance.getInstance().ShiCryopump.get_json_plots()

    def getPC104_Digital(self):
        pins = HardwareStatusInstance.getInstance().PC_104
        return '{"out":%s,"in bits":%s,"in sw":%s,"sw wf":%s}' % (
            pins.digital_out.getJson(),
            pins.digital_in.getJson_bits(),
            pins.digital_in.getJson_Switches(),
            pins.digital_in.getJson_Switches_WF())

    def getPC104_Switches(self):
        pins = HardwareStatusInstance.getInstance().PC_104
        return '{"in sw":%s,"sw wf":%s}' % (
            pins.digital_in.getJson_Switches(),
            pins.digital_in.getJson_Switches_WF())

    def getPC104_Analog(self):
        pins = HardwareStatusInstance.getInstance().PC_104
        return '{"out":%s,"in":%s}' % (pins.analog_out.getJson(),
                                       pins.analog_in.getJson())

    def getPressureGauges(self):
        gauges = HardwareStatusInstance.getInstance().PfeifferGuages
        resp = {'CryoPressure': gauges.get_cryopump_pressure(),
                'ChamberPressure': gauges.get_chamber_pressure(),
                'RoughingPressure': gauges.get_roughpump_pressure()}
        return json.dumps(resp)

    def getZoneTemps(self):
        temps=dict(ZoneTemps=[])

        for i in range(1,10):
            strzone="zone"+str(i)
            try:    
                temps['ZoneTemps'].append(ProfileInstance.getInstance().zoneProfiles.getZone(strzone).getTemp())
            except Exception as e:
                temps['ZoneTemps'].append(float('nan'))

            try:
                temps['ZoneTemps'].append(ThreadCollectionInstance.getInstance().threadCollection.dutyCycleThread.zones["zone{}".format(i)].pid.SetPoint)
            except Exception as e:
                temps['ZoneTemps'].append(float('nan'))

        buff=json.dumps(temps)
        return buff                        

    def runProfile(self):
        threadInstance = ThreadCollectionInstance.getInstance()
        result = threadInstance.threadCollection.runProfile()
        return result

    def recordData(self):
        ProfileInstance.getInstance().recordData = True

    def StoprecordData(self):
        ProfileInstance.getInstance().recordData = False

    def doRegen(self):
        try:
            pass
            return "{'result':'success'}"
        except Exception as e:
            return "{'error':'{}'}".format(e)

    def getVacuumState(self):
        return json.dumps({"VacuumState": HardwareStatusInstance.getInstance().VacuumState})

    def getTvacStatus(self):
        gauges = HardwareStatusInstance.getInstance().PfeifferGuages
        out = {
            "recordData": ProfileInstance.getInstance().recordData,
            "OperationalVacuum": HardwareStatusInstance.getInstance().OperationalVacuum,
            "activeProfile": ProfileInstance.getInstance().activeProfile,
            "vacuumWanted": ProfileInstance.getInstance().vacuumWanted,
            "currentSetpoint": ProfileInstance.getInstance().currentSetpoint,
            "inRamp": ProfileInstance.getInstance().inRamp,
            "inHold": ProfileInstance.getInstance().inHold,
            "inPause": ProfileInstance.getInstance().inPause,
            'CryoPressure': gauges.get_cryopump_pressure(),
            'ChamberPressure': gauges.get_chamber_pressure(),
            'RoughingPressure': gauges.get_roughpump_pressure(),
            "ChamberPowerLockoutPressure": HardwareStatusInstance.getInstance().ChamberPowerLockout,
            }
        return json.dumps(out)
