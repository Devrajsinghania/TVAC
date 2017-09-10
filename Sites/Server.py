#!/usr/bin/env python3.5
import socketserver
import sys

from VerbHandler import VerbHandler
from Collections.ProfileInstance import ProfileInstance
from Collections.HardwareStatusInstance import HardwareStatusInstance
from ThreadControls.ThreadCollectionInstance import ThreadCollectionInstance

from HouseKeeping import globalVars
from HouseKeeping.globalVars import debugPrint
# Adding verbose level for debug printing
verbos = 0

class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    # adding debug info
    globalVars.init()
    if(len(sys.argv)>1):
        for arg in sys.argv:
            if arg.startswith("-v"):
                globalVars.verbos = arg.count("v")
    print("\n"*3+"\033[93m"+
          "TVAC Starting!\n"+"\033[0m"+
          "Python Version: {:}".format(sys.version))
    debugPrint(1,"Debug on: Level " + str(globalVars.verbos))

    PORT = 8080

    debugPrint(1,"Starting initializing threads and drivers")
    
    hardwareStatusInstance = HardwareStatusInstance.getInstance()
    profileInstance = ProfileInstance.getInstance()
    threadInstance = ThreadCollectionInstance.getInstance()
    

    
    debugPrint(1,"Finished initializing threads and drivers")
    
    httpd = ReuseAddrTCPServer(("192.168.99.1", PORT), VerbHandler)

    print("\033[93m Set up is complete.\033[0m Starting to server request...")

    httpd.serve_forever()