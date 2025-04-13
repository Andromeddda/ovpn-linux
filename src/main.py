import pages
from pages import Connection
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import os
import json
from vpn import start_vpn, try_timeout

def connection_is_good(connection: Connection):
    return (connection.country == 'Japan') and (connection.delay in range(1, 20)) and ('udp' in connection.url)


def read_json(file):
    with open(file) as F:
        return json.load(F)
    
    
def run():
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

if __name__ == "__main__":
    run()