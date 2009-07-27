#
#  DocUtilController.py
#  docpad
#
#  Created by Manuel Astudillo on 7/26/09.
#  Copyright (c) 2009 CodeTonic. All rights reserved.
#

from Foundation import *

from docutils.core import publish_parts
from docutils.writers import html4css1
from docutils import nodes
from docutils.parsers.rst import directives

class DocUtilController(NSObject):
	textView = objc.IBOutlet()
	webView = objc.IBOutlet()
    
	@objc.IBAction
	def renderReST_(self,sender):
		text = self.textView.string()
		NSLog(u"Text: %s" % text)
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