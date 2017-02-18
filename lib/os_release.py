from sys import version as sys_version
from os import uname
from os.path import isfile
from datetime import datetime as dt

def _read_os_release(pfx='LSB_'):
    fname = '/etc/os-release'
    if not isfile(fname):
        return {}
    def processline(ln):
        return ln.strip().replace('"', '')
    def splitline(ln, pfx=''):
        if ln.count('=') == 1:
            k,v = ln.split('=')
            return pfx+k,v
        return None
    props = {}
    with open(fname, 'r') as f:
        for line in f:
            kv = splitline(processline(line), pfx=pfx)
            if kv:
                props[kv[0]] = kv[1]
    return props

def sys_info():
    """This gets basic system information to log on startup"""
    sysname, nodename, release, version, machine = uname()
    python_vs, python_cc = sys_version.split('\n')
    req_vs = '0.0.0'
    local_time = dt.now().isoformat()
    lsb = None
    try:
        lsb = _read_os_release()
    except:
        pass
    try:
        import requests
        req_vs = requests.__version__
    except:
        pass
    if not lsb:
        lsb = {}
    sysinf =  {'sysname'  : sysname,
               'nodename' : nodename,
               'release'  :  release,
               'version'  : version,
               'python'   : python_vs,
               'pythoncc' : python_cc,
               'requests' : req_vs,
               'localtime': local_time}
    sysinf.update(lsb)
    return sysinf

if __name__ == '__main__':
    import json
    print(json.dumps(sys_info(), indent=4, sort_keys=True))
