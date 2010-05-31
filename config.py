

#from configobj import ConfigObj
#import ConfigParser
#import json
import pickle

import sys
from os import path, environ, makedirs

APP_NAME = "Download To iTunes"
CONFIG_FILENAME = 'config.cfg'

DEFAULTS = {'iTunesManagesMyLibrary': 1, 'iTunesLibraryLocation': None}

def data_path():
    #if sys.platform == 'darwin':
    from AppKit import NSSearchPathForDirectoriesInDomains
    # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
    # NSApplicationSupportDirectory = 14
    # NSUserDomainMask = 1
    # True for expanding the tilde into a fully qualified path
    ret = path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], APP_NAME)
    if not path.exists(ret):
        makedirs(ret)
    return ret

def config_file_path():
    data_dir = data_path()
    return path.join(data_dir, CONFIG_FILENAME)


def get_config():
    #return ConfigObj(config_file_path())
    #config2 = ConfigParser.RawConfigParser()
    #config2.read(config_file_path())
    #return config2
    try:
        f = open(config_file_path())
        s = f.read()
        f.close()
    except IOError:
        return {}
    if s:
    #return json.loads(s)
        return pickle.loads(s)
    else:
        return {}


def save_config(config_obj):
    #config_obj.write(config_file_path())
    f = file(config_file_path(), 'w')
    #s = json.dumps(config_obj)
    s = pickle.dumps(config_obj)
    f.write(s)
    f.close()

def set_config_option(key, value):
    '''Sets and saves option.'''
    config_obj = get_config()
    #config_obj[key] = value
    config_obj[key] = value
    save_config(config_obj)

def get_config_option(key):
    config_obj = get_config()
    return config_obj.get(key, DEFAULTS.get(key, None))




#elif sys.platform == 'win32':
#    appdata = path.join(environ['APPDATA'], APPNAME)
#else:
#    appdata = path.expanduser(path.join("~", "." + APPNAME))
    
