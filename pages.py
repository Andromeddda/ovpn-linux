import requests_html
import  time
import nest_asyncio


def uptime_str_to_int(s: str):
    if (s == None):
        return 0

    split = s.split(' ')

    if (len(split) < 2):
        return 0

    num = int(s[0])
    if (split[1] == 'mins'):
        return num
    elif (split[1] == 'hours'):
        return 60*num
    elif (split[1] == 'days'):
        return 24*60*num
    return 0

def delay_str_to_int(s: str):
    split = s.split(' ')

    if (len(split) < 2):
        return 0

    if (split[1] == 'ms'):
        return int(split[0])
    
    return 60

def convert_block(block):
    country = str(block[0].contents[0])
    url = block[1].a.get('href')
    uptime = uptime_str_to_int(str(block[2].contents[0]))
    delay = delay_str_to_int(str(block[3].contents[0]))
    return Connection(country = country, url = url, uptime = uptime, delay = delay)

class Connection:
    def __init__(self, country, url, uptime, delay):
        self.country = country
        self.uptime = uptime
        self.delay = delay
        self.url = url

    def __repr__(self):
        return f'Connection({self.country}, {self.url}, {self.uptime}, {self.delay})'
        

def get_page(session, url):
    nest_asyncio.apply()

    r = requests_html.HTMLResponse(session)

    print(f"Trying to connect to {url}")
    for _ in range(5):    
        try:
            r = session.get(url)
            print(f"Successfully connected to {url}")
            return r
        except:
            time.sleep(1)
    
    print(f"Cannot reach page. Check your network connection")
    return r


def prev_div(div):
    return div.previous_sibling.previous_sibling

def next_div(div):
    return div.next_sibling.next_sibling

def get_block_by_a(element):
    parent = element.parent
    return (prev_div(parent), parent, next_div(parent), next_div(next_div(parent)))


def get_connections(soup):
    elements = soup.find('body').find_all(download="")
    return [convert_block(get_block_by_a(x)) for x in elements]
