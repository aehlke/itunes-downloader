#
#  itunesloaderAppDelegate.py
#  itunesloader
#
#  Created by Alex on 1/21/10.
#  Copyright __MyCompanyName__ 2010. All rights reserved.
#

from Foundation import *
from AppKit import *
import objc
import subprocess
import sys
import os
#import appscript

#import controller
import config

def osascript(script, *args):
    #cmd = '/usr/bin/osascript -e \'' + script + '\''
    #p = subprocess.Popen(['arch', '-i386', 'osascript', '-e', script] +
    p = subprocess.Popen(['arch', '-i386', '/usr/bin/osascript', '-e', script] +
            [unicode(arg) for arg in args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)#cmd, shell=True)
    #err = p.wait()
    (stdout, stderr) = p.communicate()
    #if err:
    #    raise RuntimeError(err, p.stderr.read()[:-1].decode('utf8'))
    #return p.stdout.read()[:-1].decode('utf8')
    return stdout[:-1].decode('utf8')
    


def prompt_dialog(query, default=''):
    '''prompts the user for text input and returns string response, or None if Cancel.'''
    #tell application "System Events"
    #     activate
    #end tell
    script = """on run {querystr, defstr}
                tell application "System Events"
                     display dialog querystr default answer defstr buttons {"Cancel", "OK"} default button 2
                end tell
                if button returned of the result is equal to "OK" then
                   return text returned of the result
                else
                   return ""
                end if
                end run"""
    ret = osascript(script, query, default)
    return ret
    


class itunesloaderAppDelegate(NSObject):
    #iTunesManagesMyLibrary = objc.ivar()
    def applicationDidFinishLaunching_(self, sender):
        #NSLog("Application did finish launching.")
        NSApp.setServicesProvider_(self)

    @objc.signature('v@:@@o^@')
    def doString_userData_error_(self, pboard, userData, error):
        # download the archive and add to itunes
        pboardString = pboard.stringForType_(NSStringPboardType)

        #iTunesManagesMyLibrary = config.get_config_option('iTunesManagesMyLibrary')
        #NSLog(str(iTunesManagesMyLibrary))
        #NSLog(dir(controller).__repr__())
        #return
        
        #NSLog(pboardString)
        #NSLog(u'%s' % pboardString)
        if pboardString[:7] in ['http://', 'https:/']:
            #terminal = appscript.app('Terminal')
            url = str(pboardString)

            cwd = os.path.dirname(__file__)
            script_path = os.path.join(cwd, 'downloadtoitunes.py')
            
            term_cmd = u'python \\"' + script_path + u'\\" \\"' + url + u'\\"'
            osascript_cmd = u'tell application "Terminal" to do script "' + term_cmd + '"'
            ret = osascript(osascript_cmd)
            NSLog(unicode(ret))
            osascript(u'tell application "Terminal" to activate')
