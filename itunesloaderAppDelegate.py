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

def osascript(cmd_text):
    cmd = '/usr/bin/osascript -e \'' + cmd_text + '\''
    p = subprocess.Popen(cmd, shell=True)

class itunesloaderAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
        NSApp.setServicesProvider_(self)

    @objc.signature('v@:@@o^@')
    def doString_userData_error_(self, pboard, userData, error):
        # download the archive and add to itunes
        pboardString = pboard.stringForType_(NSStringPboardType)
        #NSLog(pboardString)
        #NSLog(u'%s' % pboardString)
        if pboardString[:7] in ['http://', 'https:/']:
            #terminal = appscript.app('Terminal')
            url = str(pboardString)

            cwd = os.path.dirname(__file__)
            script_path = os.path.join(cwd, 'downloadtoitunes.py')
            
            term_cmd = u'python \\"' + script_path + u'\\" \\"' + url + u'\\"'
            osascript_cmd = u'tell application "Terminal" to do script "' + term_cmd + '"'
            osascript(osascript_cmd)
            osascript(u'tell application "Terminal" to activate')
