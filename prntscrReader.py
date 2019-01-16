from random import choice, randint
from psutil import cpu_count
from threading import Thread
from urllib import request
from time import sleep
from lxml import html

# Headers
_Oheaders = request.build_opener()
_Oheaders.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
request.install_opener(_Oheaders)

# PG Function: Main Progress Function
def pg(block, t):
    """ Processing screenshot URLs and check if they valid or not, if valid the image added to queue """
    global TB, QUIT
    for x in block:
        print(f'[@ THREAD {t}] Processing https://prnt.sc/{x}...')
        try:
            _img = html.fromstring(request.urlopen(f'https://prnt.sc/{x}').read()).xpath('/html/body/div[3]/div/img/@src')[0]
            QUEUE[t].append([_img, x])
        except:
            print(f'[@ THREAD {t}] Invalid [{x}]')
    TB += 1
    if len(BLOCKS) == TB:
        print(f'[@ THREAD {t}] All Blocks completed. The program will stop when all screenshots will be saved in the folder...')
        sleep(.5)
        QUIT = True

# IMPI Function: Import Images Function
def impi(t):
    """ Check the queue and if new images provided it will import them to the "images" folder """
    while True:
        if QUIT and len(QUEUE[t]) == 0:
            break
        if len(QUEUE[t]) > 0:
            if QUEUE[t][0][0][:4] != '//st':
                request.urlretrieve(str(QUEUE[t][0][0]), filename=f'images/{QUEUE[t][0][1]}.jpg')
                print(f'[@ THREAD {t}] "images/{QUEUE[t][0][1]}.jpg" Saved')
                QUEUE[t] = QUEUE[t][1:]
            else:
                QUEUE[t] = QUEUE[t][1:]
        sleep(.1)

TB = 0 # Total Blocks (Int)
QUIT = False # QUIT Variable (Bool)
L = '' # Used to contain some time-limited information (String)
TU = int(cpu_count()/2) # TU(Threads-Use) Actully split thread-count and uses *2 (Example: TU=4, Actully 8 Will be used) (Int)
URLS = [] # Array of URLs (Array)
BLOCKS = [] # Array of BLOCKS (Array)
QUEUE = [] # Images QUEUE (Array)
SCNT = int(input('How many URLs you want to generate?: '))
if SCNT > 0:
    for x in range(SCNT):
        L = ''
        while True:
            for y in range(6):
                L += choice('qwertyuiopasdfghjklzxcvbnm1234567890')
            if not L in URLS:
                break
        URLS.append(L)
        print(f'[@] URL WAS GENERATED [{x+1}/{SCNT}]')
    print(f'[@] CUTTING TO BLOCKS...')
    DPB = int(len(URLS)/TU)
    for x in range(int(len(URLS)/DPB)):
        BLOCKS.append(URLS[DPB*x:DPB*x+DPB])
    BLOCKS = BLOCKS[:int(TU)]
    i = 0
    for x in BLOCKS:
        i += len(x)
        QUEUE.append([])
    print(f'[@] CUTTED TO {len(BLOCKS)} BLOCKS (URLs COUNT NOW IS {i} URLs)')
    for x in range(TU):
        Thread(target=pg, args=(BLOCKS[x], x)).start()
        Thread(target=impi, args=[x]).start()