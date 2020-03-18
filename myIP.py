#python3.8

from datetime import date
from datetime import datetime
from socket import gethostname
from socket import gethostbyname
import os.path
import inspect
import argparse

class ipCheck:

    def __init__(self,latestList):
        latestList = latestList.split(',')
        self.hostname = latestList[0]
        self.ip = latestList[1].strip()
        self.Dt = latestList[2].strip()
        self.Tm = latestList[3].strip()

parser = argparse.ArgumentParser(description='Logs the Hostname and IP of this host.')
parser.add_argument('-p','--print',help='print the latest Host & IP',action='store_true')
parser.add_argument('-v','--verbose',help='increases verbosity of print and errors',action='store_true')
args = parser.parse_args()

scriptFile = inspect.getframeinfo(inspect.currentframe()).filename
scriptPath = os.path.dirname(os.path.abspath(scriptFile)) + '\\'
todayStr = str(date.today().strftime('%m-%d-%y'))
errLog = scriptPath + todayStr + '_myIPerror.log'
latestIPs = scriptPath + 'latestIPs.csv'
isFirst = True

try:
    
    hostName = gethostname()
    hostIP = gethostbyname(hostName)    
    myHostsFile = scriptPath + hostName + '.csv'
    if os.path.exists(myHostsFile): isFirst = False
    
    with open(myHostsFile,mode='a+') as writeFile:
        current_time = str(datetime.now().strftime("%H:%M:%S"))
        headerStr = 'Hostname,IP Address,Date Checked,Time Checked\n' if isFirst else ''
        writeStr = hostName + ', ' + hostIP + ', ' + todayStr + ', ' + current_time + '\n'
        writeFile.write(headerStr + writeStr)
    
    if args.print and not args.verbose:
        print('\n' + 'The IP of ' + hostName + ' was ' + hostIP + ' as of ' + todayStr + ' at ' + current_time + '\n')

    hosts = []
    isFound = False

    if os.path.exists(latestIPs):
        #read the contents of the file, modifying only pertinent data (in place)
        with open(latestIPs, mode='r') as readFile:
            Unused = readFile.readline() #read headers to keep them out of loop

            for line in readFile:
                host = ipCheck(line)
                #update working host when found
                if host.hostname == hostName:
                    isFound = True
                    host.ip = hostIP
                    host.Dt = todayStr
                    host.Tm = current_time
                hosts.append(host)
    
    if not isFound:
        #place current item in list and the following will create the file
        host = ipCheck(writeStr)
        hosts.append(host)

    with open(latestIPs,mode='w+') as writeFile:
        writeFile.write('Hostname,IP Address,Date Checked,Time Checked\n')
        sorter = lambda item : item.hostname
        hosts.sort(key=sorter)
        if args.print and args.verbose: print('\n')

        for hst in hosts:
            if args.print and args.verbose: 
                note =  ' *[this host]' if hst.hostname == hostName else ''
                print(hst.hostname + ": " + hst.ip + " as of " + hst.Dt + " at " + hst.Tm + str(note))
            writeStr = hst.hostname + ', ' + hst.ip + ', ' + hst.Dt + ', ' + hst.Tm + '\n'
            writeFile.write(writeStr)
        
        if args.print and args.verbose: print('\n')

except Exception as e:
    if args.print or args.verbose: print('An error occurred during host and IP retrieval: \nError Message is \"' + str(e)) + '\"\n'
    with open(errLog, 'a+') as errFile:
        current_time = str(datetime.now().strftime("%H:%M:%S"))
        errFile.write('At ' + current_time + ', during host and IP retrieval, the script returned the following error: ' + str(e) + '\n')

