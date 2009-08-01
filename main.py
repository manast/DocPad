#
#  main.py
#  docpad
#
#  Created by Manuel Astudillo on 7/26/09.
#  Copyright CodeTonic 2009. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import docpadDocument

# pass control to AppKit
AppHelper.runEventLoop()
