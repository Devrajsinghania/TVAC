#!/usr/bin/env python3.5
import os
import sys
import time
from threading import Thread

if __name__ == '__main__':
    sys.path.insert(0, os.getcwd())

from Collections.HardwareStatusInstance import HardwareStatusInstance
from Collections.ProfileInstance import ProfileInstance
from Hardware_Drivers.Shi_Mcc import Shi_Mcc

from Logging.Logging import Logging


class ShiMccUpdater(Thread):
    def __init__(self, parent=None, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        self.parent = parent

        self.mcc = Shi_Mcc()
        self.hw = HardwareStatusInstance.getInstance()
        self.mcc_read_period = 1  # 0.5s loop period
        self.param_period = 30  # 10 second period

    def run(self):
        if os.name == "posix":
            userName = os.environ['LOGNAME']
        else:
            userName = "user"
        # While true to restart the thread if it errors out
        while True:
            # Catch anything that goes wrong
            # This has no check because it should always be running
            try:
                # Thread "Start up" stuff goes here
                Logging.logEvent("Debug", "Status Update",
                                {"message": "Starting Shi Mcc Control Stub Thread",
                                "level": 2})

                if "root" in userName:
                    # Live systems go here
                    Logging.logEvent("Debug", "Status Update",
                                    {"message": "Power on the Shi Mcc",
                                    "level": 3})
                    self.mcc.open_port()
                    while self.hw.PC_104.digital_out.getVal('CryoP Pwr Relay 1') is None:
                        time.sleep(1)
                    Currently_powered = self.hw.PC_104.digital_out.getVal('MCC2 Power')
                    self.hw.PC_104.digital_out.update({'MCC2 Power': True})
                    if not Currently_powered:
                        time.sleep(5)
                    self.mcc.flush_port()
                    # Now send some initialization commands
                    # The maximum second stage temperature the cryopump may start to restart after a power failure.
                    val = self.mcc.Get_RegenParam_6()
                    if val['Error']:
                        Logging.logEvent("Debug", "Status Update",
                                         {"message": 'Shi MCC GetRegenParam_6" Error Response: %s' % (val),
                                          "level": 4})
                        raise Exception("Shi MCC Error with Get_RegenParam_6: %s" % val['Response'])
                    else:
                        if val['Data'] != 65:
                            self.run_set_cmd(self.mcc.Set_RegenParam, [' ', '6', 65])
                    # 2: Power failure recovery enabled only when T2 is less than the limit set point.
                    val = self.mcc.Get_PowerFailureRecovery()
                    if val['Error']:
                        Logging.logEvent("Debug", "Shi MCC Error",
                                         {"message": "Set_RegenParam: %s" % val['Response'],
                                          "level": 3})
                        raise Exception("Shi MCC Error with Set_RegenParam: %s" % val['Response'])
                    else:
                        if val['Data'] != 2:
                            self.run_set_cmd(self.mcc.Set_RegenParam, [' ', 2])

                next_param_read_time = time.time()
                # setup is done, this loop is the normal thread loop
                while True:
                    next_mcc_read_time = time.time() + self.mcc_read_period
                    if "root" in userName:
                        try:
                            Logging.logEvent("Debug", "Status Update",
                                             {"message": "Reading and writing with ShiMccUpdater.",
                                              "level": 4})
                            val = self.mcc.get_Status()
                            if val['Error']:
                                Logging.logEvent("Debug", "Status Update",
                                                 {"message": "Shi MCC Error Response: %s" % val['Response'],
                                                  "level": 4})
                            else:
                                self.hw.ShiCryopump.update({'MCC Status': val['Response']})
                            Logging.logEvent("Debug", "Status Update",
                                             {"message": "Cryopump Stage 1: {:.1f}K; Stage 2: {:.1f}K"
                                                         "".format(self.hw.ShiCryopump.get_mcc_status('Stage 1 Temp'),
                                                                   self.hw.ShiCryopump.get_mcc_status('Stage 2 Temp')),
                                              "level": 4})
                            if time.time() > next_param_read_time:
                                val = self.mcc.get_ParamValues()
                                if val['Error']:
                                    Logging.logEvent("Debug", "Status Update",
                                                     {"message": "Shi MCC Error Response: %s" % val['Response'],
                                                      "level": 4})
                                else:
                                    self.hw.ShiCryopump.update({'MCC Params': val['Response']})
                                next_param_read_time = time.time() + self.param_period

                            while len(self.hw.Shi_MCC_Cmds):
                                cmd = self.hw.Shi_MCC_Cmds.pop()
                                if 'FirstStageTempCTL' == cmd[0]:  # 2.9 • First Stage Temperature Control pg:10
                                    self.run_set_cmd(self.mcc.Set_FirstStageTempCTL, cmd)
                                    self.run_get_cmd(self.mcc.Get_FirstStageTempCTL,
                                                     "First Stage Temp CTL")
                                elif 'PowerFailureRecovery' == cmd[0]:  # 2.12 • Power Failure Recovery pg:11
                                    self.run_set_cmd(self.mcc.Set_PowerFailureRecovery, cmd)
                                    self.run_get_cmd(self.mcc.Get_PowerFailureRecovery,
                                                     "Power Failure Recovery")
                                elif 'Turn_CryoPumpOn' == cmd[0]:  # 2.14 • Pump On/Off/Query pg:13
                                    self.run_set_cmd(self.mcc.Turn_CryoPumpOn, cmd)
                                elif 'Turn_CryoPumpOff' == cmd[0]:  # 2.14 • Pump On/Off/Query pg:13
                                    self.run_set_cmd(self.mcc.Turn_CryoPumpOff, cmd)
                                elif 'Close_PurgeValve' == cmd[0]:  # 2.15 • Purge On/Off/Query pg:14
                                    self.run_set_cmd(self.mcc.Close_PurgeValve, cmd)
                                elif 'Open_PurgeValve' == cmd[0]:  # 2.15 • Purge On/Off/Query pg:14
                                    if self.hw.PC_104.digital_in.getVal('CryoP_GV_Closed'):
                                        self.run_set_cmd(self.mcc.Open_PurgeValve, cmd)
                                    else:
                                        Logging.logEvent("Debug", "Status Update",
                                                 {"message": 'Cryopump Gate Valve not closed. Purge valve not opened.',
                                                  "level": 2})
                                elif 'Start_Regen' == cmd[0]:  # 2.16 • Regeneration pg:14
                                    self.run_set_cmd(self.mcc.Start_Regen, cmd)
                                    Logging.logEvent("Event", "Cryopump Regeneration",
                                                     {"message": "Cryopump regeneration starting",
                                                      "ProfileInstance": ProfileInstance.getInstance()})
                                elif 'Set_RegenParam' == cmd[0]:  # 2.19 • Regeneration Parameters pg:16
                                    self.run_set_cmd(self.mcc.Set_RegenParam, cmd)
                                    val = self.mcc.Get_RegenParam(cmd[1])
                                    if val['Error']:
                                        Logging.logEvent("Debug", "Status Update",
                                             {"message": 'Shi MCC GetRegenParam_%s" Error Response: %s' % (cmd[1], val),
                                              "level": 4})
                                    else:
                                        self.hw.ShiCryopump.update({'MCC Params': {"Regen Param_%s" % cmd[1]: val['Data']}})
                                elif 'RegenStartDelay' == cmd[0]:  # 2.21 • Regeneration Start Delay pg.18
                                    self.run_set_cmd(self.mcc.Set_RegenStartDelay, cmd)
                                    self.run_get_cmd(self.mcc.Get_RegenStartDelay, "Regen Start Delay")
                                elif 'Open_RoughingValve' == cmd[0]:  # 2.24 • Rough On/Off/Query pg:19
                                    self.run_set_cmd(self.mcc.Open_RoughingValve, cmd)
                                elif 'Close_RoughingValve' == cmd[0]:  # 2.24 • Rough On/Off/Query pg:19
                                    self.run_set_cmd(self.mcc.Close_RoughingValve, cmd)
                                elif 'Clear_RoughingInterlock' == cmd[0]:  # 2.25 • Rough Valve Interlock pg:20
                                    self.run_set_cmd(self.mcc.Clear_RoughingInterlock, cmd)
                                elif 'SecondStageTempCTL' == cmd[0]:  # 2.27 • Second Stage Temperature Control pg:21
                                    self.run_set_cmd(self.mcc.Set_SecondStageTempCTL, cmd)
                                    self.run_get_cmd(self.mcc.Get_SecondStageTempCTL,
                                                     "Second Stage Temp CTL")
                                elif 'Turn_TcPressureOn' == cmd[0]:  # 2.29 • TC On/Off/Query pg:22
                                    self.run_set_cmd(self.mcc.Turn_TcPressureOn, cmd)
                                elif 'Turn_TcPressureOff' == cmd[0]:  # 2.29 • TC On/Off/Query pg:22
                                    self.run_set_cmd(self.mcc.Turn_TcPressureOff, cmd)

                                else:
                                    Logging.logEvent("Error", 'Unknown Shi_MCC_Cmd: "%s"' % cmd[0],
                                                     {"type": 'Unknown Shi_MCC_Cmd',
                                                      "filename": 'ThreadControls/ShiMccUpdater.py',
                                                      "line": 0,
                                                      "thread": "ShiMccUpdater"
                                                      })
                        except ValueError as err:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            Logging.logEvent("Error", 'Error in ShiMccUpdater reading values: "%s"' % err,
                                             {"type": exc_type,
                                              "filename": fname,
                                              "line": exc_tb.tb_lineno,
                                              "thread": "ShiMccUpdater"
                                              })
                            if Logging.debug:
                                raise err
                    else:
                        Logging.logEvent("Debug", "Status Update",
                                         {"message": "Test run of Shi MCC loop",
                                          "level": 4})

                    if time.time() < next_mcc_read_time:
                        time.sleep(next_mcc_read_time - time.time())

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Logging.logEvent("Error", "Shi MCC Interface Thread",
                                 {"type": exc_type,
                                  "filename": fname,
                                  "line": exc_tb.tb_lineno,
                                  "thread": "ShiMccUpdater"
                                  })
                Logging.logEvent("Debug", "Status Update",
                                 {"message": "There was a {} error in ShiMccUpdater. File: {}:{}\n{}".format(
                                     exc_type, fname, exc_tb.tb_lineno, e),
                                  "level": 1})
                if Logging.debug:
                    raise e
                self.mcc.close_port()
                time.sleep(4)

    def run_set_cmd(self, fun, cmd):
        if len(cmd) <= 1:
            val = fun()
        elif len(cmd) == 2:
            val = fun(cmd[1])
        elif len(cmd) == 3:
            val = fun(cmd[1],cmd[2])
        else:
            raise Exception('run_cmd has to many arguments')
        if val['Error']:
            Logging.logEvent("Debug", "Status Update",
                             {"message": 'Shi MCC Set_"%s" Error Response: %s' % (cmd[0], val),
                              "level": 3})

    def run_get_cmd(self, fun, key):
        val = fun()
        if val['Error']:
            Logging.logEvent("Debug", "Status Update",
                             {"message": 'Shi MCC Get_"%s" Error Response: %s' % (key, val),
                              "level": 3})
        else:
            if 'Data' in val:
                self.hw.ShiCryopump.update({'MCC Params': {key: val['Data']}})
            else:
                self.hw.ShiCryopump.update({'MCC Params': {key: val['Response']}})


if __name__ == '__main__':
    # adding debug info
    if(len(sys.argv)>1):
        for arg in sys.argv:
            if arg.startswith("-v"):
                Logging.verbos = arg.count("v")
    Logging.logEvent("Debug","Status Update",
        {"message": "Debug on: Level {}".format(Logging.verbos),
         "level":1})

    hw_status = HardwareStatusInstance.getInstance()
    hw_status.PC_104.digital_out.update({'MCC2 Power': True})

    thread = ShiMccUpdater()
    thread.daemon = True
    thread.start()

    while True:
        time.sleep(5)
        print(hw_status.ShiCryopump.getJson())

