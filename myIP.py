#python3.8
#last updated 3/10/20

from datetime import date
from datetime import datetime
from socket import gethostname
from socket import gethostbyname
import os.path
import inspect

try:
    scriptFile = inspect.getframeinfo(inspect.currentframe()).filename
    scriptPath = os.path.dirname(os.path.abspath(scriptFile)) + '\\'
    errLog = scriptPath + '_myIPerror.log'
    isFirst = True

    hostName = gethostname()
    hostIP = gethostbyname(hostName)
    
    myHostsFile = scriptPath + hostName + '.csv'
    if os.path.exists(myHostsFile): isFirst = False

    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    with open(myHostsFile,mode='a+') as writeFile:
        headerStr = 'Hostname,IP Address,Date Checked,Time Checked\n' if isFirst else ''
        writeStr = hostName + ', ' + hostIP + ', ' + str(today.strftime('%m-%d-%y')) + ', ' + str(now.strftime("%H:%M:%S")) + '\n'
        writeFile.write(headerStr + writeStr)
    pass

    print('\n' + 'The IP of ' + hostName + ' was ' + hostIP + ' as of ' + str(today.strftime('%m-%d-%y')) + ' at ' + str(now.strftime("%H:%M:%S")) + '\n')

except Exception as e:
    print('An error occurred : \nError Message is \"' + str(e)) + '\"\n'
    with open(errLog, 'a+') as errFile:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        errFile.write('At ' + str(current_time) + ' the script returned the following error: ' + str(e) + '\n')
    pass
