#
#  DocUtilController.py
#  docpad
#
#  Created by Manuel Astudillo on 7/26/09.
#  Copyright (c) 2009 CodeTonic. All rights reserved.
#

from Foundation import *
from Cocoa import NSOKButton, NSASCIIStringEncoding

# DocUtils
from docutils.core import publish_parts
from docutils.writers import html4css1
from docutils import nodes
from docutils.parsers.rst import directives

# Pygments
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = True

# The default formatter
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)

# Add name -> formatter pairs for every variant you want to use
VARIANTS = {
    # 'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # no lexer found - use the text one instead of an exception
        lexer = TextLexer()
    # take an arbitrary option if more than one is given
    formatter = options and VARIANTS[options.keys()[0]] or DEFAULT
    parsed = highlight(u'\n'.join(content), lexer, formatter)
    return [nodes.raw('', parsed, format='html')]

pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
pygments_directive.options = dict([(key, directives.flag) for key in VARIANTS])

directives.register_directive('sourcecode', pygments_directive)

# Controller class

class DocUtilController(NSObject):
	textView = objc.IBOutlet()
	webView = objc.IBOutlet()
	
	@objc.IBAction
	def renderReST_(self,sender):
		text = self.textView.string()
		self.webView.mainFrame().loadHTMLString_baseURL_(restify(text), None)
		
	@objc.IBAction
	def showOpenPanel_(self, sender):
		panel = NSOpenPanel.openPanel()
		panel.setCanChooseFiles_(True)
		panel.setCanChooseDirectories_(False)
		panel.setRequiredFileType_("txt")
		NSLog(u'Starting openPanel')
		runResult = panel.runModalForDirectory_file_(NSHomeDirectory(), None)
		if runResult == NSOKButton:
			NSLog("File: %s" % panel.filenames()[0])
			string = NSString.stringWithContentsOfFile_encoding_error_("/Users/manuel/Documents/plunatica/debut.txt", NSASCIIStringEncoding, None )
			self.textView.setString_(string[0])
			self.webView.mainFrame().loadHTMLString_baseURL_(restify(string[0]), None)
			
			#if not self.textView.writeToFile_atomically_(panel.filename_(), True):
			#	NSBeep()
		NSLog(u'openPanel started')
		
	@objc.IBAction
	def saveFile_(self, sender): 
		# create or get the shared instance of NSSavePanel
		panel = NSSavePanel.savePanel()
 
		# set up new attributes 
		#sp.setAccessoryView_(
		panel.setRequiredFileType_("txt")
 
		# display the NSSavePanel
		runResult = panel.runModalForDirectory_file_(NSHomeDirectory(), "")
		
		# if successful, save file under designated name 
		if runResult == NSOKButton:
			if not textData.writeToFile_atomically_(panel.filename_(), True):
				NSBeep()
				
	def textView_doCommandBySelector_(self, textView, commandSelector):
		
		NSLog(u"Command Selector: %s" % commandSelector)
		
		#if commandSelector == u"insertNewline:":
		text = self.textView.string()
		self.webView.mainFrame().loadHTMLString_baseURL_(restify(text), None)
			
#from django.utils.encoding import force_unicode, smart_str

# Import pygments directive, pass if pygments is not found
#try:
#    import rstify.pygments_directive
#except ImportError:
#    pass

class TextutilsHTMLWriter(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = TextutilsHTMLTranslator

class TextutilsHTMLTranslator(html4css1.HTMLTranslator):

    def __init__(self, document):
        html4css1.HTMLTranslator.__init__(self, document)

def restify( text, initial_header_level=1, language_code='en', settings_overrides=None, writer_overrides=TextutilsHTMLWriter):
	settings = {
        'initial_header_level': initial_header_level,
        'doctitle_xform': False,
        'language_code': language_code,
        'footnote_references': 'superscript',
        'trim_footnote_reference_space': True,
        'default_reference_context': 'view',
        'link_base': '',
    }
	# Import user settings and overwrite default ones
    # user_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
    # settings.update(user_settings)
	parts = publish_parts( source=text, writer=writer_overrides(), settings_overrides=settings )
	return parts['body']


"""
def rstify(text,
           initial_header_level=1,
           language_code='en',
           settings_overrides=None,
           writer_overrides=TextutilsHTMLWriter):

    settings = {
        'initial_header_level': initial_header_level,
        'doctitle_xform': False,
        'language_code': language_code,
        'footnote_references': 'superscript',
        'trim_footnote_reference_space': True,
        'default_reference_context': 'view',
        'link_base': '',
    }

    # Import user settings and overwrite default ones
    user_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
    settings.update(user_settings)

#    parts = publish_parts(
#        source=smart_str(text),
#        writer=writer_overrides(),
#        settings_overrides=settings
#    )
#	return force_unicode(parts['body'])

	parts = publish_parts( source=text, writer=writer_overrides(), settings_overrides=settings )

	return parts['body']
"""    