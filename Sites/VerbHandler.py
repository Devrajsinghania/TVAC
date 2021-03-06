import http.server
import json
import sys
import os

from Controllers.PostControl import PostControl
from Controllers.GetControl import GetControl
from ThreadControls.ThreadCollectionInstance import ThreadCollectionInstance

from Logging.Logging import Logging

class VerbHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """Respond to a GET request."""
        Logging.logEvent("Debug","Status Update", 
            {"message": "Received GET Request",
             "level":1})
        try:
            path = self.path

            Logging.logEvent("Debug","Status Update", 
                {"message": "GET Request Path: {}".format(path),
                 "level":2})

            # Based on the path we are given, do different functions
            control = GetControl()
            result = {
                '/runProfile': control.runProfile,
                '/checkZoneStatus': control.checkTreadStatus,
                '/getAllThermoCoupleData': control.getAllThermoCoupleData,
                '/getAllZoneData': control.getAllZoneData,
                '/getShiTemps': control.getShiTemps,
                '/getCryoPump_Status': control.getCryoPump_Status,
                '/getCryoPump_Params': control.getCryoPump_Params,
                '/getCryoPump_plots': control.getCryoPump_plots,
                '/getPC104_Digital': control.getPC104_Digital,
                '/getPC104_Switches': control.getPC104_Switches,
                '/getPC104_Analog': control.getPC104_Analog,
                '/getPressureGauges': control.getPressureGauges,
                '/getZoneTemps': control.getZoneTemps,
                '/getLastErr' : control.getLastError,
                '/putUnderVacuum':control.putUnderVacuum,
                '/VacuumNotNeeded':control.VacuumNotNeeded,
                '/StopCryoPumpingChamber':control.StopCryoPumpingChamber,
                '/StopCryoPump':control.StopCryoPump,
                '/StopRoughingPump':control.StopRoughingPump,
                '/getEventList':control.getEventList,
                '/hardStop':control.hardStop,
                '/hold':control.holdAllZones,
                '/pause':control.pauseAllZones,
                '/resume':control.resumeAllZones,
                '/unHold':control.unHoldAllZones,
                '/getVacuumState': control.getVacuumState,
                '/doRegen': control.doRegen,
                '/abortRegen': control.abortRegen,
                '/getTvacStatus': control.getTvacStatus,
                '/StoprecordData': control.StoprecordData,
                '/recordData': control.recordData,
                }[path]()

            Logging.logEvent("Debug","Status Update",
                {"message": "Sending GET Results",
                 "level":1})
            Logging.logEvent("Debug","Status Update", 
                {"message": "GET Results: {}".format(str(result).encode()),
                 "level": 5})

            # Out the results back to the server
            self.setHeader()
            self.wfile.write(str(result).encode())
        except Exception as e:
            # print("There has been an error").
            # FileCreation.pushFile("Error","Get",'{"errorMessage":"%s"}\n'%(e))

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Logging.logEvent("Error","GET Handler", 
                {"type": exc_type,
                 "filename": fname,
                 "line": exc_tb.tb_lineno,
                 "thread": "Verb Handler",
                 "ThreadCollection":ThreadCollectionInstance.getInstance().threadCollection,
                 "item":"Server",
                 "itemID":-1,
                 "details":"PATH: {} is not recognized".format(path)
                })
            Logging.logEvent("Debug","Status Update", 
                {"message": "There was a {} error in Server (GET Handler). File: {}:{}".format(exc_type,fname,exc_tb.tb_lineno),
                 "level":1})

            self.setHeader()
            output = '{"Error":"%s"}\n'%(e)
            self.wfile.write(output.encode())
            raise e

    def do_POST(self):
        """Respond to a POST request."""
        try:
            Logging.logEvent("Debug","Status Update", 
                {"message": "Received Post Request",
                 "level":1})
            body = self.getBody()
            path = self.path
            
            Logging.logEvent("Debug","Status Update", 
                {"message": "POST Request Path: {}".format(path),
                 "level":2})

            # You might need to decode the results
            if type(body) == type(b'a'):
                body = body.decode("utf-8")
            contractObj = json.loads(body)

            # Based on the path we are given, do different functions
            control = PostControl()
            result = {
                '/saveProfile': control.saveProfile,
                '/loadProfile' : control.loadProfile,
                '/runSingleProfile': control.runSingleProfile,
                '/pauseZone': control.pauseSingleThread,
                '/pauseRemoveZone': control.removePauseSingleThread,
                '/holdZone': control.holdSingleThread,
                '/releaseHoldZone': control.releaseHoldSingleThread,
                '/abortZone': control.abortSingleThread,
                '/calculateRamp': control.calculateRamp,
                '/SendHwCmd': control.SendHwCmd,
                '/setPC104Digital': control.setPC104_Digital,
                '/setPC104Analog': control.setPC104_Analog,
                '/heatUpPlaten':control.heatUpPlaten,
                '/heatUpShroud':control.heatUpShroud,

            }[path](contractObj)

            Logging.logEvent("Debug","Status Update", 
                {"message": "Sending POST Results",
                 "level":1})
            Logging.logEvent("Debug","Status Update", 
                {"message": "POST Results: {}".format(str(result).replace("\"","'").encode()),
                 "level":2})

            self.setHeader()
            self.wfile.write(str(result).encode())
        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Logging.logEvent("Error","POST Handler", 
                {"type": exc_type,
                 "filename": fname,
                 "line": exc_tb.tb_lineno,
                 "thread": "Verb Handler"
                })
            Logging.logEvent("Debug","Status Update", 
                {"message": "There was a {} error in Server (POST Handler). File: {}:{}".format(exc_type,fname,exc_tb.tb_lineno),
                 "level":1})

            self.setHeader()
            output = '{"Error":"%s"}\n'%(e)
            self.wfile.write(output.encode())
            raise(e)



    def getBody(self):
        content_len = int(self.headers['content-length'])
        tempStr = self.rfile.read(content_len)
        return tempStr

    def setHeader(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json".encode())
        self.end_headers()

    # def displayZones(self):
    #     profileInstance = ProfileInstance.getInstance()
    #     self.wfile.write(profileInstance.zoneProfiles.getJson().encode())
