#
#  docpadAppDelegate.py
#  docpad
#
#  Created by Manuel Astudillo on 7/26/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

from Foundation import *
from AppKit import *

class docpadAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
