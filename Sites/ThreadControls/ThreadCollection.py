import time
import datetime
import time

from Collections.ProfileInstance import ProfileInstance
from Logging.Logging import Logging
from Logging.MySql import MySQlConnect
from ThreadControls.SafetyCheck import SafetyCheck
from ThreadControls.controlStubs.DutyCycleControlStub import DutyCycleControlStub
from ThreadControls.controlStubs.LN2ControlStub import LN2ControlStub
from ThreadControls.controlStubs.VacuumControlStub import VacuumControlStub
from ThreadControls.updaters.PfeifferGaugeUpdater import PfeifferGaugeUpdater
from ThreadControls.updaters.ShiMccUpdater import ShiMccUpdater
from ThreadControls.updaters.ThermoCoupleUpdater import ThermoCoupleUpdater
from ThreadControls.updaters.TsRegistersUpdater import TsRegistersUpdater
from ThreadControls.updaters.TdkLambdaUpdater import TdkLambdaUpdater



class ThreadCollection:

    def __init__(self):
        # self.zoneThreadDict = self.createZoneCollection()
        self.dutyCycleThread = DutyCycleControlStub()
        self.hardwareInterfaceThreadDict = self.createHardwareInterfaces(parent=self)
        self.safetyThread = SafetyCheck(parent=self)

        self.zoneProfiles = ProfileInstance.getInstance().zoneProfiles

        self.runThreads()

        # if there is a half finished profile in the database
        result = self.returnActiveProfile()
        if result:
            print("result: {}".format(result))
            # load up ram (zone collection) with info from the database and the given start time
            self.zoneProfiles.loadProfile(result['profile_name'],result['profile_Start_Time'],result['thermal_Start_Time'],result['first_Soak_Start_Time'])
            # after it's in memory, run it!
            self.runProfile(firstStart = False)
        # end if no active profile
    #end of function 


    def returnActiveProfile(self):
        '''
        A helper function that will look in the DB to see if there is any half finished profile instances
        Returns the profile profile_name and Profile ID if there is, False, False if not
        '''
        sql = "SELECT profile_name, profile_Start_Time, thermal_Start_Time, first_Soak_Start_Time FROM tvac.Profile_Instance WHERE endTime IS NULL;"
        try:
            mysql = MySQlConnect()
            mysql.cur.execute(sql)
            mysql.conn.commit()
        except Exception as e:
            return False, e

        result = mysql.cur.fetchone()
        if not result:
            return False
        return result
        

    def createHardwareInterfaces(self,parent):
        # sending parent for testing, getting current profile data to zone instance
        return {
            1: TsRegistersUpdater(parent=parent),
            2: ThermoCoupleUpdater(parent=parent),
            3: PfeifferGaugeUpdater(),
            4: ShiMccUpdater(),
            # 5: ShiCompressorControlStub)(),
            6: TdkLambdaUpdater(),
            7: LN2ControlStub(ThreadCollection=parent),
            8: VacuumControlStub(),
            }


    def runThreads(self):
        # Starts all the hw threads
        try:
            for key in sorted(self.hardwareInterfaceThreadDict.keys()):
                self.hardwareInterfaceThreadDict[key].daemon = True
                self.hardwareInterfaceThreadDict[key].start()
            self.safetyThread.daemon = True
            self.safetyThread.start()
            self.dutyCycleThread.daemon = True
            self.dutyCycleThread.start()
        except Exception as e:
            Logging.debugPrint(1, "Error in runThreads, ThreadCollections: {}".format(str(e)))
            if Logging.debug:
                raise e



    def addProfileInstancetoBD(self):
        '''
        This is a helper function of runProfile that adds the new profile Instance to the DB
        '''

        coloums = "( profile_name, profile_I_ID, profile_Start_Time )"
        values = "( \"{}\",\"{}\", \"{}\" )".format(self.zoneProfiles.profileName,self.zoneProfiles.profileUUID, datetime.datetime.fromtimestamp(time.time()))
        sql = "INSERT INTO tvac.Profile_Instance {} VALUES {};".format(coloums, values)
        # print(sql)
        mysql = MySQlConnect()
        try:
            mysql.cur.execute(sql)
            mysql.conn.commit()
        except Exception as e:
            return e

        return True


    def runProfile(self, firstStart=True):
        '''
        This assumes a profile is already loaded in RAM, it will start the profile
        Also making an entry in the DB
        '''

        # Check to make sure there is an active profile in memory
        if not self.zoneProfiles.profileName:
            return "{'Error':'No Profile loaded in memory'}"
    
        if firstStart:
            result = self.addProfileInstancetoBD()
            # If there is an error connecting to the DB, return it
            if result != True:
                return result

        # starts all the HWcontrol threads
        try:
            for thread in self.zoneThreadDict:
                if self.zoneThreadDict[thread].zoneProfile.zone > 0:
                    self.zoneThreadDict[thread].running = True
                    self.zoneThreadDict[thread].daemon = True
                    self.zoneThreadDict[thread].start()
                    Logging.logEvent("Debug","Status Update", 
                    {"message": "Zone {} is handled, about the start".format(self.zoneThreadDict[thread].zoneProfile.zone),
                     "level":1})
        except Exception as e:
            pass

        ProfileInstance.getInstance().activeProfile = True

        return "{'result':'success'}"
        


    # TODO: Check to see if we need this?
    # commenting this out because I don't think we need it
    # def runSingleThread(self,data):
    #     thread = data['zone']
    #     if self.zoneThreadDict[thread].handeled:
    #         self.zoneThreadDict[thread] = DutyCycleControlStub(args=(thread,))
    #     self.zoneThreadDict[thread].running = True
    #     self.zoneThreadDict[thread].daemon = True
    #     self.zoneThreadDict[thread].start()

    # TODO Why is this here?
    # def checkThreadStatus(self):
    #     for thread in self.zoneThreadDict:
    #         isAlive = self.zoneThreadDict[thread].is_alive()
    #         handled = self.zoneThreadDict[thread].handeled
    #         # print("{} is {} and is {} handled".format(thread, "ALIVE" if isAlive else "DEAD", "NOT" if not handled else ""))

    def pause(self,data=None):
        self.dutyCycleThread.paused = True

    def removePause(self,data=None):
        self.dutyCycleThread.paused = False

    def holdThread(self,data=None):
        Logging.debugPrint(3,"Holding Zones")
        self.dutyCycleThread.held = True

    def releaseHoldThread(self,data=None):
        self.dutyCycleThread.held = False


    def abortThread(self,data):
        thread = data['zone']
        self.zoneThreadDict[thread].terminate()
        self.zoneThreadDict[thread] = DutyCycleControlStub(args=(thread,))

    # TODO Why is this here?
    # def calculateRamp(self,data):
    #     thread = data['zone']
    #     self.zoneThreadDict[thread].calculateRamp()
