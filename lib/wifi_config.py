from __future__ import print_function
import sys
import os.path
import re
import subprocess
from collections import OrderedDict

setting = re.compile(r"^\s*(?P<key>\w+)=\"?(?P<value>[-\w/]+)\"?$", re.MULTILINE)
network = re.compile(r"^network=\{(?P<net_config>.+?)\}$" , re.MULTILINE + re.DOTALL)

class Network(object):
    def __init__(self , d):
        self.ssid = d["ssid"]
        self.psk = d["psk"]

        if self.ssid == "":
            raise ValueError("SSID is empty string - invalid")

        if self.psk == "":
            raise ValueError("PSK key is empty string -invalid")



    def save(self , f):
        f.write("network={\n")
        f.write("\tssid=\"%s\"\n" % self.ssid)
        f.write("\tpsk=\"%s\"\n" % self.psk)
        f.write("\tkey_mgmt=WPA-PSK\n")
        f.write("}\n\n")



class WifiConfig(object):
    network_settings = set(["ssid" , "psk" , "key_mgmt"])

    def __init__(self , config_file = "/etc/wpa_supplicant/wpa_supplicant.conf"):
        self.__networks = {}
        self.__settings = OrderedDict()
        self.config_file = config_file
        with open(config_file) as f:
            content = f.read()
            for (key,value) in setting.findall( content ):
                if not key in WifiConfig.network_settings:
                    self.__settings[key] = value
                    

            for net_config in network.findall( content ):
                d = {}
                for (key,value) in setting.findall( net_config ):
                    d[key] = value

                self.__networks[d["ssid"]] = Network(d)


    def addnetwork(self, ssid , psk):
        if ssid in self.__networks:
            network = self.__networks[ssid]
            network.psk = psk
        else:
            self.__networks[ssid] = Network( {"ssid" : ssid, "psk" : psk} )
            

    def networks(self):
        return self.__networks

            
    def settings(self):
        return self.__settings


    def save(self , config_file = None):
        if config_file is None:
            config_file = self.config_file

        with open(config_file , "w") as f:
            for key,value in self.__settings.items():
                f.write("%s=%s\n" % (key,value))

            for network in self.__networks.values():
                network.save( f )
                
    @classmethod
    def ifup(cls):
        print("Trying: /sbin/ifup wlan0 ...",end = "")
        sys.stdout.flush()
        status = subprocess.check_call(["/sbin/ifup" , "wlan0"])
        if status == 0:
            print("OK")
        else:
            print("failed")
