import multiprocessing
import requests

import os

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
