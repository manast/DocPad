#
#  docpadAppDelegate.py
#  docpad
#
#  Created by Manuel Astudillo on 7/26/09.
#  Copyright CodeTonic 2009. All rights reserved.
#

from Foundation import *
from AppKit import *
import objc

class docpadAppDelegate(NSObject):
	textView = objc.IBOutlet()
	
	def applicationDidFinishLaunching_(self, sender):
		font = NSFont.fontWithName_size_("Courier", 12)
		self.textView.setFont_(font)
		self.textView.setString_("")
		NSLog("Application did finish launching.")
		
	def applicationWillTerminate_(self,sender):
		NSLog("Application will terminate.")
		
	def applicationSupportFolder(self):
		paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,NSUserDomainMask,True)
		basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
		fullPath = basePath.stringByAppendingPathComponent_("MetaWindow")
		if not os.path.exists(fullPath):
			os.mkdir(fullPath)
		return fullPath
        
	def pathForFilename(self,filename):
		return self.applicationSupportFolder().stringByAppendingPathComponent_(filename)
		
	
