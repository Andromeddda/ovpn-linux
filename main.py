import time
import pages
from pages import Connection
from bs4 import BeautifulSoup
from requests_html import HTMLSession

import requests
import os
import multiprocessing
import json

def get_vpn_page_url():
    with open('vpn_page_url.txt') as F:
        return F.readline()
    
def connection_is_good(connection: Connection):
    return (connection.country == 'Japan') and (connection.delay in range(1, 20)) and ('udp' in connection.url)


def try_decrator(process):
    def result(ret: bool, *args) -> bool:
        try:
            process(*args)
            ret = True
        except:
            ret = False
    return result


def try_timeout(process, *arg):
    func = try_decrator(process)

    ret = True
    p = multiprocessing.Process(target=func, args=[ret, *arg])
    p.start()

    p.join(10)

    if p.is_alive():
        p.kill()
        p.join()

    return ret

def read_json(file):
    with open(file) as F:
        return json.load(F)
    

def start_vpn(config_url, name, path):

    print(f"Trying to get config {config_url}...")

    r = requests.get(config_url)
    open(path, 'wb').write(r.content)

    print(f"Config witten to {path}")
    print(f"Trying to create vpn connection...")

    os.system(f'nmcli connection delete {name}')
    
    if(os.system(f'nmcli connection import type openvpn file {path}') != 0):
        raise "Incorrect configuration"
    
    if(os.system(f'nmcli connection up {name}') != 0):
        raise "Cannot connect to vpn server"

def say(n):
    print(n)
    time.sleep(1)


if __name__ == "__main__":
    strings = read_json('strings.json')

    vpn_page_url = strings['url']

    session = HTMLSession()

    page = pages.get_page(session, vpn_page_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    connections = pages.get_connections(soup)

    good_connections = [x for x in connections if connection_is_good(x)]
    good_connections.sort(key = lambda x: x.delay )

    os.system('mkdir -p configs')

    for connection in good_connections:
        if (try_timeout(start_vpn, connection.url, strings['name'], strings['path'])):
            print('SUCCESS')
            break

        print()
    






    
