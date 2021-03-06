import threading
import json


class DigitalInContract:

    __lock = threading.RLock()

    def __init__(self):
        self.pgRoughPumpRelay1 = False    # C 1: Di 0 - Roughing Pump Pressure Gauge Relay 1
        self.pgRoughPumpRelay2 = False    # C 1: Di 1 - Roughing Pump Pressure Gauge Relay 2
        self.pgCryoPumpRelay1 = False     # C 1: Di 2 - Cryo-pump Pressure Gauge Relay 1
        self.pgCryoPumpRelay2 = False     # C 1: Di 3 - Cryo-pump Pressure Gauge Relay 2
        self.pgChamberRelay1 = False      # C 1: Di 4 - Chamber Pressure Gauge Relay 1
        self.pgChamberRelay2 = False      # C 1: Di 5 - Chamber Pressure Gauge Relay 2
        self.LN2_P_Sol_Open_NC = False    # C 1: Di 6 -
        self.LN2_P_Sol_Open_O = False     # C 1: Di 7 -
        self.LN2_P_Sol_Closed_NC = False  # C 1: Di 8 -
        self.LN2_P_Sol_Closed_O = False   # C 1: Di 9 -
        self.LN2_S_Sol_Open_NC = False    # C 1: Di 10-
        self.LN2_S_Sol_Open_O = False     # C 1: Di 11-
        self.LN2_S_Sol_Closed_NC = False  # C 1: Di 12-
        self.LN2_S_Sol_Closed_O = False   # C 1: Di 13-
        self.CryoP_GV_Open_NC = False     # C 1: Di 14-
        self.CryoP_GV_Open_O = False      # C 1: Di 15-
        self.CryoP_GV_Closed_NC = False   # C 1: Di 16-
        self.CryoP_GV_Closed_O = False    # C 1: Di 17-
        self.RoughP_GV_Open = False       # C 1: Di 18-
        self.RoughP_GV_Closed = False     # C 1: Di 19-
        self.RoughP_Pwr_NC = False        # C 1: Di 20-
        self.RoughP_Pwr_O = False         # C 1: Di 21-
        self.RoughP_On_NC = False         # C 1: Di 22-
        self.RoughP_On_O = False          # C 1: Di 23-
        self.notUsed1 = False             # C 1: Di 24- Unassigned channel 24
        self.notUsed2 = False             # C 1: Di 25- Unassigned channel 25
        self.notUsed3 = False             # C 1: Di 26- Unassigned channel 26
        self.notUsed4 = False             # C 1: Di 27- Unassigned channel 27
        self.notUsed5 = False             # C 1: Di 28- Unassigned channel 28
        self.notUsed6 = False             # C 1: Di 29- Unassigned channel 29
        self.LN2AirOK = False             # C 1: Di 30- 100 psi Air supply connected to the LN2 supply valves
        self.AirOK = False                # C 1: Di 31- 100 psi Air supply connected to the TVAC
        self.front_door_closed = False    # C 2: Di 0 -
        self.back_door_closed = False     # C 2: Di 1 -
        self.t22 = False                  # C 2: Di 2 -
        self.t23 = False                  # C 2: Di 3 -
        self.t24 = False                  # C 2: Di 4 -
        self.t25 = False                  # C 2: Di 5 -
        self.t26 = False                  # C 2: Di 6 -
        self.t27 = False                  # C 2: Di 7 -
        self.t28 = False                  # C 2: Di 8 -
        self.t29 = False                  # C 2: Di 9 -
        self.t30 = False                  # C 2: Di 10-
        self.t31 = False                  # C 2: Di 11-
        self.t32 = False                  # C 2: Di 12-
        self.t33 = False                  # C 2: Di 13-
        self.t34 = False                  # C 2: Di 14-
        self.t35 = False                  # C 2: Di 15-
        self.t36 = False                  # C 2: Di 16-
        self.t37 = False                  # C 2: Di 17-
        self.t38 = False                  # C 2: Di 18-
        self.t39 = False                  # C 2: Di 19-
        self.t40 = False                  # C 2: Di 20-
        self.t41 = False                  # C 2: Di 21-
        self.t42 = False                  # C 2: Di 22-
        self.t43 = False                  # C 2: Di 23-
        self.t44 = False                  # C 2: Di 24-
        self.t45 = False                  # C 2: Di 25-
        self.notUsed7 = False             # C 2: Di 26-
        self.notUsed8 = False             # C 2: Di 27-
        self.notUsed9 = False             # C 2: Di 28-
        self.notUsed10 = False            # C 2: Di 29-
        self.notUsed11 = False            # C 2: Di 30-
        self.LN2en = False                # C 2: Di 31- LN2 flow is enabled

        self.LN2_P_Sol_Open = None      # LN2 Platen Solenoid valve is open?
        self.LN2_P_Sol_Open_WF = None   # LN2 Platen Solenoid valve open switch wiring fault.
        self.LN2_P_Sol_Closed = None    # LN2 Platen Solenoid valve is closed?
        self.LN2_P_Sol_Closed_WF = None  # LN2 Platen Solenoid valve closed switch wiring fault.

        self.LN2_S_Sol_Open = None      # LN2 Shroud Solenoid valve is open?
        self.LN2_S_Sol_Open_WF = None   # LN2 Shroud Solenoid valve open switch wiring fault.
        self.LN2_S_Sol_Closed = None    # LN2 Shroud Solenoid valve is closed?
        self.LN2_S_Sol_Closed_WF = None  # LN2 Shroud Solenoid valve closed switch wiring fault.

        self.CryoP_GV_Open = None       # Cryo Pump Gate valve is open?
        self.CryoP_GV_Open_WF = None    # Cryo Pump Gate valve open switch wiring fault.
        self.CryoP_GV_Closed = None     # Cryo Pump Gate valve is closed?
        self.CryoP_GV_Closed_WF = None  # Cryo Pump Gate valve closed switch wiring fault.

        self.RoughP_Powered = None      # Roughing Pump is Powered?
        self.RoughP_Powered_WF = None   # Roughing Pump is Powered switch wiring fault.
        self.RoughP_On_Sw = None        # Roughing Pump is On?
        self.RoughP_On_Sw_WF = None     # Roughing Pump is On switch wiring fault.

        self.chamber_closed = None      # When True the chamber is closed.

    def update(self, d):
        self.__lock.acquire()
        if 'C1 B0' in d:
            self.pgRoughPumpRelay1 = ((d['C1 B0'] & 0x01) > 0)  # C 1: Di 1
            self.pgRoughPumpRelay2 = ((d['C1 B0'] & 0x02) > 0)  # C 1: Di 1
            self.pgCryoPumpRelay1 = ((d['C1 B0'] & 0x04) > 0)  # C 1: Di 2
            self.pgCryoPumpRelay2 = ((d['C1 B0'] & 0x08) > 0)  # C 1: Di 3
            self.pgChamberRelay1 = ((d['C1 B0'] & 0x10) > 0)  # C 1: Di 4
            self.pgChamberRelay2 = ((d['C1 B0'] & 0x20) > 0)  # C 1: Di 5
            self.LN2_P_Sol_Open_NC = ((d['C1 B0'] & 0x40) > 0)  # C 1: Di 6
            self.LN2_P_Sol_Open_O = ((d['C1 B0'] & 0x80) > 0)  # C 1: Di 7

            self.LN2_P_Sol_Open = self.LN2_P_Sol_Open_NC and not self.LN2_P_Sol_Open_O
            self.LN2_P_Sol_Open_WF = self.LN2_P_Sol_Open_NC == self.LN2_P_Sol_Open_O

        if 'C1 B1' in d:
            self.LN2_P_Sol_Closed_NC = ((d['C1 B1'] & 0x01) > 0)  # C 1: Di 8
            self.LN2_P_Sol_Closed_O = ((d['C1 B1'] & 0x02) > 0)  # C 1: Di 9
            self.LN2_S_Sol_Open_NC = ((d['C1 B1'] & 0x04) > 0)  # C 1: Di 10
            self.LN2_S_Sol_Open_O = ((d['C1 B1'] & 0x08) > 0)  # C 1: Di 11
            self.LN2_S_Sol_Closed_NC = ((d['C1 B1'] & 0x10) > 0)  # C 1: Di 12
            self.LN2_S_Sol_Closed_O = ((d['C1 B1'] & 0x20) > 0)  # C 1: Di 13
            self.CryoP_GV_Open_NC = ((d['C1 B1'] & 0x40) > 0)  # C 1: Di 14
            self.CryoP_GV_Open_O = ((d['C1 B1'] & 0x80) > 0)  # C 1: Di 15

            self.LN2_P_Sol_Closed = self.LN2_P_Sol_Closed_NC and not self.LN2_P_Sol_Closed_O
            self.LN2_P_Sol_Closed_WF = self.LN2_P_Sol_Closed_NC == self.LN2_P_Sol_Closed_O

            self.LN2_S_Sol_Open = self.LN2_S_Sol_Open_NC and not self.LN2_S_Sol_Open_O
            self.LN2_S_Sol_Open_WF = self.LN2_S_Sol_Open_NC == self.LN2_S_Sol_Open_O

            self.LN2_S_Sol_Closed = self.LN2_S_Sol_Closed_NC and not self.LN2_S_Sol_Closed_O
            self.LN2_S_Sol_Closed_WF = self.LN2_S_Sol_Closed_NC == self.LN2_S_Sol_Closed_O

            self.CryoP_GV_Open = self.CryoP_GV_Open_NC and not self.CryoP_GV_Open_O
            self.CryoP_GV_Open_WF = self.CryoP_GV_Open_NC == self.CryoP_GV_Open_O

        if 'C1 B2' in d:
            self.CryoP_GV_Closed_NC = ((d['C1 B2'] & 0x01) > 0)  # C 1: Di 16
            self.CryoP_GV_Closed_O = ((d['C1 B2'] & 0x02) > 0)  # C 1: Di 17
            self.RoughP_GV_Open = ((d['C1 B2'] & 0x04) > 0)  # C 1: Di 18
            self.RoughP_GV_Closed = ((d['C1 B2'] & 0x08) > 0)  # C 1: Di 19
            self.RoughP_Pwr_NC = ((d['C1 B2'] & 0x10) > 0)  # C 1: Di 20
            self.RoughP_Pwr_O = ((d['C1 B2'] & 0x20) > 0)  # C 1: Di 21
            self.RoughP_On_NC = ((d['C1 B2'] & 0x40) > 0)  # C 1: Di 22
            self.RoughP_On_O = ((d['C1 B2'] & 0x80) > 0)  # C 1: Di 23

            self.CryoP_GV_Closed = self.CryoP_GV_Closed_NC and not self.CryoP_GV_Closed_O
            self.CryoP_GV_Closed_WF = self.CryoP_GV_Closed_NC == self.CryoP_GV_Closed_O

            self.RoughP_Powered = self.RoughP_Pwr_NC and not self.RoughP_Pwr_O
            self.RoughP_Powered_WF = self.RoughP_Pwr_NC == self.RoughP_Pwr_O

            self.RoughP_On_Sw = self.RoughP_On_NC and not self.RoughP_On_O
            self.RoughP_On_Sw_WF = self.RoughP_On_NC == self.RoughP_On_O

        if 'C1 B3' in d:
            self.notUsed1 = ((d['C1 B3'] & 0x01) > 0)  # C 1: Di 24
            self.notUsed2 = ((d['C1 B3'] & 0x02) > 0)  # C 1: Di 25
            self.notUsed3 = ((d['C1 B3'] & 0x04) > 0)  # C 1: Di 26
            self.notUsed4 = ((d['C1 B3'] & 0x08) > 0)  # C 1: Di 27
            self.notUsed5 = ((d['C1 B3'] & 0x10) > 0)  # C 1: Di 28
            self.notUsed6 = ((d['C1 B3'] & 0x20) > 0)  # C 1: Di 29
            self.LN2AirOK = ((d['C1 B3'] & 0x40) > 0)  # C 1: Di 30
            self.AirOK = ((d['C1 B3'] & 0x80) > 0)  # C 1: Di 31
        if 'C2 B0' in d:
            self.front_door_closed = ((d['C2 B0'] & 0x01) > 0)  # C 2: Di 0
            self.back_door_closed = ((d['C2 B0'] & 0x02) > 0)  # C 2: Di 1
            self.t22 = ((d['C2 B0'] & 0x04) > 0)  # C 2: Di 2
            self.t23 = ((d['C2 B0'] & 0x08) > 0)  # C 2: Di 3
            self.t24 = ((d['C2 B0'] & 0x10) > 0)  # C 2: Di 4
            self.t25 = ((d['C2 B0'] & 0x20) > 0)  # C 2: Di 5
            self.t26 = ((d['C2 B0'] & 0x40) > 0)  # C 2: Di 6
            self.t27 = ((d['C2 B0'] & 0x80) > 0)  # C 2: Di 7

            self.chamber_closed = self.front_door_closed and self.back_door_closed

        if 'C2 B1' in d:
            self.t28 = ((d['C2 B1'] & 0x01) > 0)  # C 2: Di 8
            self.t29 = ((d['C2 B1'] & 0x02) > 0)  # C 2: Di 9
            self.t30 = ((d['C2 B1'] & 0x04) > 0)  # C 2: Di 10
            self.t31 = ((d['C2 B1'] & 0x08) > 0)  # C 2: Di 11
            self.t32 = ((d['C2 B1'] & 0x10) > 0)  # C 2: Di 12
            self.t33 = ((d['C2 B1'] & 0x20) > 0)  # C 2: Di 13
            self.t34 = ((d['C2 B1'] & 0x40) > 0)  # C 2: Di 14
            self.t35 = ((d['C2 B1'] & 0x80) > 0)  # C 2: Di 15
        if 'C2 B2' in d:
            self.t36 = ((d['C2 B2'] & 0x01) > 0)  # C 2: Di 16
            self.t37 = ((d['C2 B2'] & 0x02) > 0)  # C 2: Di 17
            self.t38 = ((d['C2 B2'] & 0x04) > 0)  # C 2: Di 18
            self.t39 = ((d['C2 B2'] & 0x08) > 0)  # C 2: Di 19
            self.t40 = ((d['C2 B2'] & 0x10) > 0)  # C 2: Di 20
            self.t41 = ((d['C2 B2'] & 0x20) > 0)  # C 2: Di 21
            self.t42 = ((d['C2 B2'] & 0x40) > 0)  # C 2: Di 22
            self.t43 = ((d['C2 B2'] & 0x80) > 0)  # C 2: Di 23
        if 'C2 B3' in d:
            self.t44 = ((d['C2 B3'] & 0x01) > 0)  # C 2: Di 24
            self.t45 = ((d['C2 B3'] & 0x02) > 0)  # C 2: Di 25
            self.notUsed7 = ((d['C2 B3'] & 0x04) > 0)  # C 2: Di 26
            self.notUsed8 = ((d['C2 B3'] & 0x08) > 0)  # C 2: Di 27
            self.notUsed9 = ((d['C2 B3'] & 0x10) > 0)  # C 2: Di 28
            self.notUsed10 = ((d['C2 B3'] & 0x20) > 0)  # C 2: Di 29
            self.notUsed11 = ((d['C2 B3'] & 0x40) > 0)  # C 2: Di 30
            self.LN2en = ((d['C2 B3'] & 0x80) > 0)  # C 2: Di 31
        self.__lock.release()

    def getVal(self, name):
        self.__lock.acquire()
        if name == 'pgRoughPumpRelay1':
            val = self.pgRoughPumpRelay1
        elif name == 'pgRoughPumpRelay2':
            val = self.pgRoughPumpRelay2
        elif name == 'pgCryoPumpRelay1':
            val = self.pgCryoPumpRelay1
        elif name == 'pgCryoPumpRelay2':
            val = self.pgCryoPumpRelay2
        elif name == 'pgChamberRelay1':
            val = self.pgChamberRelay1
        elif name == 'pgChamberRelay2':
            val = self.pgChamberRelay2

        elif name == 'LN2_P_Sol_Open':
            val = self.LN2_P_Sol_Open
        elif name == 'LN2_P_Sol_Open_NC':
            val = self.LN2_P_Sol_Open_NC
        elif name == 'LN2_P_Sol_Open_O':
            val = self.LN2_P_Sol_Open_O
        elif name == 'LN2_P_Sol_Open_WF':
            val = self.LN2_P_Sol_Open_WF

        elif name == 'LN2_P_Sol_Closed':
            val = self.LN2_P_Sol_Closed
        elif name == 'LN2_P_Sol_Closed_NC':
            val = self.LN2_P_Sol_Closed_NC
        elif name == 'LN2_P_Sol_Closed_O':
            val = self.LN2_P_Sol_Closed_O
        elif name == 'LN2_P_Sol_Closed_WF':
            val = self.LN2_P_Sol_Closed_WF

        elif name == 'LN2_S_Sol_Open':
            val = self.LN2_S_Sol_Open
        elif name == 'LN2_S_Sol_Open_NC':
            val = self.LN2_S_Sol_Open_NC
        elif name == 'LN2_S_Sol_Open_O':
            val = self.LN2_S_Sol_Open_O
        elif name == 'LN2_S_Sol_Open_WF':
            val = self.LN2_S_Sol_Open_WF

        elif name == 'LN2_S_Sol_Closed':
            val = self.LN2_S_Sol_Closed
        elif name == 'LN2_S_Sol_Closed_NC':
            val = self.LN2_S_Sol_Closed_NC
        elif name == 'LN2_S_Sol_Closed_O':
            val = self.LN2_S_Sol_Closed_O
        elif name == 'LN2_S_Sol_Closed_WF':
            val = self.LN2_S_Sol_Closed_WF

        elif name == 'CryoP_GV_Open':
            val = self.CryoP_GV_Open
        elif name == 'CryoP_GV_Open_NC':
            val = self.CryoP_GV_Open_NC
        elif name == 'CryoP_GV_Open_O':
            val = self.CryoP_GV_Open_O
        elif name == 'CryoP_GV_Open_WF':
            val = self.CryoP_GV_Open_WF

        elif name == 'CryoP_GV_Closed':
            val = self.CryoP_GV_Closed
        elif name == 'CryoP_GV_Closed_NC':
            val = self.CryoP_GV_Closed_NC
        elif name == 'CryoP_GV_Closed_O':
            val = self.CryoP_GV_Closed_O
        elif name == 'CryoP_GV_Closed_WF':
            val = self.CryoP_GV_Closed_WF

        elif name == 'RoughP_GV_Open':
            val = self.RoughP_GV_Open
        elif name == 'RoughP_GV_Closed':
            val = self.RoughP_GV_Closed

        elif name == 'RoughP_Powered':
            val = self.RoughP_Powered
        elif name == 'RoughP_Pwr_NC':
            val = self.RoughP_Pwr_NC
        elif name == 'RoughP_Pwr_O':
            val = self.RoughP_Pwr_O
        elif name == 'RoughP_Powered_WF':
            val = self.RoughP_Powered_WF

        elif name == 'RoughP_On_Sw':
            val = self.RoughP_On_Sw
        elif name == 'RoughP_On_NC':
            val = self.RoughP_On_NC
        elif name == 'RoughP_On_O':
            val = self.RoughP_On_O
        elif name == 'RoughP_On_Sw_WF':
            val = self.RoughP_On_Sw_WF

        # elif name == 'notUsed1':
        #     val = self.notUsed1
        elif name == 'LN2AirOK':
            val = self.LN2AirOK
        elif name == 'AirOK':
            val = self.AirOK
        elif name == 'front_door_closed':
            val = self.front_door_closed
        elif name == 'back_door_closed':
            val = self.back_door_closed
        elif name == 'Chamber Closed':
            val = self.chamber_closed
        # elif name == 'notUsed7':
        #     val = self.notUsed7
        elif name == 'LN2en':
            val = self.LN2en
        else:  # Unknown Value!
            val = None
        self.__lock.release()
        return val

    def getJson_bits(self):
        self.__lock.acquire()
        message = ['"PG-SW-RoughP-Relay 1":%s' % json.dumps(self.pgRoughPumpRelay1),
                   '"PG-SW-RoughP-Relay 2":%s' % json.dumps(self.pgRoughPumpRelay2),
                   '"PG-SW-CryoP-Relay 1":%s' % json.dumps(self.pgCryoPumpRelay1),
                   '"PG-SW-CryoP-Relay 2":%s' % json.dumps(self.pgCryoPumpRelay2),
                   '"PG-SW-Chamber-Relay 1":%s' % json.dumps(self.pgChamberRelay1),
                   '"PG-SW-Chamber-Relay 2":%s' % json.dumps(self.pgChamberRelay2),
                   '"LN2-P-Sol-Open: NC":%s' % json.dumps(self.LN2_P_Sol_Open_NC),
                   '"LN2-P-Sol-Open: O":%s' % json.dumps(self.LN2_P_Sol_Open_O),
                   '"LN2-P-Sol-Closed: NC":%s' % json.dumps(self.LN2_P_Sol_Closed_NC),
                   '"LN2-P-Sol-Closed: O":%s' % json.dumps(self.LN2_P_Sol_Closed_O),
                   '"LN2-S-Sol-Open: NC":%s' % json.dumps(self.LN2_S_Sol_Open_NC),
                   '"LN2-S-Sol-Open: O":%s' % json.dumps(self.LN2_S_Sol_Open_O),
                   '"LN2-S-Sol-Closed: NC":%s' % json.dumps(self.LN2_S_Sol_Closed_NC),
                   '"LN2-S-Sol-Closed: O":%s' % json.dumps(self.LN2_S_Sol_Closed_O),
                   '"CryoP-GV-Open: NC":%s' % json.dumps(self.CryoP_GV_Open_NC),
                   '"CryoP-GV-Open: O":%s' % json.dumps(self.CryoP_GV_Open_O),
                   '"CryoP-GV-Closed: NC":%s' % json.dumps(self.CryoP_GV_Closed_NC),
                   '"CryoP-GV-Closed: O":%s' % json.dumps(self.CryoP_GV_Closed_O),
                   '"RoughP-GV-Open":%s' % json.dumps(self.RoughP_GV_Open),
                   '"RoughP-GV-Closed":%s' % json.dumps(self.RoughP_GV_Closed),
                   '"RoughP-Pwr: NC":%s' % json.dumps(self.RoughP_Pwr_NC),
                   '"RoughP-Pwr: O":%s' % json.dumps(self.RoughP_Pwr_O),
                   '"RoughP-On: NC":%s' % json.dumps(self.RoughP_On_NC),
                   '"RoughP-On: O":%s' % json.dumps(self.RoughP_On_O),
                   '"notUsed1":%s' % json.dumps(self.notUsed1),
                   '"Air supply LN2 OK":%s' % json.dumps(self.LN2AirOK),
                   '"Air supply OK":%s' % json.dumps(self.AirOK),
                   '"Front Door Closed":%s' % json.dumps(self.front_door_closed),
                   '"Back Door Closed":%s' % json.dumps(self.back_door_closed),
                   '"Chamber Closed":%s' % json.dumps(self.chamber_closed),
                   '"notUsed7":%s' % json.dumps(self.notUsed7),
                   '"LN2-en":%s' % json.dumps(self.LN2en),
                   ]
        self.__lock.release()
        return '{' + ','.join(message) + '}'

    def getJson_Switches(self):
        self.__lock.acquire()
        message = ['"LN2-P-Sol-Open":%s' % json.dumps(self.LN2_P_Sol_Open),
                   '"LN2-P-Sol-Closed":%s' % json.dumps(self.LN2_P_Sol_Closed),
                   '"LN2-S-Sol-Open":%s' % json.dumps(self.LN2_S_Sol_Open),
                   '"LN2-S-Sol-Closed":%s' % json.dumps(self.LN2_S_Sol_Closed),
                   '"CryoP-GV-Open":%s' % json.dumps(self.CryoP_GV_Open),
                   '"CryoP-GV-Closed":%s' % json.dumps(self.CryoP_GV_Closed),
                   '"RoughP-GV-Open":%s' % json.dumps(self.RoughP_GV_Open),
                   '"RoughP-GV-Closed":%s' % json.dumps(self.RoughP_GV_Closed),
                   '"RoughP Powered":%s' % json.dumps(self.RoughP_Powered),
                   '"RoughP_On_Sw":%s' % json.dumps(self.RoughP_On_Sw),
                   '"Chamber Closed":%s' % json.dumps(self.chamber_closed),
                   ]
        self.__lock.release()
        return '{' + ','.join(message) + '}'

    def getJson_Switches_WF(self):
        self.__lock.acquire()
        message = ['"LN2-P-Sol-Open: WF":%s' % json.dumps(self.LN2_P_Sol_Open_WF),
                   '"LN2-P-Sol-Closed: WF":%s' % json.dumps(self.LN2_P_Sol_Closed_WF),
                   '"LN2-S-Sol-Open: WF":%s' % json.dumps(self.LN2_S_Sol_Open_WF),
                   '"LN2-S-Sol-Closed: WF":%s' % json.dumps(self.LN2_S_Sol_Closed_WF),
                   '"CryoP-GV-Open: WF":%s' % json.dumps(self.CryoP_GV_Open_WF),
                   '"CryoP-GV-Closed: WF":%s' % json.dumps(self.CryoP_GV_Closed_WF),
                   '"RoughP Powered: WF":%s' % json.dumps(self.RoughP_Powered_WF),
                   '"RoughP_On_Sw: WF":%s' % json.dumps(self.RoughP_On_Sw_WF),
                   ]
        self.__lock.release()
        return '{' + ','.join(message) + '}'
