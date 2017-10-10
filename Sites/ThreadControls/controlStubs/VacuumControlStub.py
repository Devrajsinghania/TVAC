from threading import Thread
import json
import uuid
import time
import datetime
import sys
import os


from Collections.ProfileInstance import ProfileInstance
from Collections.HardwareStatusInstance import HardwareStatusInstance

from Logging.MySql import MySQlConnect
from Logging.Logging import Logging


class VacuumControlStub(Thread):
    '''
    This class contains the main inteligences for getting and keeping the test chaber under vacuum,
    '''

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):

        Logging.logEvent("Debug","Status Update", 
        {"message": "Creating VacuumControlStub:",
         "level": 3})

        Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs

        self.zoneProfiles = ProfileInstance.getInstance().zoneProfiles
        self.hw = HardwareStatusInstance.getInstance()
        self.state = None
        self.oldState = True

        self.updatePeriod = 2


    def run(self):
        # While true to restart the thread if it errors out
        while True:
            # This has no startup, but should wait until all drivers and updaters are running
            Logging.logEvent("Event","Thread Start",
                {"thread": "VacuumControlStub",
                 "ProfileInstance": ProfileInstance.getInstance()})
            Logging.logEvent("Debug","Status Update",
                {"message": "Starting VacuumControlStub",
                 "level":2})
            
            # TODO: change this to a while not ready, sleep 1
            time.sleep(1)
            try:
               while True:
                    if (ProfileInstance.getInstance().activeProfile or
                        ProfileInstance.getInstance().vacuumWanted) and \
                            self.hw.PfeifferGuages.get_roughpump_pressure() is not None:
                        # With an active profile, we start putting the system under pressure
             
                        # Logging.logEvent("Debug","Status Update", 
                        # {"message": "Running Vacuum Control Stub",
                        #  "level":2})
                        # Setup code is here
                        if self.state:
                            self.oldState = self.state

                        # connection to the MCC
                        # JK, it's already done in the MCC control stub

                        # Reading of pressure gauges, to figure out where the system is

                        # When you know what the pressure is, you know what to do go get into pressure
                        self.cryoPumpPressure = self.hw.PfeifferGuages.get_cryopump_pressure()
                        self.chamberPressure = self.hw.PfeifferGuages.get_chamber_pressure()
                        self.roughPumpPressure = self.hw.PfeifferGuages.get_roughpump_pressure()

                        # learning from Zoneprofiles what vacuum state the system needs to be in
                        # If it's here, you want the vacuum to be on
                        
                        Logging.logEvent("Debug","Status Update", 
                        {"message": "Current chamber pressure: {}".format(self.chamberPressure),
                         "level":4})

                        # Pressure is in Torr and Temperature is in Kelvin.
                        # calculations to get from here to there
                        if self.chamberPressure > 300: #torr?
                            # use the roughing pump to achieve Rough vacuum
                            # Wait until 0.0.041 tor
                            self.state = "Atmosphere"
                        if ((self.oldState != "Crossover Vacuum") and (self.chamberPressure < 300)) or \
                                ((self.oldState != "Atmosphere") and (self.chamberPressure > 0.046)):
                            # open Cryopump-Roughing gate valve
                            # Wait until 0.041 tor
                            self.state = "Rough Vacuum"
                        if ((self.oldState != "Cryo Vacuum") and
                                (self.chamberPressure < 0.040) and
                                (self.cryoPumpPressure < 0.045)) or \
                                ((self.oldState == "Cryo Vacuum") and
                                     (self.hw.ShiCryopump.get_mcc_status('Stage 1 Temp') > 20)):
                            # Alert the user they should close o-ring seal 
                            # Start the cryopump
                            self.state = "Crossover Vacuum"
                        userName = os.environ['LOGNAME']
                        if "root" in userName:
                            if (self.hw.ShiCryopump.get_mcc_status('Stage 2 Temp') < 15 and self.chamberPressure < 0.035):
                                # Close the rough gate valve
                                # Open the cryopump gate valve
                                # Wait until 10e-6 tor
                                self.state = "Cryo Vacuum"
                        else:
                            if self.chamberPressure < 0.005: #torr?
                                self.state = "Cryo Vacuum"
                        if self.chamberPressure < 9e-5: #torr?
                            # Wait for nothing, either the program will end, or be stopped by the safety checker
                            self.state = "Operational Vacuum"

                        Logging.logEvent("Debug","Status Update", 
                        {"message": "Current chamber state: {}".format(self.state),
                         "level":4})

                        result = {
                            'Atmosphere': self.atmosphere,
                            'Rough Vacuum': self.roughVacuum,
                            'Crossover Vacuum': self.crossoverVacuum,
                            'Cryo Vacuum': self.CryoVacuum,
                            'Operational Vacuum': self.operationalVacuum,
                        }[self.state]()

                        if "Operational Vacuum" in self.state:
                            self.hw.OperationalVacuum = True
                        else:
                            self.hw.OperationalVacuum = False

                        

                        # sleep until the next time around
                        time.sleep(self.updatePeriod)


                        # TODO: Is there some safe way of taking the chamber out of vacuum?
                    # End of inner if
                    else: 
                        time.sleep(1)
                # end of inner while True
            except Exception as e:

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error: {} in file {}:{}".format(exc_type, fname, exc_tb.tb_lineno))

                # FileCreation.pushFile("Error",self.zoneUUID,'{"errorMessage":"%s"}'%(e))
                ProfileInstance.getInstance().zoneProfiles.activeProfile = False
                raise e
            # end of try, catch
        #end of outer while true
    # end of run()

    def atmosphere(self):
        '''
        It enters this state everytime you are at atmosphere pressure
        '''
        if self.oldState != self.state:
            # The system has just crossed over to a new point
            userName = os.environ['LOGNAME']
            if "root" in userName:
                # TODO: Read coldwater value from Compressor
        
                # Close Cryopump gate Valve 
                self.hw.PC_104.digital_out.update({'CryoP GateValve': False})
                # TODO: Add check for CryoP GateValve closed state.
                # Prep the on Roughing Pump
                self.hw.PC_104.digital_out.update({'RoughP Pwr Relay': True})
                time.sleep(0.2)
                self.hw.PC_104.digital_out.update({'RoughP GateValve': True})
                time.sleep(0.2)
                self.hw.PC_104.digital_out.update({'RoughP PurgeGass': True})
                time.sleep(1)  # TODO: replace sleep with Roughing pump Gate valve check and power check
                # Turn on Roughing Pump
                self.hw.PC_104.digital_out.update({'RoughP Start': True})
                # Do we send an alart to the user, if they need to do this phycisally?

            else:
                print("in Atomo")


    def roughVacuum(self):
        '''
        It enters this state everytime you are between 0.040 torr and 0.005 torr
        '''
        if (self.oldState != self.state):  # and (self.oldState == "Atmosphere"):
            Logging.logEvent("Debug", "Status Update",
                             {"message": "Entering Rough vacuum. Ruffing the Cryo Pump.",
                              "level": 1})
            # The system has just crossed over to a new point
            userName = os.environ['LOGNAME']
            if "root" in userName:
                # open Cryopump-Roughing gate valve
                self.hw.Shi_MCC_Cmds.append(['Close_PurgeValve'])
                time.sleep(2)
                self.hw.Shi_MCC_Cmds.append(['Open_RoughingValve'])
                self.hw.Shi_MCC_Cmds.append(['FirstStageTempCTL', 50, 3])
                self.hw.Shi_MCC_Cmds.append(['SecondStageTempCTL', 10])
            else:
                Logging.logEvent("Debug", "Status Update",
                                 {"message": "In Rough vacuum.",
                                  "level": 4})


    def crossoverVacuum(self):
        '''
        It enters this state everytime you are between 0.041 torr and 0.005
        '''
        if (self.oldState != self.state):
            Logging.logEvent("Debug", "Status Update",
                             {"message": "Entering Crossover Vacuum from Rough vacuum. Cryo pump On.",
                              "level": 1})
            # The system has just crossed over to a new point
            userName = os.environ['LOGNAME']
            if "root" in userName:
                #TODO: Alert the user they should close o-ring seal 
                self.hw.Shi_MCC_Cmds.append(['Close_RoughingValve'])
                time.sleep(2)
                # Starting the Cryppump:
                #TODO: starts the Compressor
                # self.hw.Shi_compressor_Cmds.append([''])
                self.hw.Shi_MCC_Cmds.append(['Turn_CryoPumpOn'])
            else:
                print("In Crossover Vacuum")

    def CryoVacuum(self):
        '''
        It enters this state everytime you are between 0.005 torr and 0.00001
        '''
        if (self.oldState != self.state):
            # The system has just crossed over to a new point
            userName = os.environ['LOGNAME']
            if "root" in userName:

                # Close the rough gate valve
                self.hw.PC_104.digital_out.update({'RoughP GateValve': False})

                # wait here until the valve is closed
                # TODO Replace Sleep with a check of the Gate valve switches
                time.sleep(4)

                # Open the cryopump gate valve
                self.hw.PC_104.digital_out.update({'CryoP GateValve': True})
                # TODO Add a check of the Gate valve switches - Keep Sleep
                time.sleep(4)

                # Open the cryopump gate valve
                self.hw.PC_104.digital_out.update({'RoughP Pwr Relay': False})
                time.sleep(2)
                self.hw.PC_104.digital_out.update({'RoughP PurgeGass': False})

            else:
                print("In Strong Cryo Vacuum")
        
    def operationalVacuum(self):
        '''
        It enters this state everytime you are lower than 0.00001 torr
        '''
        if self.oldState != self.state:
            # The system has just crossed over to a new point
            
            pass
            # Bakes ban happen here.
            # Thermal Profiles can start here



    # TODO: Write a wrapper around opening valves to make one final check of the pressures before we open them