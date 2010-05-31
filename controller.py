#
#  controller.py
#  itunesloader
#
#  Created by Alex Ehlke on 5/30/10.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet, ivar, accessor
from Foundation import *
from AppKit import *

import config



class controller(NSWindowController):
    iTunesManagesMyLibrary = ivar('iTunesManagesMyLibrary')
    #iTunesManagesMyLibrary = ivar()
    iTunesManagesMyLibraryMenuItem = IBOutlet()
    iTunesLibraryLocationMenuItem = IBOutlet()
    iTunesLibraryLocationMenuItemEnabled = ivar('iTunesLibraryLocationMenuItemEnabled')

    def awakeFromNib(self):
        #NSLog('awakeFromNib')
        self.iTunesManagesMyLibrary = config.get_config_option('iTunesManagesMyLibrary')
        self.iTunesManagesMyLibraryMenuItem.setState_(self.iTunesManagesMyLibrary)
        self.refreshMenuEnable()

    #@accessor
    #def iTunesManagesMyLibraryValue(self):
    #    return self.iTunesManagesMyLibrary

    @accessor
    def setITunesManagesMyLibrary_(self, value):
        #NSLog('setITunesManagesMyLibrary_')
        self.iTunesManagesMyLibrary = value
        #NSLog(str(self.iTunesManagesMyLibrary))
        config.set_config_option('iTunesManagesMyLibrary', value)
        self.refreshMenuEnable()

    @IBAction
    def setLibraryLocation_(self, sender):
        #NSLog('setLibraryLocation_')
        panel = NSOpenPanel.openPanel()
        panel.setCanChooseDirectories_(YES)
        panel.setAllowsMultipleSelection_(NO)
        panel.setCanChooseFiles_(NO)
        old_path = config.get_config_option('iTunesLibraryLocation')
        ret = panel.runModalForDirectory_file_types_(old_path, None, None)
        #NSLog(str(ret))
        if ret:
            path = panel.filenames()[0]
            config.set_config_option('iTunesLibraryLocation', path)
        else:
            # Canceled
            pass

    def refreshMenuEnable(self):
        #NSLog('refreshMenuEnable')
        if self.iTunesManagesMyLibrary:
            #NSLog('NO')
            #self.iTunesLibraryLocationMenuItem.setEnabled_(NO)
            self.iTunesLibraryLocationMenuItemEnabled = NO
        else:
            #NSLog('YES')
            #self.iTunesLibraryLocationMenuItem.setEnabled_(YES)
            self.iTunesLibraryLocationMenuItemEnabled = YES

    @IBAction
    def toggleITunesManagesMyLibrary_(self, sender):
        #NSLog('toggleITunesManagesMyLibrary_')
        #self.refreshMenuEnable()
        pass
        #NSLog('tog action')
        #self.iTunesLibraryLocationMenuItem.setEnabled_(self.iTunesManagesMyLibrary == 0)
        #pass
        
        #NSLog(sender.state())
        #NSLog(dir(self).__repr__())#self.iTunesManagesMyLibrary).__repr__())
        #self.toggleITunesManagesMyLibrary_.setState_(0)
        #NSLog(dir(self.toggleITunesManagesMyLibrary).__repr__())
        #toggleITunesManagesMyLibrary_.setEnabled(false)

        #self.iTunesManagesMyLibrary.setState_(0)
        #self.iTunesManagesMyLibrary.setEnabled(false)
        
    
