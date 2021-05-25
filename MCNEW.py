import requests, time, threading, os
from lxml import html

clear = lambda: os.system('cls')



min_players = input('Minimum player count: ')

mmp_found = 0
mmp_errors = 0
tms_found = 0
tms_errors = 0
ms_found = 0
ms_errors = 0

with open('T:\Python Projects\MC new server scraper\Result.txt', 'w') as file:
    file.write('')

def GUI():
    global mmp_found
    global mmp_errors
    global tms_found
    global tms_errors
    global ms_found
    global ms_errors
    
    while(True):
        clear()
        print(f'Servers on MMP Found: {mmp_found}\nErrors while scanning MMP: {mmp_errors}\n\nServers on TMS Found: {tms_found}\nErrors while scanning TMS: {tms_errors}\n\nServers on MS Found: {ms_found}\nErrors while scanning MS: {ms_errors}\n\n')
        time.sleep(0.5)

def mmp():
    global mmp_found
    global mmp_errors
    for page in range(1, 10000): #loads page after page on the site
        URL = f'https://minecraft-mp.com/servers/latest/{page}/'
        page = requests.get(URL)

        tree = html.fromstring(page.content)
        for server in range(1, 25):
            try:
                ip = tree.xpath('((//*[@height="90"])[{}]/td[2]/strong)/text()'.format(server))
                online = tree.xpath('((//*[@height="90"])[{}]/td[2]/span)/text()'.format(server))
                version = tree.xpath('((//*[@height="90"])[{}]/td[2]/a)[1]/text()'.format(server))
                name = tree.xpath('((//*[@height="90"])[{}]/td[2]/div/h4/a)[1]/text()'.format(server))
                players = tree.xpath('((//*[@height="90"])[{}]/td[3])[1]/text()'.format(server))
                country = tree.xpath('((//*[@height="90"])[{}]/td[2]/a[2]/img)/@title'.format(server))

                if str(players[0].split('/')[0]) != 'N' and int(str(players[0].split('/')[0])) >= int(min_players): #Checks if there are equal to or more players than the min allowed
                    if not name:
                        name = ['Unknown']
                
                    #print(f'IP: {ip[0]} - Name: {name[0]} - Country: {country[0]} - Status: {online[0]} - Version: {version[0]} - Players: {players[0]}')
                    with open('T:\Python Projects\MC new server scraper\Result.txt', 'a') as file:
                        file.write(f'IP: {ip[0]}\n    Name: {name[0]}\n    Country: {country[0]}\n    Status: {online[0]}\n    Version: {version[0]}\n    Players: {players[0]}\n    Found on: minecraft-mp.com\n\n')
                    mmp_found += 1
                    #time.sleep(0.1)
            except Exception as e:
                #print(f'Error mmp: {e}')
                mmp_errors += 1
                #return

def tms():
    global tms_found
    global tms_errors
    for page in range(1, 10000): #loads page after page on the site
        URL = f'https://topminecraftservers.org/sort/new/page/{page}'
        if(page == 1): #Checks if it is on the first page of the site (due to promoted servers)
            x = 6
            y = 25
        else:
            x = 1
            y = 20
        page = requests.get(URL)

        tree = html.fromstring(page.content)
        for server in range(x, y):
            try:
                ip = tree.xpath('((//*[@class="form-control text-justify"])[{}])/text()'.format(server))
                version = tree.xpath('((//*[@class="col-xs-12 col-md-6"]/a)[{}])/text()'.format(server))
                players = tree.xpath('((//*[@class="panel-body"])[{}]/span/b)/text()'.format(server))
                country = tree.xpath('((//*[tbody]/tbody/tr/td/a/img)[@width="16"])/@alt'.format(server))
                
                if str(players[0]) != 'Offline' and int(str(players[0])) >= int(min_players): #Checks if there are equal to or more players than the min allowed, also if it says offline where it normally says players

                    #print(f'IP: {ip[0]} - Country: {country[0]} - Version: {version[0]} - Players: {players[0]}')
                    with open('T:\Python Projects\MC new server scraper\Result.txt', 'a') as file:
                            file.write(f'IP: {ip[0]}\n    Country: {country[0]}\n    Version: {version[0]}\n    Players: {players[0]}\n    Found on: topminecraftservers.org\n\n')
                    tms_found += 1
                    #time.sleep(0.1)
            except Exception as e:
                #print(f'Error tms: {e}')
                tms_errors += 1
                #return

def ms():
    global ms_found
    global ms_errors
    for page in range(1, 10000): #loads page after page on the site
        URL = f'https://minecraft-server.net/rank/{page}/newest/'
        if(page == 1): #Checks if it is on the first page of the site (due to promoted servers)
            x = 7
            y = 25
        else:
            x = 1
            y = 20
        page = requests.get(URL)

        tree = html.fromstring(page.content)
        for server in range(x, y):
            try:
                ip = tree.xpath('(//*[@class="col-12 form-control copy-ip-address"])[{}]/@value'.format(server))
                name = tree.xpath('(//*[@class="h5 text-truncate"]/a)[{}]/text()'.format(server))
                players = tree.xpath('(//*[@class="col-lg-3 text-right d-none d-lg-block pl-3"]/div)[{}]/text()'.format(server))
                
                if int(str(players[0])) >= int(min_players): #Checks if there are equal to or more players than the min allowed

                    #print(f'IP: {ip[0]} - Name: {name[0]}  - Players: {players[0]}')
                    with open('T:\Python Projects\MC new server scraper\Result.txt', 'a') as file:
                            file.write(f'IP: {ip[0]}\n    Name: {name[0]}\n    Players: {players[0]}\n    Found on: minecraft-server.net\n    (unable to check server status & version :cry:)\n\n')
                    ms_found += 1
                    #time.sleep(0.1)
            except Exception as e:
                #print(f'Error ms: {e}')
                ms_errors += 1
                #return

if __name__ == "__main__":
    threadGUI = threading.Thread(target=GUI)
    threadTMS = threading.Thread(target=tms)
    threadMMP = threading.Thread(target=mmp)
    threadMS = threading.Thread(target=ms)
    threadGUI.start()
    threadTMS.start()
    threadMMP.start()
    threadMS.start()
