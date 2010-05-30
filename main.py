#
#  main.py
#  itunesloader
#
#  Created by Alex Ehlke on 1/21/10.
#  Copyright __MyCompanyName__ 2010. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import itunesloaderAppDelegate

# pass control to AppKit
AppHelper.runEventLoop()
