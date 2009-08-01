#
#  docpadDocument.py
#  docpad
#
#  Created by Manuel Astudillo on 8/1/09.
#  Copyright CodeTonic 2009. All rights reserved.
#

from Foundation import *
from AppKit import *

from Cocoa import NSOKButton, NSASCIIStringEncoding, NSUTF8StringEncoding

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



class docpadDocument(NSDocument):
	textView = objc.IBOutlet()
	webView = objc.IBOutlet()
	
	def init(self):
		self = super(docpadDocument, self).init()
		
		# initialization code
		NSLog("Initializing...")
		self.textContents = NSString.stringWithString_(u'')
		return self
		
	def initTextView(self, string ):
		font = NSFont.fontWithName_size_("Courier", 12)
		self.textView.setFont_(font)
		
		self.textView.setString_(string)
		self.textView.setDelegate_(self)
		
	def rest2html(self):
		text = self.textView.string()
		self.webView.mainFrame().loadHTMLString_baseURL_(restify(text), None)
		
	def windowNibName(self):
		return u"docpadDocument"
    
	def windowControllerDidLoadNib_(self, aController):
		super(docpadDocument, self).windowControllerDidLoadNib_(aController)
		
		NSLog("Nib Loaded")
		self.initTextView( self.textContents )
		self.rest2html()

	def dataOfType_error_(self, typeName, outError):
		NSLog("Data Of Type %s" % typeName )
		
		tmp = NSString.stringWithString_(self.textView.string())
		data = tmp.dataUsingEncoding_(NSASCIIStringEncoding)
		
		return (data, None)
   	
	def readFromData_ofType_error_(self, data, typeName, outError):
		NSLog("Data Of Type %s" % typeName )
	
		self.textContents = NSString.alloc().initWithData_encoding_(data, NSUTF8StringEncoding)
		if self.textContents != None:
			readSuccess = True
		else:
			readSuccess = False
	
		return (readSuccess, None)
		
	def textView_doCommandBySelector_(self, textView, commandSelector):
		NSLog(u"Command Selector: %s" % commandSelector)
		self.rest2html()
		#if commandSelector == u"insertNewline:":

