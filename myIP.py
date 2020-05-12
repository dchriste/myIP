#python3.8

from datetime import date
from datetime import datetime
from socket import gethostname
from socket import gethostbyname
import os.path
import inspect
import argparse
import sys

class ipCheck:

    def __init__(self,latestList):
        latestList = latestList.split(',')
        self.hostname = latestList[0]
        self.ip = latestList[1].strip()
        self.Dt = latestList[2].strip()
        self.Tm = latestList[3].strip()

parser = argparse.ArgumentParser(description='Logs the Hostname and IP of this host.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-l','--list',help='list all machines\' latest IPs',action='store_true')
group.add_argument('-p','--print',help='print the latest Host & IP',action='store_true')
parser.add_argument('-v','--verbose',help='increases verbosity of print and errors',action='store_true')
args = parser.parse_args()

scriptFile = inspect.getframeinfo(inspect.currentframe()).filename
scriptPath = os.path.abspath(os.path.dirname(sys.argv[0])) + '\\'
todayStr = str(date.today().strftime('%m-%d-%y'))
current_time = str(datetime.now().strftime("%H:%M:%S"))
errLog = '{path}{dir}_myIPerror.log'.format(path=scriptPath,dir=todayStr)
latestIPs = '{path}latestIPs.csv'.format(path=scriptPath)
isFirst = True

try:
    
    hostName = gethostname()
    hostIP = gethostbyname(hostName)    
    myHostsFile = '{path}{hostname}.csv'.format(path=scriptPath,hostname=hostName)
    if os.path.exists(myHostsFile): isFirst = False
    
    writeStr = '{host},{ip},{day},{time}\n'.format(host=hostName,ip=hostIP,day=todayStr,time=current_time)

    if not args.list:
        with open(myHostsFile,mode='a+',encoding='utf-8') as writeFile:            
            headerStr = 'Hostname,IP Address,Date Checked,Time Checked\n' if isFirst else ''            
            writeFile.write(headerStr + writeStr)
        
        if args.print and not args.verbose:
            print('\n' + 'The IP of {host} was {ip} as of {day} at {time}\n'.format(host=hostName,ip=hostIP,day=todayStr,time=current_time))

    hosts = []
    isFound = False

    if os.path.exists(latestIPs):
        #read the contents of the file, modifying only pertinent data (in place)
        with open(latestIPs, mode='r',encoding='utf-8') as readFile:
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

    sorter = lambda item : item.hostname
    hosts.sort(key=sorter)
    if (args.print and args.verbose) or args.list: print('\n',end='')

    isFirst = True

    for hst in hosts:
        #deal with printing if requested
        if (args.print and args.verbose) or args.list: 
            note =  ' *[this host]' if hst.hostname == hostName else ''
            print('{0.hostname}: {0.ip} as of {0.Dt} at {0.Tm}{note}'.format(hst,note=note))
        
        #deal with files if not listing
        if not args.list:
            if isFirst and os.path.exists(latestIPs): os.remove(latestIPs)
            with open(latestIPs,mode='a+',encoding='utf-8') as writeFile:
                headerStr = 'Hostname,IP Address,Date Checked,Time Checked\n' if isFirst else ''
                isFirst = False
                writeStr = '{0.hostname},{0.ip},{0.Dt},{0.Tm}\n'.format(hst)
                writeFile.write(headerStr + writeStr)

    if (args.print and args.verbose) or args.list: print('\n',end='')

except Exception as e:
    if args.print or args.verbose: print('An error occurred during host and IP retrieval: \nError Message is \"{error}\"\n'.format(error=e))
    with open(errLog, 'a+') as errFile:
        current_time = str(datetime.now().strftime("%H:%M:%S"))
        errFile.write('At {time}, during host and IP retrieval, the script returned the following error: {error}\n'.format(time=current_time,error=e))
